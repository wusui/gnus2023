# Copyright (C) 2023 Warren Usui, MIT License
"""
Compare computed values with suggested prices
"""
import os
import pandas as pd

def _get_col_info(header_part):
    return [f"Total_Rankings_{header_part}_All",
            f"Total_Rankings_{header_part}_Top_4", "Simulation"]

def _get_columns(xlsx_file):
    return _get_col_info(xlsx_file.split(".")[0])

def _make_series(headers):
    def _gen_series(evalues):
        return pd.Series(evalues[1], name="_".join(
                    ["Price_Rating", headers[evalues[0]]]))
    def _ms_inner(values):
        return list(map(_gen_series, enumerate(values)))
    return _ms_inner

def _handle_files(xlsx_file):
    def _gen_price_ranks(d_frame):
        def _gpr_ind(col_head):
            def _foo(iloc_val):
                def _bar(iloc_chkr):
                    if iloc_val == iloc_chkr:
                        return 0
                    if (d_frame.iloc[iloc_val][col_head] ==
                                    d_frame.iloc[iloc_chkr][col_head]):
                        return 0
                    if (d_frame.iloc[iloc_val][col_head] <
                                    d_frame.iloc[iloc_chkr][col_head]):
                        if col_head.startswith("Total"):
                            if (d_frame.iloc[iloc_chkr]['avg_value']
                                     >= d_frame.iloc[iloc_val]['avg_value']):
                                return 1
                    else:
                        if col_head == "Simulation":
                            if (d_frame.iloc[iloc_chkr]['avg_value']
                                     >= d_frame.iloc[iloc_val]['avg_value']):
                                return 1
                    if (d_frame.iloc[iloc_chkr]['avg_value']
                                    <= d_frame.iloc[iloc_val]['avg_value']):
                        return -1
                    return 0
                return sum(list(map(_bar, range(len(d_frame)))))
            return list(map(_foo, range(len(d_frame))))
        def fnumbers():
            return list(map(_gpr_ind, _get_columns(xlsx_file)))
        return _make_series(_get_columns(xlsx_file))(fnumbers())
    def out_df():
        return pd.read_excel(os.sep.join(["simulation", xlsx_file]))
    def out_cols():
        return _gen_price_ranks(out_df())
    def out_info1():
        return pd.concat(out_cols(), axis=1)
    def out_pd():
        return pd.concat([out_df(), out_info1()], axis=1)
    return out_pd().to_excel(os.sep.join(['price_ranking', xlsx_file]))

def price_ranking():
    """
    Mkdir.  _handle_files does the bulk of the work here.
    """
    if not os.path.exists('price_ranking'):
        os.mkdir('price_ranking')
    return list(map(_handle_files, os.listdir("simulation")))

if __name__ == "__main__":
    price_ranking()
