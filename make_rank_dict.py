# Copyright (C) 2023 Warren Usui, MIT License
"""
Add stat ranking columns to spreadsheet
"""
import os
import itertools
import pandas as pd
from common_gnus import get_groups, get_bat_stats, get_pit_stats

def _extract_stat(fname):
    def _extract_stat_inner(dframe):
        def _smod_fname():
            return fname.split(".")[0]
        return {_smod_fname(): dict(zip(dframe['ID'].tolist(),
                        dframe[_smod_fname()].tolist()))}
    return _extract_stat_inner

def _read_ranked_file(fname):
    return _extract_stat(fname)(pd.read_excel(os.sep.join(
                ["ranked_stats", fname])))

def _group_loop():
    def _ptype_loop(group):
        def _borp_loop(sfunc):
            def _gen_bp_stat(stat):
                return _read_ranked_file(list(filter(
                    lambda a: a.endswith("".join([group, "_", stat,
                        ".xlsx"])), os.listdir("ranked_stats")))[0])
            return list(map(_gen_bp_stat, sfunc()))
        return list(map(_borp_loop, [get_bat_stats, get_pit_stats]))
    return list(map(_ptype_loop, get_groups()))

def _make_rank_dict(big_df):
    def _mrd_inner2(indv_stats):
        def _mrd_inner3(big_list):
            def _mrd_inner4(istat):
                def plist(ival):
                    return ival[list(ival.keys())[0]]
                def _mrd_inner5(player):
                    if player in plist(istat):
                        return str(plist(istat)[player])
                    return ' '
                return pd.Series(list(map(_mrd_inner5, big_list)),
                            name=list(istat.keys())[0])
            return list(map(_mrd_inner4, list(map(
                    lambda a: indv_stats[a], range(len(indv_stats))))))
        return _mrd_inner3(big_df['ID'].tolist())
    return _mrd_inner2(list(itertools.chain(*list(itertools.chain(
            *_group_loop())))))

def _merge_all(adj_df):
    return pd.concat([adj_df, pd.concat(_make_rank_dict(adj_df),
                                        axis=1)], axis=1)

def make_rank_dict():
    """
    Output comparative ranks spreadsheet
    """
    _merge_all(pd.read_excel("gnu_adjusted_stats.xlsx")).to_excel(
                            "comparative_ranks.xlsx")

if __name__ == "__main__":
    make_rank_dict()
