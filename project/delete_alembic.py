from app import app
from psycopg2 import connect
# import psycopg2
# try:
#     conn = psycopg2.connect(
#         database="dash_db",
#         user='postgres',
#         password='123456',
#         host='192.168.2.91',
#         port = "5432"
#     )
#     cur = conn.cursor()
#
#     sql_query = 'DROP TABLE IF EXISTS alembic_version;'
#
#     cur.execute(sql_query)
#
#
#     cur.close()
#     conn.close()
# except Exception as e:
#     print(e)


#
# config = {
#     "host": "localhost",
#     "dbname": "dash_db",
#     "user": "postgres",
#     "password": "123456",
#     "port": "5432"
# }
#
#
# def query():
#
#     sql_query = 'DROP TABLE IF EXISTS alembic_version;'
#     with connect(**config) as conn:
#         with conn.cursor() as cur:
#             cur.execute(sql_query)
#             # res = cur.fetchall()
#             # print(res)
#
#
# query()