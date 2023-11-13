import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget

class ChatBotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatBot Simulado")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.layout.addWidget(self.text_edit)

        self.input_text = QLineEdit()
        self.input_text.setStyleSheet('background-color: #fff; padding: 10px; border: 1px solid #ddd;')
        self.layout.addWidget(self.input_text)

        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet('background-color: #007acc; color: #fff; padding: 10px; border: 1px solid #007acc;')
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

    def send_message(self):
        user_message = self.input_text.text()
        self.input_text.clear()
        self.add_message(f'Você: {user_message}', 'user')
        self.bot_response()

    def bot_response(self):
        response = self.generate_response()
        self.add_message(f'ChatBot: {response}', 'bot')

    def add_message(self, message, sender):
        current_text = self.text_edit.toPlainText()
        if current_text:
            current_text += '\n'
        current_text += f'<{sender}>{message}</{sender}>'
        self.text_edit.setHtml(current_text)

    def generate_response(self):
        responses = [
            "Olá! Como posso ajudar?",
            "Estou aqui para responder suas perguntas.",
            "Pergunte-me qualquer coisa!",
            "Eu sou um chatbot simples, mas farei o meu melhor para ajudar.",
        ]
        return random.choice(responses)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotApp()
    window.show()
    sys.exit(app.exec_())
