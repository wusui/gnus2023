# Copyright (C) 2023 Warren Usui, MIT License
"""
Generate ranked_stats tables (ordinal values of a player's stat among
all players in the spreadsheet)
"""
import os
import pandas as pd

def _mark_info(list_of_values):
    def _mrk_inner(indx):
        if list_of_values[indx] == list_of_values[indx + 1]:
            return indx + 1
        return 0
    return list(map(_mrk_inner, range(len(list_of_values) - 1))) + [0]

def _find_starts(list_of_values):
    def _strt_filt(location):
        if list_of_values[location] == 0 and list_of_values[location + 1] > 0:
            return True
        return False
    return list(filter(_strt_filt, range(0, len(list_of_values) - 1)))

def _find_ends(list_of_values):
    def _end_filt(location):
        if list_of_values[location - 1] > 0 and list_of_values[location] == 0:
            return True
        return False
    return list(filter(_end_filt, range(1, len(list_of_values))))

def _get_endpoints(lfunc):
    def _get_epoints_inner(list_of_values):
        return list(map(lambda a: a + 1, lfunc(list_of_values)))
    return _get_epoints_inner

def _handle_ranges(lsize):
    def _do_one_range(rnge):
        def _do_one_range_inner(indx):
            if indx in rnge:
                return sum(rnge) / len(rnge) + 1
            return 0
        return _do_one_range_inner
    def _handle_ranges_inner(rnge):
        return list(map(_do_one_range(list(range(rnge[0], rnge[1]))),
                        range(lsize)))
    return _handle_ranges_inner

def _add_indv(hties):
    def _add_indv_inner(indx):
        if hties[indx] == 0:
            return indx + 1
        return hties[indx]
    return _add_indv_inner

def _eval_info(list_of_values):
    def _full_length(hties):
        if not hties:
            return list_of_values
        return hties
    def _dists():
        return list(zip(_get_endpoints(_find_starts)(list_of_values),
                        _get_endpoints(_find_ends)(list_of_values)))
    def set_tie_inds(list_of_lists):
        return _full_length(list(map(sum, zip(*list_of_lists))))
    def collect_tie_inds():
        return set_tie_inds(list(map(_handle_ranges(len(list_of_values)),
                                     _dists())))
    return list(map(_add_indv(collect_tie_inds()),
                    list(range(len(list_of_values)))))

def _get_values_in_table(this_table):
    return [_eval_info(_mark_info(this_table[list(this_table.columns)[-1]
                                 ].values.tolist())), this_table]

def _get_ranking_table(test_table):
    return _get_values_in_table(pd.read_excel(test_table))

def _xlsx_to_col_head(xls_name):
    return "_".join(["Ranking", xls_name.split(os.sep)[-1].split('.')[0]])

def _make_ranked_xlsx(file_name):
    def _mk_ranked_1(test_table):
        def _mk_ranked_2(rankings):
            def _mk_ranked_3(series1):
                return pd.concat([rankings[1], series1], axis=1).to_excel(
                    os.sep.join(["ranked_stats",
                                 "_".join(["Ranking", file_name])]))
            return _mk_ranked_3(pd.Series(rankings[0],
                                name=_xlsx_to_col_head(test_table)))
        return _mk_ranked_2(_get_ranking_table(test_table))
    return _mk_ranked_1(os.sep.join(["indv_stats", file_name]))

def make_ranked_stats():
    """
    There should be a one to one correspondence between files in
    indv_stats and files in ranked_stats
    """
    if not os.path.exists('ranked_stats'):
        os.mkdir('ranked_stats')
    list(map(_make_ranked_xlsx, os.listdir('indv_stats')))

if __name__ == "__main__":
    make_ranked_stats()
