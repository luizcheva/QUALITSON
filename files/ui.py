import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QVBoxLayout, QWidget, QGridLayout, QLineEdit,
    QPushButton, QScrollArea, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt, QCoreApplication
from files.request import connectionBD
from files.theme import (
    MEDIUM_FONT_SIZE, MINIMUM_WIDTH,
    TEXT_MARGIN, SMALL_FONT_SIZE, MINIMUM_HEIGHT,
)
from PIL import Image
from files.request import (
    KEY_CONTAINER, DIR_CONTAINER, convertData, downloadImage
)


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.chat_history = []
        self.setWindowTitle("Qualitson")

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setMinimumSize(900, 700)

        # Adicione um QScrollArea para a grade de mensagens
        self.scroll_area = QScrollArea()
        layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        # Crie um widget para conter a grade de mensagens
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.message_grid = QGridLayout()
        self.scroll_content.setLayout(self.message_grid)

        self.user_input = QLineEdit()
        margins = [TEXT_MARGIN for _ in range(4)]
        self.user_input.setMinimumHeight(MINIMUM_HEIGHT)
        self.user_input.setMinimumWidth(MINIMUM_WIDTH)
        self.user_input.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')
        self.user_input.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.user_input.setTextMargins(*margins)

        self.user_input.setPlaceholderText('Digite um item válido...')
        self.send_button = QPushButton("Enviar")

        # Adicione campos de entrada e botão a um widget que será esticável
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.addWidget(self.user_input)
        bottom_layout.addWidget(self.send_button)

        # Alinhe o widget inferior na parte inferior
        layout.addWidget(bottom_widget, alignment=Qt.AlignBottom)

        self.qualitson_response = []
        self.guardaResposta = []
        self.guardaROs = []
        self.guardaROs_img = []
        self.alturaImg = 400
        self.send_button.clicked.connect(self.send_user_message)
        self.user_input.returnPressed.connect(self.send_user_message)

    def add_message(self, sender, message, is_user=True, is_img=False):
        message_text = f'<strong>{sender}:</strong><br>{message}'
        message_box = QTextEdit()
        message_box.setReadOnly(True)
        message_box.setHtml(message_text)

        if is_user:
            message_box.setStyleSheet(
                "background-color: #7030A0; color: #FFF; border-radius: 10px; "
                "padding: 10px; font-size: 12px;"
            )
            message_box.setMinimumHeight(70)
        elif is_img:
            message_box.setStyleSheet(
                "background-color: #DDD; color: #333; border-radius: 10px; "
                f"padding: 10px; font-size: {SMALL_FONT_SIZE}px;"
            )
            message_box.setMinimumHeight(self.alturaImg)
            message_box.setMinimumWidth(640)
        else:
            message_box.setStyleSheet(
                "background-color: #DDD; color: #333; border-radius: 10px; "
                f"padding: 10px; font-size: {SMALL_FONT_SIZE}px;"
            )
            message_box.setMinimumHeight(250)

        row = self.message_grid.rowCount()
        self.message_grid.addWidget(message_box, row, 0 if is_user else 1)
        self.roll()

    def send_user_message(self):
        user_message = self.user_input.text()
        total_message = len(self.chat_history)
        if user_message:
            self.add_message("Você", user_message)
            self.chat_history.append(user_message)
            self.roll()
            self.user_input.clear()

            # Qualitson Answere
            if total_message >= 2:
                chatbot_response_RO = self.generate_message_RO(user_message)
                if chatbot_response_RO is not None:
                    if type(chatbot_response_RO) is tuple:
                        msg, img = chatbot_response_RO
                        self.add_message("Qualitson", msg, is_user=False)
                        self.chat_history.append(chatbot_response_RO)
                        html_img = self.resize_image(img, 640)
                        self.add_message(
                            "Qualitson", html_img, is_user=False, is_img=True
                        )
                        self.roll()
                        return

                    self.add_message(
                        "Qualitson", chatbot_response_RO, is_user=False
                    )
                    self.chat_history.append(chatbot_response_RO)
                    self.roll()
                    return

            chatbot_response = self.generate_chatbot_response(user_message)
            self.add_message("Qualitson", chatbot_response, is_user=False)
            self.chat_history.append(chatbot_response)
            self.roll()
        else:
            QMessageBox.critical(
                self, "Error", "Você precisa inserir um registro válido."
            )
            return

    def generate_chatbot_response(self, item):
        self.qualitson_response.clear()
        bd = connectionBD()
        pesquisar = bd.consultaProblema(item)
        problemas = bd.retornaProblema(pesquisar)

        if problemas is not None:
            self.guardaResposta.clear()
            msgWelcome = f'Informações sobre o Item: {item}<br>'
            self.qualitson_response.append(msgWelcome)
            for x, texto in enumerate(problemas):
                informacoes = (
                    f'{texto["DESCRIPTION"]}, Lote: {texto["BATCH"]}. '
                    f'Data: {texto["DATE"]}<br>'
                )
                response = (
                    f'({x}) {informacoes}'
                )
                self.guardaResposta.append(
                    (
                        x, texto["BATCH"], texto["END_AZURE"],
                        texto["DESCRIPTION"], texto["ITEM"]
                    )
                )
                self.qualitson_response.append(response)

            detalhes = (
                '<br>Digite um número para ver mais detalhes do problema '
                'ou digite outro código de item:'
            )
            self.qualitson_response.append(detalhes)
            resposta_qualitson = ''.join(self.qualitson_response)
            return resposta_qualitson
        else:
            return f'Não encontrei nenhum item com o código enviado "{item}"'

    def generate_message_RO(self, item):
        self.guardaROs.clear()
        self.guardaROs_img.clear()
        cont_opt = len(self.guardaResposta)
        try:
            opt_ = int(item)
        except ValueError:
            return None
        for resp in self.guardaResposta:
            num, lote, path, *_ = resp
            if str(num) == item and opt_ <= cont_opt:
                if not lote:
                    informacao = (
                        'Lote vazio ou inexistente em nosso Banco de dados'
                    )
                    return informacao
                bd = connectionBD()
                pesquisar = bd.consultaROs(lote)
                problemas = bd.retornaROs(pesquisar)
                if problemas is not None:
                    for valor in problemas:
                        data_ocorrencia = convertData(valor["DATE"])
                        informacao = (
                            f'Problema({str(item)}) - Lote: {valor["BATCH"]} -'
                            f' Em {data_ocorrencia} foi aberta uma RO '
                            f'para esse problema ({valor["IDENTIFICATION"]}), '
                            'onde sua classificação é '
                            f'"{valor["CLASSIFICATION"]}" '
                            f'onde a disposição foi "{valor["DISPOSITION"]}" '
                            '<br><br>'
                        )
                        self.guardaROs.append(informacao)
                        self.guardaROs_img.append(path)
                    msg_img = "Segue a imagem do problema:<br>"
                    self.guardaROs.append(msg_img)
                    qualitison_ROs = ''.join(self.guardaROs)
                    return (qualitison_ROs, path)
                else:
                    informacao = (f'Nenhum registro de RO para o lote {lote}')
                    self.guardaROs.append(informacao)
                    qualitison_ROs = ''.join(self.guardaROs)
                    return qualitison_ROs

        return None

    def resize_image(self, image_path, width):
        # Carregue a imagem e redimensione-a usando Pillow
        self.alturaImg = 400
        raizImg = DIR_CONTAINER + image_path + KEY_CONTAINER
        imgFile = downloadImage(raizImg)
        img = Image.open(imgFile)
        largura, altura = img.size
        nova_largura = width
        nova_altura = round(altura * nova_largura / largura)
        self.alturaImg = nova_altura + 50

        img = img.resize(size=(nova_largura, nova_altura))

        # Salve a imagem redimensionada temporariamente
        pasta = "_img"
        temp_image_path = "temp.png"
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        caminho = os.path.join(pasta, temp_image_path)
        img.save(caminho)

        # Insira a imagem redimensionada no QTextEdit
        html_img = f'<img src="{caminho}">'

        return html_img

    def roll(self):
        QCoreApplication.processEvents()
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


if __name__ == '__main__':
    app = QApplication([])
    window = ChatWindow()

    window.show()
    sys.exit(app.exec())
