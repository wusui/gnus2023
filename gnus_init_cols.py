# Copyright (C) 2023 Warren Usui, MIT License
"""
Calculate Gnu statistics from the extracted data
"""
import pandas as pd

def _gnus_init_cols(df_stats):
    def _assign_kwargs():
        return {'Gnu_Projected_outs':
            _gen_gnu_column(['Projected', _ip_math]),
            'Gnu_Last_Year_outs':
            _gen_gnu_column(['Last_Year', _ip_math]),
            'Gnu_Projected_wh':
            _gen_gnu_column(['Projected', _wh_math]),
            'Gnu_Last_Year_wh':
            _gen_gnu_column(['Last_Year', _wh_math]),
            'Gnu_Projected_er':
            _gen_gnu_column(['Projected', _er_math]),
            'Gnu_Last_Year_er':
            _gen_gnu_column(['Last_Year', _er_math])}
    def _er_math(ykey):
        def _er_math_inner(indx):
            def _era(indx):
                return df_stats["_".join(
                    [ykey, "Earned_Run_Average"])][indx]
            if _era(indx) == ' ':
                return ' '
            return int((float(_era(indx)) * int(_ip_math(
                ykey)(indx)) / 27) + .1)
        return _er_math_inner
    def _wh_math(ykey):
        def _wh_math_inner(indx):
            if df_stats[
                    "_".join([ykey,
                        "Hits_Allowed"])][indx] == ' ':
                return ' '
            return str(
                int(df_stats["_".join([ykey,
                        "Hits_Allowed"])][indx]) +
                int(df_stats["_".join([ykey,
                        "Base_on_Balls_Walks"])][indx]))
        return _wh_math_inner
    def _compute_out_frac(parts):
        return str(int(parts[0]) * 3 + int(parts[1]))
    def _ip_math(ykey):
        def _ip_math_inner(indx):
            def _locv(indx):
                return df_stats["_".join(
                    [ykey, "Innings_Pitched"])][indx]
            if _locv(indx) == ' ':
                return ' '
            if '.' in _locv(indx):
                return _compute_out_frac(
                    _locv(indx).split("."))
            return str(int(_locv(indx)) * 3)
        return _ip_math_inner
    def _gen_gnu_column(stat_pkg):
        return list(map(stat_pkg[1](stat_pkg[0]),
                        range(len(df_stats))))
    pd.concat([df_stats, df_stats.assign(
        **_assign_kwargs())], axis=1).to_excel(
                "gnu_stats_included.xlsx")

def gnus_init_cols():
    """
    Add adjusted pitching stats for later calculations
    (referred to as Gnu stats)
    """
    return _gnus_init_cols(pd.read_excel(
            "extracted_data.xlsx"))

if __name__ == "__main__":
    gnus_init_cols()
