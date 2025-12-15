import json
from sentence_transformers import SentenceTransformer, util
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime


# ================== MODELO ==================
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# ================== DADOS FAQ ==================
def carregar_perguntas():
    with open("faq.json", "r", encoding="utf-8") as file:
        return json.load(file)

faq_data = carregar_perguntas()
perguntas = [item["pergunta"] for item in faq_data]
respostas = {item["pergunta"]: item["resposta"] for item in faq_data}
perguntas_emb = modelo.encode(perguntas, convert_to_tensor=True)


def buscar_resposta(pergunta_usuario):
    entrada_emb = modelo.encode(pergunta_usuario, convert_to_tensor=True)
    similaridades = util.pytorch_cos_sim(entrada_emb, perguntas_emb)

    max_similaridade, indice = similaridades[0].max(0)
    max_similaridade = max_similaridade.item()

    if max_similaridade < 0.45:
        return "❌ Desculpe, não tenho essa informação no momento. Consulte o RH ou setor responsável."

    return respostas[perguntas[indice]]


# ================== JANELA ==================
class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Faq Helper • Chat")
        self.setFixedSize(840, 600)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("""
                                            background-color: #DCD7C9;
                                        """)

        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)

        # Input
        self.textarea = QTextEdit()
        self.textarea.setFixedHeight(90)
        self.textarea.setFont(QFont('Arial', 10))
        self.textarea.installEventFilter(self)

        # Botão
        self.botao = QPushButton("Enviar")
        self.botao.setFont(QFont('Arial', 10))
        self.botao.clicked.connect(self.salvar_texto)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.textarea)
        layout.addWidget(self.botao)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        QTimer.singleShot(300, self.mensagem_boas_vindas)


    def eventFilter(self, obj, event):
        if obj is self.textarea and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                if event.modifiers() == Qt.ShiftModifier:
                    return False  # Shift+Enter → quebra linha
                else:
                    self.salvar_texto()
                    return True  # Enter → envia
        return super().eventFilter(obj, event)

    
    def mensagem_boas_vindas(self):
        hora = datetime.now().hour

        if 5 <= hora < 12:
            saudacao = "☀️ Bom dia!"
        elif 12 <= hora < 18:
            saudacao = "🌤 Boa tarde!"
        else:
            saudacao = "🌙 Boa noite!"

        # Montar menu automaticamente a partir do FAQ
        menu = "\n".join(
            [f"• {item['pergunta']}" for item in faq_data]
        )

        mensagem = (
            f"{saudacao}\n\n"
            "Eu sou o 🤖 *Faq Helper*.\n"
            "Posso te ajudar com informações sobre:\n\n"
            f"{menu}\n\n"
            "💬 Basta digitar sua dúvida."
        )

        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.adicionar_mensagem(
            f"🤖 {mensagem}\n\n{data_hora}",
            is_user=False
        )

    
    def mostrar_digitando(self):
        self.label_digitando = QLabel("🤖 digitando...")
        self.label_digitando.setFont(QFont('Arial', 9))
        self.label_digitando.setStyleSheet("background-color: #547792; color: #fff; padding: 8px; border-radius: 8px;")

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.label_digitando)
        layout.addStretch()

        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, container)

        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

        return container

    
    # ================== CHAT ==================
    def adicionar_mensagem(self, texto, is_user=True):
        bubble = QLabel(texto)
        bubble.setWordWrap(True)
        bubble.setFont(QFont('Arial', 10))
        bubble.setMaximumWidth(int(self.width() * 0.7))

        if is_user:
            bubble.setStyleSheet("""
                background-color: #1F7D53;
                color: #fff;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.08);
            """)
        else:
            bubble.setStyleSheet("""
                background-color: #547792;
                color: #fff;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.08);
            """)

        container = QWidget()
        layout = QHBoxLayout(container)

        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()

        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, container)

        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def responder_bot(self, texto, container_digitando):
        # Remove o "digitando..."
        container_digitando.deleteLater()

        data_hora_formatada = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        resposta = buscar_resposta(texto)

        self.adicionar_mensagem(f"🤖 {resposta}\n{data_hora_formatada}", is_user=False)

    
    def salvar_texto(self):
        data_hora_formatada = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        texto = self.textarea.toPlainText().strip()
        if not texto:
            return

        self.adicionar_mensagem(f"👨‍💻 {texto}\n{data_hora_formatada}", is_user=True)
        self.textarea.clear()

        # Mostrar indicador digitando
        container_digitando = self.mostrar_digitando()

        # Simular tempo de resposta
        QTimer.singleShot(600, lambda: self.responder_bot(texto, container_digitando))


