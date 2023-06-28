import datetime
import pandas as pd
def report_date_borders(df, report_initial_date_status, year_filter_list, quarter_filter_list, month_filter_list):
    """report_initial_date_status - today or 2023_first_date"""
    first_day_ref = datetime.datetime(2023, 1, 1)
    if report_initial_date_status == "today":
        first_day_ref = datetime.datetime.now()


    # режем
    df = df.loc[df['year'].isin(year_filter_list)]
    df = df.loc[df['quarter'].isin(quarter_filter_list)]
    df = df.loc[df['month'].isin(month_filter_list)]

    first_date = df.iloc[0, df.columns.get_loc("date")]
    last_date = df.iloc[-1, df.columns.get_loc("date")]

    # print("first_date: ", first_date)

    if first_day_ref >= first_date and first_day_ref <= last_date:
        first_date = first_day_ref
    # print("first_date_last: ", first_date)

    return first_date, last_date


