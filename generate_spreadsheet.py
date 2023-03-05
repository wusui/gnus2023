# Copyright (C) 2023 Warren Usui, MIT License
"""
Generate the spreadsheet from scratch
"""
import os
from add_stats import add_stats
from common_gnus import get_sheets
from eligibility import eligibility
from gen_adjusted_stats import gen_adjusted_stats
from gnus_init_cols import gnus_init_cols
from stats_and_proj import stats_and_proj
from talking_heads_rankings import talking_heads_rankings

def _deleter(xlsx_file):
    if xlsx_file == "gnu_adjusted_stats.xlsx":
        return
    os.remove(xlsx_file)

def _cleanup():
    list(map(_deleter, get_sheets()))

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
    _cleanup()

if __name__ == "__main__":
    generate_spreadsheet()
