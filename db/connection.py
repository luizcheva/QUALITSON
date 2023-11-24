import os
import dotenv
import pyodbc

TABLE_NAME = 'baseCQ'
dotenv.load_dotenv()

server = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DATABASE']
username = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
driver = '{ODBC Driver 17 for SQL Server}'

connection = (
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};'
    f'PWD={password};'
)

try:
    cnxn = pyodbc.connect(connection)
    print('Connection established')
    # data = '2023-07-17'
    # with cnxn:
    #     with cnxn.cursor() as cursor:
    #         sql = (
    #             f"INSERT INTO {TABLE_NAME} ("
    #             "ITEM, BATCH, [ORDER], DESCRIPTION, [DATE], [PATH]) "
    #             "VALUES ("
    #             "'101.004', 'NZK96', 0, 'Rebarba na Rosca interna', "
    #             f"'{data}', "
    #             "'101.004 - Rebarba na Rosca interna - NZK96.jpg');"
    #         )
    #         print(sql)
    #         cursor.execute(sql)

    with cnxn:
        with cnxn.cursor() as cursor:
            sql = (
                f"SELECT * FROM {TABLE_NAME};"
            )
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            print(columns)

            data = cursor.fetchall()
            for item in data:
                _, valor, *resto, end_azure = item
                print(valor, end_azure)

        cnxn.commit()
except pyodbc.InterfaceError:
    print('Cannot connect to SQL server')
