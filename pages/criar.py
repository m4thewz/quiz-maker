import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import shutil
from settings import *

class TopLevel:
    def __init__(self, janela, root):
        self.root = root
        self.janela = janela
        self.janela.title("Quiz Maker - Criar um Quiz")
        self.janela.resizable(False, False)
        self.janela.configure(bg=BACKGROUND)
        self.arquivo = None # localização da imagem do quiz
        self.perguntas = []
        self.frames = []
        self.alternativasFrames = []
        self.corretas = []
        self.paginaAtual = 0
        
        frame = tk.Frame(janela, width=100, bg=BACKGROUND)
        self.framePerguntas = tk.Frame(frame, bg=BACKGROUND)

        self.tituloEntry = tk.Entry(frame, bd=1, relief="solid", bg=ENTRY_COLOR)
        self.autorEntry = tk.Entry(frame, bd=1, relief="solid", bg=ENTRY_COLOR)
        self.descricaoEntry = tk.Text(frame, height=3, bd=1, relief="solid", bg=ENTRY_COLOR)

        botoesFrame = tk.Frame(frame, bg=BACKGROUND)
        removerPerguntaBotao = tk.Button(botoesFrame, text="Remover Pergunta", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=self.removerPergunta)
        adicionarPerguntaBotao = tk.Button(botoesFrame, text="Adicionar Pergunta", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=self.adicionarPergunta)
        paginaAnteriorBotao = tk.Button(botoesFrame, text="<", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=lambda: self.trocarPagina('anterior'))
        proximaPaginaBotao = tk.Button(botoesFrame, text=">", font=(FONT, 12), relief="flat", bg=BUTTON_COLOR, command=lambda: self.trocarPagina('proximo'))
        salvarBotao = tk.Button(frame, text="Salvar", font=(FONT, 15), relief="flat", bg=BUTTON_COLOR, command=self.salvar)

        tk.Label(janela, text="Criar um Quiz", bg=BACKGROUND, font=(FONT, 35)).pack()
        self.imagemFrame = tk.Label(janela, bg=BACKGROUND)
        self.selecionarImagemBotao = tk.Button(janela, text="Selecione uma imagem de capa", font=(FONT, 15), relief="flat", bg=BUTTON_COLOR, disabledforeground="black", command=self.selecionarImagem)
        self.imagemFrame.pack(fill="x")
        self.selecionarImagemBotao.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Título:", bg=BACKGROUND, font=(FONT, 15), anchor="w").pack(fill="x")
        self.tituloEntry.pack(fill="x")

        tk.Label(frame, text="Autor:", bg=BACKGROUND, font=(FONT, 15), anchor="w").pack(fill="x")
        self.autorEntry.pack(fill="x")

        tk.Label(frame, text="Descrição:", bg=BACKGROUND, font=(FONT, 15), anchor="w").pack(fill="x")
        self.descricaoEntry.pack(fill="x")

        # Botões
        removerPerguntaBotao.grid(row=0, column=0, sticky="e")
        adicionarPerguntaBotao.grid(row=0, column=1, sticky="e", padx=(10, 0))
        paginaAnteriorBotao.grid(row=0, column=2, sticky="e")
        proximaPaginaBotao.grid(row=0, column=3, sticky="w", padx=(10, 0))
        
        botoesFrame.grid_rowconfigure(0, weight=1)
        botoesFrame.grid_columnconfigure(2, weight=1)
        botoesFrame.pack(fill="x", pady=(10, 0))
        
        self.framePerguntas.pack(fill="x")
        salvarBotao.pack(fill="x", pady=(0, 10))

        self.adicionarPergunta()
        self.exibirPergunta()
        frame.pack(padx=10)

    def exibirPergunta(self):
        for frame in self.frames: frame.pack_forget() # apaga os frames da tela, mas sem destrui-los
        self.frames[self.paginaAtual].pack(fill="x")

    def removerPergunta(self):
        # Passa para a página anterior, depois disso remove a página atual das listas de perguntas e frames.
        pagina = self.paginaAtual
        if self.paginaAtual > 0:
            self.trocarPagina("anterior")
            for w in self.frames[pagina].winfo_children():
                w.destroy()
            self.frames.pop(pagina)
            self.perguntas.pop(pagina)
            self.alternativasFrames.pop(pagina)
            self.corretas.pop(pagina)

    def adicionarPergunta(self):
        # Cria um nove frame e adiciona na lista de frames e de perguntas, depois cria 2 alternativas
        framePergunta = tk.Frame(self.framePerguntas, bg=BACKGROUND)
        alternativasFrame = tk.Frame(framePergunta, bg=BACKGROUND)
        correta = tk.StringVar()
        correta.set("Selecione uma alternativa correta")
        opcoes = ["", ""] # Os 2 entry inicial começa vazio entao ja defino aqui o valor deles
        menu = tk.OptionMenu(framePergunta, correta, *opcoes)
        self.corretas.append([correta, menu])

        tk.Label(framePergunta, text="Pergunta:", font=(FONT, 15), bg=BACKGROUND, anchor="w").pack(fill="x")
        pergunta_entry = tk.Entry(framePergunta, bd=1, relief="solid", bg=ENTRY_COLOR)
        pergunta_entry.pack(fill="x")

        self.perguntas.append((pergunta_entry, []))
        self.frames.append(framePergunta)

        altLabelFrame = tk.Frame(framePergunta, bg=BACKGROUND)
        tk.Label(altLabelFrame, text="Alternativas:", font=(FONT, 15), bg=BACKGROUND, anchor="sw").grid(row=0, column=0, sticky="e")
        tk.Button(altLabelFrame, text="-", font=(FONT, 13), relief="flat", bg=BUTTON_COLOR, command=self.removerAlternativa).grid(row=0, column=1, sticky="e")
        tk.Button(altLabelFrame, text="+", font=(FONT, 13), relief="flat", bg=BUTTON_COLOR, command=self.adicionarAlternativa).grid(row=0, column=2, sticky="w", padx=(10, 0))
        altLabelFrame.grid_rowconfigure(0, weight=1)
        altLabelFrame.grid_columnconfigure(1, weight=1)

        altLabelFrame.pack(fill="x", pady=10)
        alternativasFrame.pack(fill="x")
        self.alternativasFrames.append(alternativasFrame)
        tk.Label(framePergunta, text="Alternativa correta:", font=(FONT, 15), bg=BACKGROUND, anchor="w").pack(fill="x")
        [self.adicionarAlternativa(True) for _ in range(2)]

        # estilo do menu
        menu.configure(
            font=(FONT, 10),
            bg=ENTRY_COLOR,
            activebackground=ENTRY_COLOR,
            highlightthickness=0,
            border=1,
            relief="solid",
            indicatoron=0
        )
        menu["menu"].configure(
            font=(FONT, 10),
            border=0,
        )
        menu.pack(fill="x", pady=(0,10))

        # self.atualizarCorreta()
        self.trocarPagina("proximo")
        

    def atualizarCorreta(self, outro=None):
        pagina = len(self.frames) - 1
        opcoes = [alt.get() for alt in self.perguntas[pagina][1]]
        menu = self.corretas[pagina]

        menuOptions = menu[1]["menu"]
        menuOptions.delete(0, "end")  # Limpa as opções atuais
        for opcao in opcoes:
            menuOptions.add_command(label=opcao, command=lambda value=opcao: menu[0].set(value))
        menu[0].set("Selecione uma alternativa correta")

    def adicionarAlternativa(self, inicial=False):
        # cria um entry e depois adicinoa na lista de perguntas
        pagina = len(self.frames) - 1 if inicial else self.paginaAtual

        entry = tk.Entry(self.alternativasFrames[pagina], bd=1, relief="solid", bg=ENTRY_COLOR)
        entry.bind("<KeyRelease>", self.atualizarCorreta)
        entry.pack(fill="x", pady=(0, 10))

        self.perguntas[pagina][1].append(entry)
        self.atualizarCorreta()

    def removerAlternativa(self):
        alternativas = self.perguntas[self.paginaAtual][1]
        if len(alternativas) > 2: # minimo de 2 alternativas por pergunta
            # apaga o ultimo entry da tela e remove da lista de perguntas
            alternativas[-1].destroy()
            alternativas.pop()
        self.atualizarCorreta()

    def trocarPagina(self, sentido):
        if sentido == "proximo" and self.paginaAtual < len(self.frames) - 1:
            self.paginaAtual += 1
        if sentido == "anterior" and self.paginaAtual > 0:
            self.paginaAtual -= 1
        self.exibirPergunta()
    
    def selecionarImagem(self):
        arquivo = filedialog.askopenfile(filetypes=[('Arquivos de Imagem', '*.jpg *.png')]) # abre uma janela de seleção de arquivos png e jpg
        
        if arquivo:
            self.arquivo = arquivo.name
            imagem = ImageTk.PhotoImage(Image.open(arquivo.name).resize((250, 250)))
            labelImagem = tk.Label(self.imagemFrame, image=imagem, bg=BACKGROUND, border=0)
            labelImagem.image = imagem
            labelImagem.pack(fill="x")

            self.selecionarImagemBotao["state"] = "disabled"
            self.selecionarImagemBotao.pack_forget()
        else:
            return

    def salvar(self):
        titulo = self.tituloEntry.get()
        autor = self.autorEntry.get()
        descricao = self.descricaoEntry.get("1.0", "end").strip()
        preenchido = bool(titulo and autor and descricao)

        data = {
            "titulo": titulo,
            "autor": autor,
            "descricao": descricao,
            "perguntas": []
        }
        # verifica se ta tudo preenchido
        for i, (pergunta_entry, alternativas) in enumerate(self.perguntas):
            pergunta = pergunta_entry.get()
            alts = []
            corretaValor = self.corretas[i][0].get()

            for alt in alternativas:
                if not alt.get(): preenchido = False
                else: alts.append(alt.get())

            if not pergunta or not alts or not all(alts):
                preenchido = False
            if preenchido:
                correta = 0
                try:
                    correta = alts.index(corretaValor)
                except:
                    messagebox.showerror(title="Erro", message="Selecione uma alternativa correta.")
                    return
                data["perguntas"].append({"pergunta": pergunta, "alternativas": alts, "correta": correta})
        
        if preenchido:
            # le o arquivo data e dps insere o quiz no incicio da lista
            with open('data.json', 'r', encoding="utf-8") as file:
                jsonData = json.load(file)

            # copia a imagem para a pasta 'images'
            if self.arquivo:
                extensao = self.arquivo.split("/")[-1].split(".")[1]
                arquivo = len(jsonData) + 1
                caminhoArquivo = f"{os.getcwd()}\images\{arquivo}.{extensao}"
                shutil.copyfile(self.arquivo, caminhoArquivo)
                data["imagem"] = f"images/{arquivo}.{extensao}"
                print('oi')
            jsonData.insert(0, data)

            with open('data.json', 'w', encoding="utf-8") as file:
                json.dump(jsonData, file, indent=2, ensure_ascii=False)
            messagebox.showinfo(title="Quiz salvo", message="Seu quiz foi salvo com sucesso.")
            # atualiza a pagina incial e dps apaga o toplevel
            self.root.quizzes = jsonData
            self.root.limparPagina()
            self.root.exibirQuizzes()
            self.janela.destroy()
        else:
            messagebox.showerror(title="Erro", message="Preencha todos os campos.")
        print(data)
        

if __name__ == "__main__":
    window = tk.Tk()
    app = TopLevel(window)
    window.mainloop()
