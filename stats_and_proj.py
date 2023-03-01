# Copyright (C) 2023 Warren Usui, MIT License
"""
Get CBS player statistics (scraping web pages)
"""
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

def _rootdir():
    return "https://www.cbssports.com/fantasy/baseball/stats/"

def _this_year():
    return datetime.date.today().year

def _last_year():
    return _this_year() - 1

def _read_stat_page(stat_details):
    return BeautifulSoup(requests.get(
                "".join([_rootdir(), stat_details]),
                timeout=600).text, 'html.parser').find("tbody")

def _check_all_pos(inp_func):
    return list(map(inp_func,
                    ['C', '1B', '2B', 'SS', '3B', 'OF', 'U', 'SP', 'RP']))

def _extract_numb(plyr_info):
    return plyr_info["href"].split("/")[3]

def _get_current_page(position):
    return f"{position}/{_this_year()}/season/projections"

def _get_past_page(position):
    return f"{position}/{_last_year()}/season/stats"

def _get_pnumb_list(web_page):
    return list(map(_extract_numb,
           _read_stat_page(web_page).find_all("a", href=True)))[::2]

def _build_df(stat_set):
    def _bld_get_cols(df0):
        if stat_set[1] == 'P':
            return df0.iloc[:, [3, 5, 10, 11, 13, 14, 17]]
        return df0.iloc[:, [5, 6, 7, 11, 12, 20]]
    def _bld_df_output(df1):
        df1.rename(index=dict(zip(
            list(range(len(df1.index))), _get_pnumb_list(stat_set)))
            ).to_excel("_".join(stat_set.split('/')[0:2]) + ".xlsx")
    def _bld_df_handle_pd(df0):
        _bld_df_output(_bld_get_cols(df0))
    print(stat_set)
    _bld_df_handle_pd(pd.read_html("".join([_rootdir(), stat_set]))[0])
    return stat_set

def _stats_and_proj(position):
    return [_build_df(_get_current_page(position)),
            _build_df(_get_past_page(position))]

def gen_spreadsheets():
    """
    Generate the spreadsheets for each position's statistics from last year
    and projected statistics for this year
    """
    return _check_all_pos(_stats_and_proj)

if __name__ == "__main__":
    if len(gen_spreadsheets()) != 9:
        print("Potential Problem")
