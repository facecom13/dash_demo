import datetime
import pandas as pd
def calendar_store_data_func(calendar_start_date, calendar_finish_date):

    first_date = calendar_start_date
    last_date = calendar_finish_date
    temp_date = first_date
    result_df_list = []
    while temp_date < last_date:
        temp_dict = {}
        temp_dict['date'] = temp_date
        temp_dict['year'] = temp_date.year
        temp_dict['quarter'] = pd.Timestamp(temp_date).quarter
        temp_dict['month'] = temp_date.month
        temp_date = temp_date + datetime.timedelta(days=1)
        result_df_list.append(temp_dict)
    df = pd.DataFrame(result_df_list)
    return df