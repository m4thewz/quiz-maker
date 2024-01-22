import tkinter as tk
import json
from PIL import Image, ImageTk
from pages.home import HomePage
from pages.quiz import QuizPage
from settings import *

class Quiz():
    def __init__(self):
        # Configuração inicial da janela
        self.janela = tk.Tk()
        self.janela.resizable(False, False)
        self.janela.title("Quiz Maker")
        self.janela.wm_iconphoto(True, ImageTk.PhotoImage(Image.open("icon.png").resize((32,32))))
        self.janela.configure(bg=BACKGROUND)
        self.data = []
        self.carregarJSON()
        # Obtem todas as paginas que pode ser exibidas
        self.paginas = [HomePage(self.janela, self), QuizPage(self.janela, self.data[0], self)]
        self.paginaAtual = 0 # Define a primeira página (é o índice da lista de paginas)
        self.atualizarPagina(self.paginaAtual)

        self.janela.mainloop()
    # Verifica a pagina atual e a exibe dependendo disso
    def atualizarPagina(self, proximaPagina):
        self.paginaAtual = proximaPagina
        for widget in self.janela.winfo_children(): # apaga todos os elementos da página anterior
            widget.destroy()
        self.paginas[self.paginaAtual].gerarElementos()
    def trocarQuiz(self, quiz):
        if isinstance(quiz, dict):
            self.paginas[1] = QuizPage(self.janela, quiz, self)
            self.atualizarPagina(1)
    def carregarJSON(self):
        file = open("data.json", "r", encoding="utf-8")
        self.data = json.load(file)
        file.close()


if __name__ == "__main__":
    Quiz()