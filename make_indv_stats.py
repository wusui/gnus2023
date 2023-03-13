# Copyright (C) 2023 Warren Usui, MIT License
"""
Generate Projected and Last Year tables for both batters and pitchers
"""
import os
import json
import pandas as pd

def _twoway_list():
    """
    Make sure pitcher stats for two-way players are recorded.
    For the start of the 2023 season, this only applies to Shohei Ohtani.
    """
    return [2901324]
def _add_twoways2(everybody):
    def _add_twoways3(idval):
        return everybody.loc[everybody['ID'] == idval]
    return pd.concat(list(map(_add_twoways3, _twoway_list())))
def _add_twoways(other_players):
    return pd.concat([other_players,
            _add_twoways2(pd.read_excel("gnu_adjusted_stats.xlsx"))])

def _mk_comp(all_data):
    return [_add_twoways(all_data.loc[all_data['position'] == 'P']),
            all_data.loc[all_data['position'] != 'P']]

def _make_two_dfs():
    return _mk_comp(pd.read_excel("gnu_adjusted_stats.xlsx"))

def _plyr_tables(pos_tables):
    return [
            pos_tables[0].loc[pos_tables[0]['Projected_Wins'] != ' '],
            pos_tables[0].loc[pos_tables[0]['Last_Year_Wins'] != ' '],
            pos_tables[1].loc[pos_tables[1]['Projected_Hits'] != ' '],
            pos_tables[1].loc[pos_tables[1]['Last_Year_Hits'] != ' ']]

def _mk_dict(id_lists):
    return dict([["Projected_P", id_lists[0]],
                ["Last_Year_P", id_lists[1]],
                ["Projected_B", id_lists[2]],
                ["Last_Year_B", id_lists[3]]])

def _make_json(out_data):
    with open("player_groups.json", "w", encoding='utf8') as outfile:
        outfile.write(json.dumps(out_data, indent=4, ensure_ascii=False))

def _make_indv_lists():
    return _mk_dict(list(map(lambda a: list(a.iloc[:, 0]),
                        _plyr_tables(_make_two_dfs()))))

def make_json():
    """
    Collect four lists of IDs for Projected Pitcher stats, Last Year
    Pitcher stats, Projected Batter stats, and Last Year Batter Stats
    """
    _make_json(_make_indv_lists())

def _process_all_stats(players):
    def _pbs_inner(bpdata):
        def _handle_bats(bptype):
            def _get_fields(bptype):
                if bptype.endswith("P"):
                    return [[f"{bptype[0:-2]}_Wins", False],
                            [f"{bptype[0:-2]}_Saves", False],
                            [f"Gnu_{bptype[0:-2]}_ERA", True],
                            [f"Gnu_{bptype[0:-2]}_Whip", True],
                            [f"Gnu_{bptype[0:-2]}_Ks_per_9", False]]
                return [[f"Gnu_{bptype[0:-2]}_Batting_Avg",False],
                        [f"{bptype[0:-2]}_Runs", False],
                        [f"{bptype[0:-2]}_Home_Runs", False],
                        [f"{bptype[0:-2]}_Runs_Batted_In", False],
                        [f"{bptype[0:-2]}_Stolen_Bases", False]]
            def _indv_stat(stat_name):
                def _getpset():
                    return bpdata.loc[bpdata['ID'].isin(players[bptype])]
                def _fix_nonum(chkfld):
                    def _fix_nonum_inner(indx):
                        if chkfld.iloc[indx].replace('.','',1).isdigit():
                            return chkfld.iloc[indx]
                        return '0'
                    return _fix_nonum_inner
                def _getlist1():
                    return _getpset()[['name', stat_name[0]]].copy(
                         ).reset_index(drop=True)
                def _series1():
                    return _getlist1()[stat_name[0]]
                def _series2():
                    return list(map(_fix_nonum(_series1()),
                                      range(len(_series1()))))
                def _series3():
                    return pd.Series(_series2(),
                                     name=stat_name[0]).astype(float)
                def _getplid():
                    return _getpset()[['ID', 'name']].copy(
                           ).reset_index(drop=True)
                def _unsorted():
                    return pd.concat([_getplid(), _series3()], axis=1)
                def _sorted():
                    return _unsorted().sort_values(by=[stat_name[0]],
                           ascending=stat_name[1])
                _sorted().to_excel(os.sep.join(["indv_stats",
                                    ".".join([stat_name[0], "xlsx"])]))
            list(map(_indv_stat, _get_fields(bptype)))
        _handle_bats('Projected_P')
        _handle_bats('Projected_B')
        _handle_bats('Last_Year_P')
        _handle_bats('Last_Year_B')
    return _pbs_inner

def make_indv_stats():
    """
    Generate sorted list for each statistic.  Save in indv_stats
    """
    if not os.path.exists('indv_stats'):
        os.mkdir('indv_stats')
    _process_all_stats(_make_indv_lists())(pd.read_excel(
                        "gnu_adjusted_stats.xlsx"))

if __name__ == "__main__":
    make_indv_stats()
