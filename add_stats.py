# Copyright (C) 2023 Warren Usui, MIT License
"""
Get Statistics
"""
import itertools
import pandas as pd
from common_gnus import read_sheets, this_year, last_year

def _get_gen_tables(all_stats):
    def _make_stat_lines(stats_to_add):
        def _add_id_label():
            return list(map(lambda a: stats_to_add[a].rename(
                   columns={'Unnamed: 0':'ID'}), list(stats_to_add)))
        def _extract_stats(matching_df):
            if len(matching_df) == 0:
                return [' '] * (len(matching_df.columns) -1)
            return list(matching_df.iloc[0])[1:]
        def _hndl_plyr(indx):
            def _hndl_plyr_inner(stat_table_to_use):
                #print(indx)
                return _extract_stats(stat_table_to_use.loc[
                        stat_table_to_use.ID == str(indx)])
            return _hndl_plyr_inner
        def _step_through_stats(indx):
            return list(map(_hndl_plyr(indx), _add_id_label()))
        return list(map(_step_through_stats,
                        list(all_stats['with_elig'].iloc[:, 1])))
    def _make_dfs(pl_dfs):
        return [pl_dfs[0][1:], pd.concat(list(map(
                lambda a: all_stats[a], pl_dfs))).applymap(str)]
    def _get_pvsb(posind):
        def _get_pvsb_inner(dfnames):
            if (dfnames[1] == 'P') == posind:
                return False
            return dfnames
        return _get_pvsb_inner
    def _get_tlist(yearv):
        return list(filter(lambda a: a.endswith(yearv), all_stats.keys()))
    def _gen_tbls(yearv):
        return list(map(lambda a: list(filter(_get_pvsb(a),
                        _get_tlist(str(yearv)))), [False, True]))
    return _make_stat_lines(dict(list(map(_make_dfs,
                         _gen_tbls(this_year()) + _gen_tbls(last_year())))))

def _column_headers(all_stats):
    def _half_pattern():
        return [f'RP_{this_year()}', f'1B_{this_year()}']
    def _head_pattern():
        return _half_pattern() + _half_pattern()
    def _arrange_head():
        return list(map(lambda a: list(all_stats[a].keys())[1:],
                                       _head_pattern()))
    def _gen_part_head():
        return list(map(lambda a: a.replace("/", "_"),
                list(map(lambda a: "_".join(a.split()[1:]),
                list(itertools.chain(*_arrange_head()))))))
    def _add_proj_or_last_year(head_list):
        def _add_proj_or_last_year_inner(indx):
            if indx < len(head_list) / 2:
                return [indx, "_".join(["Projected", head_list[indx]])]
            return  [indx, "_".join(["Last_Year", head_list[indx]])]
        return _add_proj_or_last_year_inner
    def _col_headers(head_list):
        return list(map(_add_proj_or_last_year(head_list),
                        range(len(head_list))))
    return dict(_col_headers(_gen_part_head()))

def _write_it(df1_out):
    df1_out.to_excel('extracted_data.xlsx', index=False)

def _drop_extra(df_out):
    _write_it(df_out[df_out.columns.drop(list(df_out.filter(
        regex='Unnamed: 0')))])

def _main_adder(all_stats):
    def _mk_long_rows():
        return list(map(lambda a: list(itertools.chain(*a)),
                        _get_gen_tables(all_stats)))
    def _mk_series():
        return list(map(pd.Series, _mk_long_rows()))
    def _generate_stat_half():
        return pd.concat(_mk_series(), axis=1).transpose().rename(
                        columns=_column_headers(all_stats))
    _drop_extra(pd.concat([all_stats['with_elig'], _generate_stat_half()],
              axis=1))
    #pd.concat([all_stats['with_elig'], _generate_stat_half()],
    #          axis=1).to_excel('extracted_data.xlsx', index=False)

def add_stats():
    """
    Pass dict of all sheets that are saved locally as DataFrames
    """
    _main_adder(read_sheets())

if __name__ == "__main__":
    add_stats()
