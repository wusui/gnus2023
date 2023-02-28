# Copyright (C) 2023 Warren Usui, MIT License
"""
Get CBS player positions
"""
import datetime
#import json
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

#def _pos_eligibility(position):
#    if position.endswith('P'):
#        return []
#    return [position, _get_pnumb_list(_get_current_page(
#`                    position))]

#def positions_info():
#    """
#    Return a dict of eligible player IDs indexed by position
#    """
#    return dict(list(filter(lambda a: len(a) > 0,
#                            _check_all_pos(_pos_eligibility))))

def _build_df(test_stats):
    print(test_stats)
    #test_stats = _get_current_page('RP')
    df = pd.read_html("".join([_rootdir(), test_stats]))[0]
    pnlist = _get_pnumb_list(test_stats)
    if test_stats[1] == 'P':
        df1 = df.iloc[:, [3, 5, 10, 11, 13, 14, 17]]
    else:
        df1 = df.iloc[:, [5, 6, 7, 11, 12, 20]]
    df2 = df1.rename(index=dict(zip(
        list(range(len(df1.index))), pnlist)))
    df2.to_excel("_".join(test_stats.split('/')[0:2]) + ".xlsx")
    return test_stats

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
    #with open("player_pos.json", "w", encoding='utf8') as outfile:
    #    outfile.write(json.dumps(positions_info(), indent=4,
    #                             ensure_ascii=False))
    if len(gen_spreadsheets()) != 9:
        print("Potential Problem")
