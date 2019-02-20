'''

ToDo INFORMAÇÕES NECESSÁRIAS
ToDo id_livro
ToDo título
ToDo autor
ToDo páginas
ToDo início da leitura
ToDo fim da leitura
ToDo cidade da editora
ToDo editora
ToDo ano da edição

OUTRAS INFORMAÇÕES
ToDo Separar os livros lidos por anos
ToDo fazer uma lista com os livros a serem lidos

'''
from tkinter import *
import tkinter as tk


FONTE = ("Verdana", 12)

def livros2013():
    janela_livros2013 = Toplevel()
    janela_livros2013.title('Livros lidos em 2013')


class BbtRafa(tk.Tk):
    #cria a inicialização da janela principal
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #cria o container para colocar os widgets
        container = tk.Frame(self)
        #localização do container
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #cria um dicionário vazio para colocar os frames
        self.frames={}

        #para cada Frame das janelas do programa
        for F in (PaginaPrincipal, PaginaListaLer, PaginaLidos):
            #coloca o frame no container
            frame = F(container, self)
            #define que o frame será o atual
            self.frames[F] = frame
            #localização do frame
            frame.grid(row=0, column=0, sticky='nsew')
        #exibe o frame na janela inicial do programa
        self.show_frame(PaginaPrincipal)

    #função para mostrar cada frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#classe para exibir a janela incial do programa
class PaginaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='BBT do Rafael Said', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_livros_ler = tk.Button(self, text='Livros que quero ler', command= lambda: controller.show_frame(PaginaListaLer))
        btn_livros_ler.pack()

        btn_livros_lidos = tk.Button(self, text='Livros lidos', command=lambda: controller.show_frame(PaginaLidos))

        btn_livros_lidos.pack()

class PaginaListaLer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Lista de livros a serem lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()

class PaginaLidos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Livros lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn2013 = tk.Button(self, text='2013')
        btn2013.pack()

        btn2014 = tk.Button(self, text='2014')
        btn2014.pack()

        btn2015 = tk.Button(self, text='2015')
        btn2015.pack()

        btn2016 = tk.Button(self, text='2016')
        btn2016.pack()

        btn2017 = tk.Button(self, text='2017')
        btn2017.pack()

        btn2018 = tk.Button(self, text='2018')
        btn2018.pack()

        btn2019 = tk.Button(self, text='2019')
        btn2019.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()

app = BbtRafa()
app.mainloop()


'''
janela_principal = Tk()
janela_principal.title('BBT do Rafael Said')

Label(janela_principal, text='Bem-vindo à biblioteca do Rafael Said!').grid(row=0, sticky=N)
btn_lista = Button(janela_principal, width=20, text='Livros a serem lidos').grid(row=1, sticky=N)
btn_livros_lidos = Button(janela_principal, width=20, text='Livros lidos').grid(row=2, sticky=N)

janela_principal.mainloop()
'''