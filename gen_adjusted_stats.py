# Copyright (C) 2023 Warren Usui, MIT License
"""
Calculate metrics for statistics that are ratios
(Batting Average, ERA, WHIP and K's per 9 innings
"""
import itertools
import pandas as pd
from common_gnus import get_groups

def _adj_data(group):
    return {
        "Batting_Avg": [f"{group}_Hits",
                        f"{group}_At_Bats", 1000, 4000, 1],
        "ERA": [f"Gnu_{group}_er", f"Gnu_{group}_outs",
                        500, 3000, 27],
        "Whip": [f"Gnu_{group}_wh", f"Gnu_{group}_outs",
                        1200, 3000, 3],
        "Ks_per_9": [f"{group}_Strikeouts",
                     f"Gnu_{group}_outs", 900, 3000, 27]
    }

def _gen_adjusted(orig_stats):
    def _calc_stats(group):
        def _calc_stats_inner(indx):
            def _add_to_plyr(plyr_indx):
                def _do_math(mparts):
                    return ((int(orig_stats[mparts[0]][plyr_indx]) + mparts[2])
                        / (int(orig_stats[mparts[1]][plyr_indx]) + mparts[3])
                        ) * mparts[4]
                if orig_stats[_adj_data(group)[indx][0]][plyr_indx] == ' ':
                    return ' '
                return f'{_do_math(_adj_data(group)[indx]):.6f}'
            return list(map(_add_to_plyr,
                            range(len(orig_stats))))
        return _calc_stats_inner
    def _hndl_grp(group):
        return list(map(_calc_stats(group),
                        list(_adj_data(group))))
    return list(map(_hndl_grp, get_groups()))

def _formatted(new_columns):
    def _fmt_grp_lev(group_num):
        def _fmt_stat_lev(stat_num):
            return pd.Series(new_columns[group_num][stat_num],
                             name="_".join(["Gnu",
                                    get_groups()[group_num],
                                    list(_adj_data("Protected"))[stat_num]]))
        return list(map(_fmt_stat_lev, range(len(_adj_data("Projected")))))
    return list(map(_fmt_grp_lev, range(len(get_groups()))))

def _gen_formatted_stats(orig_df):
    def _chain_stats(fmtted_stats):
        def _write_stats(one_set_of_stats):
            pd.concat([orig_df, one_set_of_stats], axis=1).to_excel(
                "gnu_adjusted_stats.xlsx", index=False)
        _write_stats(pd.concat(list(itertools.chain(*fmtted_stats)), axis=1))
    _chain_stats(_formatted(_gen_adjusted(orig_df)))

def gen_adjusted_stats():
    """
    Add normalized fractional data to the spreadsheet
    """
    _gen_formatted_stats(pd.read_excel("gnu_stats_included.xlsx"))

if __name__ == "__main__":
    gen_adjusted_stats()
