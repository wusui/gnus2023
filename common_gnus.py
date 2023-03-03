# Copyright (C) 2023 Warren Usui, MIT License
"""
Common code used by Darren Lewis and the Gnus
"""
import os
import datetime
import pandas as pd

def get_sheets():
    """
    Find all xlsx files
    """
    return list(filter(lambda a: a.endswith(".xlsx"), os.listdir()))

def read_sheets():
    """
    Find all xlsx files and load the DataFrames into a dictionary indexed
    by file name
    """
    return dict(list(map(lambda a: [a.split('.')[0], pd.read_excel(a)],
                         get_sheets())))

def this_year():
    """
    Get current year
    """
    return datetime.date.today().year

def last_year():
    """
    Get previous year
    """
    return this_year() - 1
