import tkinter as tk
import json
from settings import *
from pages.criar import TopLevel
from PIL import Image, ImageTk

class HomePage():
    def __init__(self, window, root):
        self.window = window
        self.root = root
        self.quizzes = []
        self.page = 0  # Página atual

    def gerarElementos(self):
        titulo = tk.Label(self.window, text="Quiz Maker", font=(FONT, 35), bg=BACKGROUND)
        titulo.pack()
        self.pageFrame = tk.Frame(self.window, bg=BACKGROUND)
        self.pageFrame.pack(fill="x")

        with open("data.json", "r", encoding="utf-8") as file:
            self.quizzes = json.load(file)
        self.exibirQuizzes()
        botao = tk.Button(self.window, text="Criar um Quiz", relief="flat", bg=BUTTON_COLOR, command=self.abrirNovaJanela)
        botao.pack(fill="x", padx=(10, 10), pady=(0, 10))

    def exibirQuizzes(self):
        # exibe os quizzes em uma grade 3x3
        start = self.page * 6
        end = min(start + 6, len(self.quizzes))
        for i in range(2):
            for j in range(3):
                index = i * 3 + j
                if index < (end - start):
                    self.exibirQuiz(self.quizzes[start + index], row=i + 1, column=j)

        # botões pra trocar de pagina
        if self.page > 0:
            tk.Button(self.pageFrame, text="Página Anterior", relief="flat", bg=BUTTON_COLOR, command=lambda: self.mudarPagina("anterior")).grid(row=4, column=0, padx=(10, 0), pady=(5, 10), sticky="w", columnspan=1)
        if end < len(self.quizzes):
            tk.Button(self.pageFrame, text="Próxima Página", relief="flat", bg=BUTTON_COLOR, command=lambda: self.mudarPagina("proximo")).grid(row=4, column=2, padx=(0, 10), pady=(5, 10), sticky="e", columnspan=1)


    def exibirQuiz(self, quiz, row, column):
        frame = tk.Frame(self.pageFrame, bg=BACKGROUND)
        frame.grid(row=row, column=column, padx=10, pady=10)

        # obtem a imagem (se não tiver definida, define uma de padrao) e a redimensiona
        imagem = ImageTk.PhotoImage(Image.open(quiz.get("imagem", "images/padrao.png")).resize((250, 250))) 

        labelImagem = tk.Label(frame, image=imagem, bg=BACKGROUND)
        labelImagem.image = imagem
        labelImagem.pack(fill="x")

        botao = tk.Button(frame, text=quiz["titulo"], relief="flat", bg=BUTTON_COLOR, command=lambda q=quiz: self.root.trocarQuiz(q))
        botao.pack(fill="x")

        labelImagem.bind("<Button-1>", lambda e, q=quiz: self.root.trocarQuiz(q))

    def mudarPagina(self, sentido):
        if sentido == "proximo" and (self.page + 1) * 6 < len(self.quizzes):
            self.page += 1
            self.limparPagina()
            self.exibirQuizzes()
        if sentido == "anterior" and self.page > 0:
            self.page -= 1
            self.limparPagina()
            self.exibirQuizzes()

    def limparPagina(self):
        for widget in self.pageFrame.winfo_children():
            widget.destroy()
    def abrirNovaJanela(self):
        TopLevel(tk.Toplevel(), self)
    
if __name__ == "__main__":
    window = tk.Tk()
    app = HomePage(window, None)
    app.gerarElementos()
    window.mainloop()
