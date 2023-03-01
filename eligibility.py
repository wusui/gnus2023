# Copyright (C) 2023 Warren Usui, MIT License
"""
Get CBS player positions
"""
import os
import itertools
import pandas as pd

def _get_sheets():
    return list(filter(lambda a: a.endswith(".xlsx"), os.listdir()))

def _read_sheets():
    return dict(list(map(lambda a: [a.split('.')[0], pd.read_excel(a)],
                         _get_sheets())))

def _main_head_info(head_info):
    def _person(value_keys):
        def _person_inner(plyr_numb):
            def _position(plyr_numb):
                def _position_inner(v_key):
                    def _get_indx(in_val):
                        if in_val.split("_")[-1] == \
                                list(value_keys[0].keys())[0].split("_")[-1]:
                            return 0
                        return 1
                    if plyr_numb in value_keys[_get_indx(v_key)][v_key]:
                        return v_key
                    return ''
                return _position_inner
            return list(map(_position(plyr_numb), list(value_keys[0]))) + \
                    list(map(_position(plyr_numb), list(value_keys[1])))
        return _person_inner
    def _set_elg_values(value_keys):
        return list(map(lambda a: list(filter(None, a)),
                        list(map(_person(value_keys),
                        head_info.iloc[:, 0].tolist()))))
    def _check_pos(pos_list):
        def _set_pos_list(pos_name):
            return [pos_name, pos_list[pos_name].iloc[:, 0].tolist()]
        def _check_pos_inner(start_pt):
            return dict(list(map(_set_pos_list,
                                 list(pos_list.keys())[start_pt::2])))
        return _check_pos_inner
    def _checkv_pos_key(dkey):
        if dkey[1] == 'P' or dkey[0] in 'tU':
            return False
        return True
    def _pull_not_right(df_dict):
        return dict(list(map(lambda a: [a, df_dict[a]],
                   list(filter(_checkv_pos_key, df_dict.keys())))))
    def _fmt_eligibility_info(pos_list):
        return [_check_pos(pos_list)(0), _check_pos(pos_list)(1)]
    return _set_elg_values(_fmt_eligibility_info(
            _pull_not_right(_read_sheets())))

def _get_pos_columns():
    return _main_head_info(pd.read_excel('thead_data.xlsx'))

def _get_yrange(pos_info):
    return sorted(set(list(map(lambda a: a.split('_')[-1],
                                list(itertools.chain(*pos_info))))))

def _gen_elig_cols(pos_info):
    def _elg_header(indx):
        return ["Positions Last Year", "Projected This Year"][indx]
    def _gen_series(series_pos):
        return pd.Series(series_pos[1], name=_elg_header(series_pos[0]))
    def _gen_col(cyear):
        def _person(ppos):
            def _position(apos):
                if apos.endswith(cyear):
                    return True
                return False
            return ", ".join(list(map(lambda a: a.split('_')[0],
                                       list(filter(_position, ppos)))))
        return list(map(_person, pos_info))
    return list(map(_gen_series, enumerate(
                list(map(_gen_col, _get_yrange(pos_info))))))

def _add_elg_cols(col_info):
    pd.concat([pd.read_excel("thead_data.xlsx"),
               col_info[0], col_info[1]], axis=1).to_excel("with_elig.xlsx")

def add_eligibility():
    """
    Add position eligibility columns (last year's stats, this year's
    projected positions)
    """
    _add_elg_cols(_gen_elig_cols(_get_pos_columns()))

if __name__ == "__main__":
    add_eligibility()
