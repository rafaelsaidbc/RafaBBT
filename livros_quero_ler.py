from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


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


# classe da lista de livros a serem lidos
class LISTA_LER():
    def __init__(self):
        self.livros_ler_window = Tk()
        self.livros_ler_window.configure(background='red')
        self.livros_ler_window.title('BBT | By Rafa Said')
        self.livros_ler_window.resizable(False, False)
        self.livros_ler_window.wm_iconbitmap('bbt.ico')

        # style para configurar a Treeview
        style = ttk.Style(self.livros_ler_window)
        style.theme_use("clam")
        # style.configure("Treeview", background='yellow', fieldbackground='black', foregound='yellow')

        # ========== LABELS ==========
        Label(self.livros_ler_window, text='LIVROS QUE QUERO LER', width=25, bg='red', fg='black',
              font='arial 30 bold').grid(row=0, column=0, sticky=W, padx=10, pady=10)

        # ============================= TREEVIEW =============================
        tree = ttk.Treeview(self.livros_ler_window, selectmode='browse', column=('column1', 'column2'), show='headings')
        # define as colunas da Treeview
        tree.column('column1', width=400, minwidth=400, stretch=YES, anchor=N)
        tree.heading('#1', text='Autor')
        tree.column('column2', width=400, minwidth=400, stretch=YES, anchor=N)
        tree.heading('#2', text='Título')
        tree.grid(row=1, column=0)

        # pega a referência na database do Firebase
        referencia = db.reference()
        # pega os itens que estão catalogados na database
        livros_ler = referencia.child('livrosLer').get().items()

        # pega cada elemento (key) do Firebase
        for elemento in livros_ler:
            # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
            dados = elemento[1]
            # insere os dados do Firesabe na TreeView
            tree.insert('', END, values=(dados['autor'], dados['titulo']))

        # ========== FUNÇÕES ==========
        def cadastrar_livro():
            # cria uma instância em TopLevel, para ser acessada somente com click
            janela_livros_ler_db = Toplevel(bg='blue')
            # define o título da janela
            janela_livros_ler_db.title('Cadastro de livros na lista de leitura')
            janela_livros_ler_db.configure(background='red')
            janela_livros_ler_db.wm_iconbitmap('bbt.ico')

            # cria as Labels com os dados e posiciona na janela
            Label(janela_livros_ler_db, text='Título', width=15, bg='red', font='arial 20 bold').grid(row=0)
            Label(janela_livros_ler_db, text='Autor', width=15, bg='red', font='arial 20 bold').grid(row=1)

            # define as variáveis como globais para poderem ser acessadas por outras funções
            titulo_livros_ler = Entry(janela_livros_ler_db, width=40, font='arial 20 bold')
            titulo_livros_ler.grid(row=0, column=1, padx=4, pady=8)
            autor_livros_ler = Entry(janela_livros_ler_db, width=40, font='arial 20 bold')
            autor_livros_ler.grid(row=1, column=1, padx=4, pady=8)

            def adicionar_livro_db():
                # obtém a referência da database no Firebase
                referencia = db.reference()
                # obtém a referência da child livrosLidos e armazena na variável postar_livro
                postar_livro = referencia.child('livrosLer')

                # cria a instância para postar um livro no Firebase
                novo_post = postar_livro.push()

                # cria um dicionario com os dados do livro {id_livro, título, autor, páginas, início da leitura, fim da leitura, cidade da editora, editora, ano da edição}
                dicionario_livro = {
                    'titulo': titulo_livros_ler.get(),
                    'autor': autor_livros_ler.get(),
                }
                # posta os dados do livro no Firebase
                novo_post.set(dicionario_livro)
                # mostra uma mensagem confirmando a inclusão do livro na database
                messagebox.showinfo('Lista de livros a serem lidos', 'Livro inserido com sucesso!')

                # limpa as ENTRY
                titulo_livros_ler.delete(0, 'end')
                autor_livros_ler.delete(0, 'end')

                # =============== BUTTON ===============

            btn_add_db = Button(janela_livros_ler_db, text='CADASTRAR', width=12, bg='red', fg='black',
                                font='arial 20 bold', bd=5, command=adicionar_livro_db).grid(row=2, column=1,
                                                                                             sticky=N + W, padx=5,
                                                                                             pady=8)

            btn_sair_db = Button(janela_livros_ler_db, text='SAIR', width=12, bg='red', fg='black',
                                 font='arial 20 bold', bd=5, command=janela_livros_ler_db.destroy).grid(row=2, column=1,
                                                                                                        sticky=N + E,
                                                                                                        padx=5, pady=8)

        # função para deletar os registros
        def deletar_registro():
            tree.bind("<TreeviewSelect>")
            titulo = tree.item(tree.selection())['values'][1]
            messagebox.askquestion('RAFA BBT',
                                   'Você tem certeza que deseja apagar ' + titulo + '?')

            reference_database = db.reference().child('livrosLer')
            dicionario_database = reference_database.get()
            for key, valores in dicionario_database.items():
                if valores['titulo'] == titulo:
                    key_firebase = key
                    break
            referencia_deletar = reference_database.child(key_firebase)
            referencia_deletar.delete()

        cadastrar = Button(self.livros_ler_window, text='CADASTRAR', width=12, bg='red', fg='black',
                           font='arial 20 bold', bd=5, command=cadastrar_livro).grid(row=3, column=0, sticky=N + W,
                                                                                     padx=5, pady=8)

        deletar = Button(self.livros_ler_window, text='DELETAR', width=12, bg='red', fg='black', font='arial 20 bold',
                         bd=5, command=deletar_registro).grid(row=3, column=0, sticky=N, padx=5, pady=8)

        sair = Button(self.livros_ler_window, text='SAIR', width=12, bg='red', fg='black', font='arial 20 bold', bd=5,
                      command=self.livros_ler_window.destroy).grid(row=3, column=0, sticky=N + E, padx=5, pady=8)

        # ============================== EXECUTA A JANELA ==============================
        self.livros_ler_window.mainloop()


try:
    LISTA_LER()
except:
    raise Exception('A janela não pode ser criada!')
