# Copyright (C) 2023 Warren Usui, MIT License
"""
Get CBS player statistics (scraping web pages)
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from common_gnus import this_year, last_year

def _read_df(fname):
    return "".join(["https://www.cbssports.com/fantasy/baseball/stats/",
                    fname])

def _read_stat_page(stat_details):
    return BeautifulSoup(requests.get(
                _read_df(stat_details),
                timeout=600).text, 'html.parser').find("tbody")

def _get_pnumb_list(web_page):
    return list(map(lambda a: a["href"].split("/")[3],
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
    _bld_df_handle_pd(pd.read_html(_read_df(stat_set))[0])
    return stat_set

def _stats_and_proj_bypos(position):
    return [_build_df(f"{position}/{this_year()}/season/projections"),
            _build_df(f"{position}/{last_year()}/season/stats")]

def stats_and_proj():
    """
    Generate the spreadsheets for each position's statistics from last year
    and projected statistics for this year
    """
    return list(map(_stats_and_proj_bypos,
                    ['C', '1B', '2B', 'SS', '3B', 'OF', 'U', 'SP', 'RP']))

if __name__ == "__main__":
    if len(stats_and_proj()) != 9:
        print("Potential Problem")
