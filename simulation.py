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

def _set_up_val(inlist):
    if len(inlist) == 2:
        return inlist[0] / inlist[1]
    return inlist[0]

def _calc_factors(parms):
    def _set_factor_1():
        if parms['o'] in (parms['p'], parms['s']):
            return .5
        return 0
    def _set_factor_2(ifactor):
        if parms['o'] < max([parms['p'], parms['s']]):
            if parms['o'] > min([parms['p'], parms['s']]):
                return 1
        return ifactor
    def _set_factor_3(ifactor):
        if parms['p'] < parms['s']:
            return 0 - ifactor
        return ifactor
    def _set_factor_4(ifactor):
        if parms['p'] < parms['s']:
            return 0 - ifactor
        return ifactor
    def _set_factor_5(ifactor):
        if parms['m'] in ([4, 3], [5, 3]):
            return 0 - ifactor
        return ifactor
    return _set_factor_5(_set_factor_4(_set_factor_3(_set_factor_2(
                        _set_factor_1()))))

def _factor_calc(sinfo):
    def _fc_lev1(plyr):
        def _fc_lev2(one_team):
            def _fc_lev3(other_team):
                def _fc_lev4(math_vars):
                    def _addup(list1):
                        def _addup_inner(list2):
                            return list1[list2[0]] + list2[1]
                        return _addup_inner
                    def _set_ltsize(ltsize):
                        def _set_othr_stat(othr_stat):
                            def _set_orig_stat(orig_stat):
                                def _set_pstat(pstat):
                                    def adj1():
                                        return list(map(lambda a:
                                                a * (ltsize - 1),
                                                orig_stat))
                                    def adj2():
                                        return list(map(lambda a: a / ltsize,
                                                adj1()))
                                    def _set_padj_stat(padj_stat):
                                        if one_team == other_team:
                                            return 0
                                        return _calc_factors({
                                                "p": _set_up_val(padj_stat),
                                                "o": _set_up_val(othr_stat),
                                                "s": _set_up_val(orig_stat),
                                                "m": math_vars})
                                    return _set_padj_stat(
                                                    list(map(_addup(adj2()),
                                                    pstat)))
                                return _set_pstat(enumerate(list(map(_make_int,
                                                list(map(lambda a:
                                                plyr[_get_slist(sinfo)[a]],
                                                math_vars))))))
                            return _set_orig_stat(
                                    list(map(lambda a: one_team[a],math_vars)))
                        return _set_othr_stat(list(map(lambda a: other_team[a],
                                                       math_vars)))
                    return _set_ltsize(_tsize(_get_slist(sinfo)))
                return _fc_lev4
            return _fc_lev3
        return _fc_lev2
    return _fc_lev1

def _simulation(sinfo):
    def _sim_with_df(d_frame):
        def _chk_indv(s_teams):
            def _chk_indv_inner(plyr):
                def _chk_vs_vteams(one_team):
                    def _chk_vs_oteams(other_team):
                        def _eval_diff(math_vars):
                            return _factor_calc(sinfo)(plyr)(one_team)(
                                                other_team)(math_vars)
                        return sum(list(map(_eval_diff, _st_math(sinfo))))
                    return sum(list(map(_chk_vs_oteams, s_teams)))
                return sum(list(map(_chk_vs_vteams, s_teams)))
            return _chk_indv_inner
        def _get_sim_tms():
            return _gen_sim_stats(d_frame)(_get_slist(sinfo))
        def _get_answer():
            return list(map(_chk_indv(_get_sim_tms()), list(d_frame.iloc)))
        def _get_sim_col():
            return pd.Series(_get_answer(), name="Simulation")
        def _get_sim_frame():
            return pd.concat([d_frame, _get_sim_col()], axis=1)
        _get_sim_frame().to_excel(os.sep.join(["simulation",
                                  "_".join(sinfo) + ".xlsx"]), index=False)
        return _get_answer()
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
