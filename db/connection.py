import os
import dotenv
import pyodbc

TABLE_NAME = 'baseROs'
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

    with cnxn:
        with cnxn.cursor() as cursor:
            sql = (
                f'SELECT * FROM {TABLE_NAME}'
            )
            cursor.execute(sql)
            data = cursor.fetchall()

            for valor in data:
                print(valor)

except pyodbc.InterfaceError:
    print('Cannot connect to SQL server')
