# Copyright (C) 2023 Warren Usui, MIT License
"""
Add all and best 4 rankings to spreadsheet
"""
import itertools
import pandas as pd

def _stype(numb):
    return ["Projected", "Last_Year"][numb // 4 % 2]

def _ptype(numb):
    return ["Batter", "Pitcher"][numb // 2 % 2]

def _rtype(numb):
    return ["All", "Top_4"][numb % 2]

def _make_all_ranks(df1):
    def _num_tot(vector):
        return [sum(vector), sum(vector) - max(vector)]

    def _stat_level(rowv):
        def _stat_level_inner(offset):
            if rowv[offset] != ' ':
                return float(rowv[offset])
            return 0
        return _stat_level_inner

    def _group_level(rowv):
        def _group_level_inner(offset):
            return _num_tot(list(map(_stat_level(rowv),
                                    list(range(offset, offset + 5)))))
        return _group_level_inner

    def _plyr_level(pnumb):
        return list(map(_group_level(df1.iloc[pnumb]), range(-20, 0, 5)))

    def _fix_ch(rvalue):
        if rvalue == 0:
            return ' '
        return str(rvalue)

    def _flatten_rows(rows):
        return pd.Series(list(map(_fix_ch, list(itertools.chain(*rows)))))

    def _genhead(hnumb):
        return [hnumb, "_".join(["Total_Rankings", f"{_stype(hnumb)}",
                         f"{_ptype(hnumb)}", f"{_rtype(hnumb)}"])]
    def _gencols():
        return dict(list(map(_genhead, list(range(8)))))

    def _gen_players():
        return list(map(_plyr_level, list(range(len(df1)))))

    def _gen_stats():
        return list(map(_flatten_rows, _gen_players()))

    def _gen_df():
        return pd.concat(_gen_stats(), axis=1).transpose()

    def _gen_full_df():
        return pd.concat([df1, _gen_df()], axis=1)

    _gen_full_df().rename(columns=_gencols()).to_excel("total_rankings.xlsx")

def make_all_ranks():
    """
    Using comparative_ranks.xlsx, generate total_rankings.xlsx
    """
    _make_all_ranks(pd.read_excel("comparative_ranks.xlsx"))

if __name__ == "__main__":
    make_all_ranks()
