import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd

def credit_tab_quarter_select_options_func(data_input):

    quarter_list = [1,2,3,4]


    options_dict = {}
    for quarter in quarter_list:
        options_dict[quarter] = quarter
    options = options_dict

    return options
