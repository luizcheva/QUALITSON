import sqlite3
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent
DB_NAME = 'db_QUALITSON.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'usinagem'
TABLE_ROS = 'baseROs'


class connectionBD():
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def consultaProblema(self, item):
        sql = f'SELECT * FROM {TABLE_NAME} WHERE ITEM LIKE "%{item}%";'
        self.cursor.execute(sql)
        registroProblema = self.cursor.fetchall()
        self.close()
        return registroProblema

    def consultaROs(self, lote):
        sql = f'SELECT * FROM {TABLE_ROS} WHERE LOTE LIKE "%{lote}%";'
        self.cursor.execute(sql)
        registroROs = self.cursor.fetchall()
        self.close()
        return registroROs

    def retornaProblema(self, consulta):
        if consulta:
            list_dados = []
            for valor in consulta:
                dicionario = dict(valor)
                list_dados.append(dicionario)
            return list_dados
        else:
            return

    def retornaROs(self, consulta):
        if consulta:
            list_dados = []
            for valor in consulta:
                dicionario = dict(valor)
                list_dados.append(dicionario)
            return list_dados
        else:
            return

    def close(self):
        self.cursor.close()
        self.connection.close()


def convertData(data):
    convert_date = datetime.strptime(data, '%Y-%m-%d')

    return convert_date.strftime('%d/%m/%Y')
