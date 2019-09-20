from subprocess import call
from tkinter import *

import firebase_admin
from firebase_admin import credentials


# função para iniciar a janela/página livros que quero ler
def click_livros_quero_ler():
    call(["python", "livros_quero_ler.py"])


# função para iniciar a janela/página livros lidos
def click_livros_lidos():
    call(["python", "livros_lidos.py"])


# função para iniciar a janela/página minha estante
def click_minha_estante():
    call(["python", "minha_estante.py"])


# função para concetar a credencial de acesso ao Firebase, utilizando os dados do arquivo json como chave de autenticação
def conexao_firebase():
    # cria a credencial necessária para acessar o Firebase
    credencial = credentials.Certificate(
        'C:\\Users\\Usuario\\Documents\\Rafael\\Projetos\\RafaBBT\\bbt-rafa-firebase.json')
    # inicializa a conexão com o Firebase, utilizando a credencial e o endereço do Firebase
    firebase_admin.initialize_app(credencial, {
        'databaseURL': 'https://bbt-rafa.firebaseio.com'})


# executa a função para conectar à database do Firebase
conexao_firebase()


# classe principal do programa
class BBT_RAFA_SAID():
    def __init__(self):
        self.bbt_window = Tk()
        self.bbt_window.configure(background='red')
        self.bbt_window.title('BBT | By Rafa Said')
        self.bbt_window.resizable(False, False)
        self.bbt_window.wm_iconbitmap('bbt.ico')

        # ========== LABELS ==========
        Label(self.bbt_window, text='BBT RAFA, LEILA E SOFIA', width=25, bg='red', fg='black',
              font='arial 30 bold').grid(row=0, column=0, sticky=W, padx=10, pady=10)

        # ========= BUTTON ==========
        self.livros_quero_ler = Button(self.bbt_window, text='LIVROS QUE QUERO LER', width=20, bg='red', fg='black',
                                       font='arial 20 bold', bd=5, command=click_livros_quero_ler).grid(row=1, column=0,
                                                                                                        sticky=N,
                                                                                                        padx=5, pady=8)

        self.livros_lidos = Button(self.bbt_window, text='LIVROS LIDOS', width=20, bg='red', fg='black',
                                   font='arial 20 bold', bd=5, command=click_livros_lidos).grid(row=2, column=0,
                                                                                                sticky=N, padx=5,
                                                                                                pady=8)

        self.minha_estante = Button(self.bbt_window, text='MINHA ESTANTE', width=20, bg='red', fg='black',
                                    font='arial 20 bold', bd=5, command=click_minha_estante).grid(row=3, column=0,
                                                                                                  sticky=N, padx=5,
                                                                                                  pady=8)

        # ========== EXECUÇÃO DA JANELA ==========
        self.bbt_window.mainloop()


try:
    BBT_RAFA_SAID()
except:
    raise Exception('A janela não pode ser criada!')
