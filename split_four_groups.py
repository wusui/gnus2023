# Copyright (C) 2023 Warren Usui, MIT License
"""
Create split_stats directory
"""
import os
import itertools
import pandas as pd

def _stat_names(ptype):
    return {'Pitcher': ['Wins', 'Strikeouts', 'Saves', 'outs', 'wh', 'er'],
            'Batter': ['At_Bats', 'Runs', 'Hits', 'Home_Runs',
                        'Runs_Batted_In', 'Stolen_Bases']}[ptype]

def _stat_collector(df_data):
    def _write_sheets(info):
        def _ws_extract(wname):
            pd.DataFrame(list(map(lambda a: df_data.iloc[a], info[wname]))
                        ).to_excel(os.sep.join(['split_stats',
                                                f"{wname}.xlsx"]),
                                                index=False)
        return list(map(_ws_extract, list(info.keys())))
    def _collect_stats(stype):
        def _cs_inner(ptype):
            def _col_indx(indx):
                return f'{stype}_{_stat_names(ptype)[indx]}'
            def _cs_filter(indx):
                if df_data.iloc[indx][_col_indx(0)] == ' ':
                    return False
                return True
            return [f'{stype}_{ptype}',
                    list(filter(_cs_filter, list(range(len(df_data)))))]
        return _cs_inner

    def _loop_player_type(stype):
        return list(map(_collect_stats(stype), ["Pitcher", "Batter"]))

    def _loop_type():
        return list(map(_loop_player_type, ["Projected", "Last_Year"]))

    _write_sheets(dict(list(itertools.chain(*_loop_type()))))

def split_four_groups():
    """
    In the split_stats directory, create four spreadsheets (Projected
    Batters, Projected Pitchers, Last Year Batters, and Last Year Pitchers)
    """
    if not os.path.exists('split_stats'):
        os.mkdir('split_stats')
    _stat_collector(pd.read_excel("total_rankings.xlsx"))

if __name__ == "__main__":
    split_four_groups()
