import datetime
from dash import html
from dash import dash_table
import os
from sqlalchemy import create_engine
import pandas as pd
import math
import numpy as np


def rd(x, y=3):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m


def credit_limit_remain_by_today_content_func(free_remaining):
    today = datetime.datetime.now()
    total_credit_limit = ""
    remaining_volume_output = "-"
    credit_limit_check_list = []
    credit_limit_check_ = html.Div(
        children=credit_limit_check_list
    )
    remaining_volume_rounded = ""


    full_credit_line_types = ['Возобновляемая', 'Не возобновляемая']


    if free_remaining:

        freelimitremainings_ = rd(free_remaining / 1000000000)

        remaining_volume_output = format(freelimitremainings_, '.3f')



    else:
        remaining_volume_output = html.P("-")
        total_credit_limit = html.P("-")


    return remaining_volume_output
