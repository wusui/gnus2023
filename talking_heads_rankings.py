# Copyright (C) 2023 Warren Usui, MIT License
"""
Get CBS rankings from website (three pickers)
"""
from functools import reduce
import requests
from bs4 import BeautifulSoup
import pandas as pd

def _get_bs_info():
    return BeautifulSoup(requests.get(
        "https://www.cbssports.com/fantasy/baseball/rankings/roto/top300/AL/",
        timeout=600).text, 'html.parser').find_all(
        "div", class_="player-row")

def _parse_plyr(pinfo):
    def _pinfo_inner(indx):
        return [indx, pinfo[indx].find("a", href=True)["href"],
                pinfo[indx].find("span",
                        class_="team position").contents[0].strip().split()]
    return _pinfo_inner

def _dictify(exp_value):
    return [f"{exp_value[1]}+{exp_value[0]}", exp_value[2]]

def _iterate_pentries():
    return list(map(_parse_plyr(_get_bs_info()), range(900)))

def _raw_dict():
    return dict(list(map(_dictify, _iterate_pentries())))

def _thr_rtn(raw_data):
    def _reorganize(accum, new_line):
        def _sub_reorg(indx):
            if indx not in accum:
                return accum | {indx: [raw_data[new_line]]}
            return accum | {indx: accum[indx] + [raw_data[new_line]]}
        return _sub_reorg(new_line.split('+')[0])
    return reduce(_reorganize, sorted(raw_data), {})

def _namify(istring):
    return " ".join(list(map(lambda a: a.capitalize(), istring.split("-"))))

def _mny_fmt(in_data):
    return f'{in_data:.2f}'

def _average_val(cost_data):
    return _mny_fmt(sum(list(map(lambda a: int(a[-1][1:]) / 3, cost_data))))

def _gen_pos(position):
    if position.endswith('F'):
        return 'OF'
    if position.endswith('P'):
        return 'P'
    return position

def _gen_player_record(pdata):
    return [pdata[0].split('/')[-4], {
        "name": _namify(pdata[0].split('/')[-3]),
        "team": pdata[1][0][0],
        "position": _gen_pos(pdata[1][0][1]),
        "avg_value": _average_val(pdata[1]),
        "priced_picks": sum(list(map(lambda a: a[2] != "$0", pdata[1]))),
        "total_picks": len(pdata[1])
    }]

def _th_format(in_data):
    def _th_format_inner(player):
        return _gen_player_record([player, in_data[player]])
    return list(map(_th_format_inner, in_data.keys()))

def _thead_rankings():
    return dict(_th_format(_thr_rtn(_raw_dict())))

def talking_heads_rankings():
    """
    Return a spreadsheet indexed by player id of CBS sports monetary values
    for each player as evaluated by three commentators.
    """
    pd.DataFrame(_thead_rankings()).transpose().to_excel(
        "thead_data.xlsx", sheet_name="Sheet", index=True)

if __name__ == "__main__":
    talking_heads_rankings()
