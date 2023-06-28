import sqlite3
import os
import pandas as pd
def df_leasing_payment_graph_func(data_input):
    if data_input == 'demo':
        table_name = 'leasingdemoDB'
        SQLITE_URL = os.environ["SQLITE_URL"]

        conn = sqlite3.connect(SQLITE_URL)
        cur = conn.cursor()
        query = "SELECT * FROM leasingdemoDB;"
        df = pd.read_sql(query, conn)
        df.sort_values(by="date", inplace=True)

        # df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'], format='%d.%m.%Y %H:%M:%S')
        df['date'] = pd.to_datetime(df['date'])

        df['month_first_date'] = (df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))
        df_groupped = df.groupby(['month_first_date','year', 'current_agreement_status'], as_index=False).agg(
            {'payment_amount': 'sum'})
        cur.close()
        conn.close()

        return df_groupped
