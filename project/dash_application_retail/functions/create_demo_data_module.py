from pathlib import Path
import pandas as pd
import os
from sqlalchemy import create_engine

def create_demo_data_func():
    url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
    engine = create_engine(url_db, pool_recycle=3600)
    project_folder = Path(__file__).resolve().parent.parent.parent
    transhes_and_limits_csv = str(project_folder) + '/datafiles/transhes_and_limits.csv'
    df_transhes_and_limits = pd.read_csv(transhes_and_limits_csv,
                                         parse_dates=['datetime',
                                                      'date',
                                                      'agreement_start_datetime',
                                                      'ral_credit_transh_getting_deadline',
                                                      'limitdeadline',

                                                      ])

    df_transhes_and_limits['date'] = df_transhes_and_limits['date'].dt.date

    if_exists = 'replace'
    with engine.connect() as con:
        df_transhes_and_limits.to_sql(
            name='transhes_and_limits',
            con=con,
            # chunksize=1000,
            # method='multi',
            index=False,
            if_exists=if_exists
        )

    retail_csv = str(project_folder) + '/datafiles/retail.csv'
    df_retail = pd.read_csv(retail_csv,
                                         parse_dates=['credit_tranch_date',
                                                      'date',
                                                      'limitdeadline',
                                                      'ral_credit_transh_getting_deadline',
                                                      'month_first_date'

                                                      ]
                                         )

    if_exists = 'replace'
    with engine.connect() as con:
        df_retail.to_sql(
            name='retail',
            con=con,
            # chunksize=1000,
            # method='multi',
            index=False,
            if_exists=if_exists
        )





    return str(['transhes_and_limits'])
