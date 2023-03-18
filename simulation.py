# Copyright (C) 2023 Warren Usui, MIT License
"""
Get Simulated values
"""
import os
import random
import itertools
import pandas as pd
import numpy as np

def _sw_ptype(stype):
    return [[stype, "Batter"], [stype, "Pitcher"]]

def _sw_stype():
    return list(map(_sw_ptype, ['Last_Year', 'Projected']))

def _get_split_info():
    return list(itertools.chain(*_sw_stype()))

def _make_int(value):
    if isinstance(value, (int, np.int64)):
        return value
    if value.isdigit():
        return int(value)
    return 0

def _tsize(stat_list):
    if stat_list[0].endswith("Wins"):
        return 9
    return 14

def _gen_sim_stats(d_frame):
    def _gss_inner(stat_list):
        def _gen_sim_teams(tsize):
            def _get_a_stat(rindex):
                def _get_a_stat_inner(statname):
                    return _make_int(d_frame.iloc[rindex][statname])
                return _get_a_stat_inner
            def _get_stat_set(rindex):
                return list(map(_get_a_stat(rindex), stat_list))
            def _gsim_inner(_):
                def _get_rand_plyrs():
                    return list(map(lambda a: random.randrange(
                                len(d_frame.index)), list(range(tsize))))
                def _get_sim():
                    return list(map(_get_stat_set, _get_rand_plyrs()))
                return list(map(sum, list(zip(*_get_sim()))))
            return _gsim_inner
        return list(map(_gen_sim_teams(_tsize(stat_list)), range(100)))
    random.seed()
    return _gss_inner

def _read_xlsx(sinfo):
    return pd.read_excel(os.sep.join(['split_stats',
                        f'{sinfo[0]}_{sinfo[1]}.xlsx']))

def _get_slist(stat_info):
    if stat_info[1].startswith("Batter"):
        return [f'{stat_info[0]}_At_Bats', f'{stat_info[0]}_Runs',
                f'{stat_info[0]}_Hits', f'{stat_info[0]}_Home_Runs',
                f'{stat_info[0]}_Runs_Batted_In',
                f'{stat_info[0]}_Stolen_Bases']
    return [f'{stat_info[0]}_Wins', f'{stat_info[0]}_Strikeouts',
            f'{stat_info[0]}_Saves', f'Gnu_{stat_info[0]}_outs',
            f'Gnu_{stat_info[0]}_wh', f'Gnu_{stat_info[0]}_er']

def _st_math(sinfo):
    if sinfo[1].startswith('Batter'):
        return [[1], [3], [4], [5], [2, 0]]
    return [[0], [2], [1, 3], [4, 3], [5, 3]]

def _simulation(sinfo):
    def _sim_with_df(d_frame):
        def _chk_indv(s_teams):
            def _chk_indv_inner(plyr):
                def _chk_vs_vteams(one_team):
                    def _chk_vs_oteams(other_team):
                        def _eval_diff(math_vars):
                            def _addup(list1):
                                def _addup_inner(list2):
                                    return list1[list2[0]] + list2[1]
                                return _addup_inner
                            if one_team == other_team:
                                return 0
                            stat_list = _get_slist(sinfo)
                            tsize = _tsize(stat_list)
                            other_stat = list(map(lambda a: other_team[a],
                                                math_vars))
                            orig_stat = list(map(lambda a: one_team[a],
                                                math_vars))
                            pstat = list(map(lambda a: plyr[stat_list[a]],
                                                math_vars))
                            pstat = list(map(_make_int, pstat))
                            adj1 = list(map(lambda a: a * (tsize - 1),
                                                orig_stat))
                            adj2 = list(map(lambda a: a / tsize, adj1))
                            padj = list(map(_addup(adj2), enumerate(pstat)))
                            oval = other_stat[0]
                            pval = padj[0]
                            sval = orig_stat[0]
                            if len(other_stat) == 2:
                                oval = other_stat[0] / other_stat[1]
                                pval = padj[0] / padj[1]
                                sval = orig_stat[0] / orig_stat[1]
                            factor = 0
                            if oval in (pval, sval):
                                factor = .5
                            if oval < max([pval, sval]):
                                if oval > min([pval, sval]):
                                    factor = 1
                            if pval < sval:
                                factor = 0 - factor
                            if math_vars in ([4, 3], [5, 3]):
                                factor = 0 - factor
                            return factor
                        return sum(list(map(_eval_diff, _st_math(sinfo))))
                    return sum(list(map(_chk_vs_oteams, s_teams)))
                return sum(list(map(_chk_vs_vteams, s_teams)))
            return _chk_indv_inner
        sim_tms = _gen_sim_stats(d_frame)(_get_slist(sinfo))
        answer = list(map(_chk_indv(sim_tms), list(d_frame.iloc)))
        xxx = pd.Series(answer, name="Simulation")
        xxf = pd.concat([d_frame, xxx], axis=1)
        xxf.to_excel(os.sep.join(["simulation",
                                  "_".join(sinfo) + ".xlsx"]), index=False)
        return answer
    return _sim_with_df(_read_xlsx(sinfo))

def simulation():
    """
    Create directory and do the bulk of the work in _simulation
    """
    if not os.path.exists('simulation'):
        os.mkdir('simulation')
    return list(map(_simulation, _get_split_info()))

if __name__ == "__main__":
    simulation()
