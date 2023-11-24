import pyodbc
import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()

SERVER = os.environ['HOST']
DATABASE = os.environ['DATABASE']
USERNAME = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
DRIVER = os.environ['DRIVER']
TABLE_CQ = os.environ['TABLE_CQ']
TABLE_RO = os.environ['TABLE_RO']
KEY_CONTAINER = os.environ['KEY_CONTAINER']
DIR_CONTAINER = os.environ['DIR_CONTAINER']


class connectionBD():
    def __init__(self) -> None:
        self.connection = (
            f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};'
            f'UID={USERNAME};PWD={PASSWORD};'
        )
        self.conn = pyodbc.connect(self.connection)
        self.cursor = self.conn.cursor()
        self.columns = []

    def consultaProblema(self, item):
        sql = f"SELECT * FROM {TABLE_CQ} WHERE ITEM LIKE '%{item}%';"
        self.cursor.execute(sql)
        registroProblema = self.cursor.fetchall()
        self.columns = [column[0] for column in self.cursor.description]
        self.close()
        return registroProblema

    def consultaROs(self, lote):
        sql = f'SELECT * FROM {TABLE_RO} WHERE LOTE LIKE "%{lote}%";'
        self.cursor.execute(sql)
        registroROs = self.cursor.fetchall()
        self.close()
        return registroROs

    def retornaProblema(self, consulta):
        if consulta:
            list_dados = []
            for valor in consulta:
                dicionario = dict(zip(self.columns, valor))
                list_dados.append(dicionario)
            return list_dados
        else:
            return

    def retornaROs(self, consulta):
        if consulta:
            list_dados = []
            columns = [column[0] for column in self.cursor.description]
            for valor in consulta:
                dicionario = dict(zip(columns, valor))
                list_dados.append(dicionario)
            return list_dados
        else:
            return

    def close(self):
        self.cursor.close()
        self.conn.close()


def convertData(data):
    convert_date = datetime.strftime(data, '%d/%m/%Y')

    return convert_date


if __name__ == '__main__':
    search = connectionBD()
    verifica = search.consultaProblema('103.170-1')
    dados = search.retornaProblema(verifica)
    for nc in dados:
        print(nc['ID'])
        data_reg = convertData(nc['DATE'])
        print(data_reg)
