import tkinter as tk
from settings import *

class QuizPage():
    def __init__(self, window, data, root):
        self.window = window
        self.root = root
        self.data = data
        self.perguntas = data["perguntas"]
        self.totalPerguntas = len(self.perguntas)
        self.proximaPergunta = 0  # Adicionei para rastrear a próxima pergunta
        self.corretas = 0

    def gerarElementos(self):
        self.frame = tk.Frame(self.window, bg=BACKGROUND)
        self.frames = [Pergunta((pergunta, i), self.frame, self) for i, pergunta in enumerate(self.perguntas)]
        tk.Label(self.window, text=self.data["titulo"], font=(FONT, 35), bg=BACKGROUND).pack(fill="x",padx=30)
        tk.Label(self.frame, text=self.data["descricao"], font=(FONT, 15), bg=BACKGROUND).pack(fill="x")
        tk.Label(self.frame, text=f"Por {self.data['autor']}", font=(FONT, 12), bg=BACKGROUND).pack(fill="x")
        self.frame.pack(fill="x", padx=10)
        tk.Button(self.frame, text="Iniciar Quiz", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=self.iniciarQuiz).pack(fill="x",pady=(10, 0))
        tk.Button(self.window, text="Voltar a página inicial", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=lambda: self.root.atualizarPagina(0)).pack(fill="x", padx=10, pady=10)

    def iniciarQuiz(self):
        self.mudarPergunta(0)

    def mudarPergunta(self, proximaPergunta):
        if proximaPergunta < self.totalPerguntas:
            self.proximaPergunta = proximaPergunta
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frames[self.proximaPergunta].gerarElementos()
        else:
            self.finalizarQuiz()

    def finalizarQuiz(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text=f"Você acertou {self.corretas} de {len(self.perguntas)}", font=(FONT, 15), bg=BACKGROUND).pack()

class Pergunta():
    def __init__(self, pergunta, window, page):
        self.pergunta = pergunta[0]
        self.indice = pergunta[1]
        self.frame = window
        self.page = page

    def gerarElementos(self):
        self.alternativasWidgets = []
        tk.Label(self.frame, text=self.pergunta["pergunta"], font=(FONT, 15), bg=BACKGROUND).pack()
        for i, alternativa in enumerate(self.pergunta["alternativas"]):
            botao = tk.Label(self.frame, text=alternativa, font=(FONT, 13), borderwidth=2, relief="groove", bg=BUTTON_COLOR)
            botao.configure(highlightbackground = "red", highlightcolor= "red")
            botao.pack(fill="x",pady=3)
            botao.bind("<Enter>", lambda e, widget=botao: self.mudarBackground(widget, HOVER_COLOR))
            botao.bind("<Leave>", lambda e, widget=botao: self.mudarBackground(widget, BUTTON_COLOR))
            botao.bind("<Button-1>", lambda event, index=i: self.verificarCorreta(event, index))
            self.alternativasWidgets.append(botao)
        self.frame.pack(fill="x")

    def verificarCorreta(self, e, indice):
        corretaIndice = self.pergunta["correta"]
        self.mudarBackground(self.alternativasWidgets[corretaIndice], CORRECT_COLOR)
        if indice != corretaIndice:
            self.mudarBackground(e.widget, WRONG_COLOR)
        else:
            self.page.corretas += 1
        self.page.window.after(300, lambda: self.page.mudarPergunta(self.page.proximaPergunta + 1))

    def mudarBackground(self, widget, cor="#ffffff"):
        if widget["background"] not in [WRONG_COLOR, CORRECT_COLOR]:
            widget["background"] = cor

