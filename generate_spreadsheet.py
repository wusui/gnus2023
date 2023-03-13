# Copyright (C) 2023 Warren Usui, MIT License
"""
Generate the spreadsheet from scratch
"""
import os
import shutil
from add_stats import add_stats
from common_gnus import get_sheets
from eligibility import eligibility
from gen_adjusted_stats import gen_adjusted_stats
from gnus_init_cols import gnus_init_cols
from make_indv_stats import make_indv_stats
from make_ranked_stats import make_ranked_stats
from make_rank_dict import make_rank_dict
from make_all_ranks import make_all_ranks
from stats_and_proj import stats_and_proj
from talking_heads_rankings import talking_heads_rankings

def _deleter(xlsx_file):
    if xlsx_file == "total_rankings.xlsx":
        return
    os.remove(xlsx_file)

def _cleanup():
    list(map(_deleter, get_sheets()))

def _del_directory(dname):
    shutil.rmtree(os.sep.join([os.getcwd(), dname]))

def generate_spreadsheet():
    """
    Perform all spreadsheet creation tasks sequentially
    """
    talking_heads_rankings()
    stats_and_proj()
    eligibility()
    add_stats()
    gnus_init_cols()
    gen_adjusted_stats()
    make_indv_stats()
    make_ranked_stats()
    make_rank_dict()
    make_all_ranks()
    _del_directory("indv_stats")
    _del_directory("ranked_stats")
    _cleanup()

if __name__ == "__main__":
    generate_spreadsheet()
