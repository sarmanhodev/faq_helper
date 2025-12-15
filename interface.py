from PyQt5.QtWidgets import QApplication
from main import TelaPrincipal

app = QApplication([])

# Criar e exibir a tela principal
tela = TelaPrincipal()
tela.show()

# Iniciar o loop de eventos
app.exec_()
