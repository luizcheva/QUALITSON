import pymssql
import dotenv
import os
from datetime import datetime
from requests import get
from pathlib import Path
from PySide6.QtWidgets import QMessageBox

ROOT_DIR = Path(__file__).parent
dotenv.load_dotenv(dotenv_path=ROOT_DIR / '.env')

SERVER = os.environ['HOST']
DATABASE = os.environ['DATABASE']
USERNAME = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
TABLE_CQ = os.environ['TABLE_CQ']
TABLE_RO = os.environ['TABLE_RO']
KEY_CONTAINER = os.environ['KEY_CONTAINER']
DIR_CONTAINER = os.environ['DIR_CONTAINER']
DIR_IMG = ROOT_DIR / 'img/'


class connectionBD():
    def __init__(self) -> None:
        try:
            self.conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
            self.cursor = self.conn.cursor()
            self.columns = []
        except pymssql.Error as err:
            QMessageBox.critical(
                None, "Error", f"Erro ao conectar:\n{str(err)}"
            )
            return

    def consultaProblema(self, item):
        sql = f"SELECT * FROM {TABLE_CQ} WHERE ITEM LIKE '%{item}%';"
        self.cursor.execute(sql)
        registroProblema = self.cursor.fetchall()
        self.columns = [column[0] for column in self.cursor.description]
        self.close()
        return registroProblema

    def consultaROs(self, lote):
        sql = f"SELECT * FROM {TABLE_RO} WHERE BATCH LIKE '%{lote}%';"
        self.cursor.execute(sql)
        registroROs = self.cursor.fetchall()
        self.columns = [column[0] for column in self.cursor.description]
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
            for valor in consulta:
                dicionario = dict(zip(self.columns, valor))
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


def downloadImage(dir):
    if not os.path.exists(DIR_IMG):
        os.makedirs(DIR_IMG)

    nameFile = os.path.join(DIR_IMG, 'down_temp.jpg')

    with open(nameFile, 'wb') as imagem:
        response_ = get(dir, stream=True)

        if not response_.ok:
            return None

        for data in response_.iter_content(1024):
            if data:
                imagem.write(data)
            else:
                return None

    return nameFile


if __name__ == '__main__':
    # search = connectionBD()
    # verifica = search.consultaProblema('103.170-1')
    # dados = search.retornaProblema(verifica)
    # for nc in dados:
    #     print(nc['ID'])
    #     data_reg = convertData(nc['DATE'])
    #     print(data_reg)
    print(ROOT_DIR)
    print(DIR_IMG)
