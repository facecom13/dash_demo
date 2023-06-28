from sqlalchemy import create_engine
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
def reload_leasing_tables_func(data_input):
    output = []
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine('url_db', pool_recycle=3600)

        # try:
        #     with engine.connect() as con:
        #         query = 'DELETE FROM "leasingDB";'
        #         r_set_delete = con.execute(query)
        # except Exception as delete_rows_error:
        #     return f"не удалось удалить строки в таблице leasingDB: {delete_rows_error}"

        try:
            def drop_table(table_name, engine=engine):
                Base = declarative_base()
                metadata = MetaData()
                metadata.reflect(bind=engine)
                table = metadata.tables[table_name]
                if table is not None:
                    Base.metadata.drop_all(engine, [table], checkfirst=True)

            drop_table('leasing_db')
            output.append('leasing_DB удален')
        except Exception as delete_error:
            output.append(f"не удалось удалить таблицу leasing_DB: {delete_error}")


        ##########копируем из leasing_DB
        # copy_query = 'INSERT INTO "leasingDB" SELECT * FROM "leasing_temp_DB" ;'
        copy_query = 'CREATE TABLE leasingdb SELECT * FROM "leasing_temp_DB";'
        try:
            with engine.connect() as con:
                con.execute(copy_query)
                output.append('таблица копирована')
        except Exception as insert_rows_error:
            return f"не удалось вставить строки в таблице leasingDB: {insert_rows_error}"


        return str(output)