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


# classe principal do programa
class LIVROS_LIDOS():
    def __init__(self):
        self.minha_bbt_window = Tk()
        self.minha_bbt_window.configure(background='red')
        self.minha_bbt_window.title('RAFA BBT | By Rafa Said')
        self.minha_bbt_window.resizable(False, False)
        self.minha_bbt_window.wm_iconbitmap('bbt.ico')

        # =============================== FUNÇÔES ===============================
        # função para adicionar livros lidos no Firebase
        def formulario_add_books():

            fonte = 'arial 12 bold'

            window_add_books = Toplevel()
            window_add_books.title('Cadastro de livros da minha estante')
            window_add_books.wm_iconbitmap('bbt.ico')
            window_add_books.configure(background='red')

            Label(window_add_books, text='Ano de aquisição', font=fonte, bg='red').grid(row=0, pady=5)
            Label(window_add_books, text='Título', font=fonte, bg='red').grid(row=1, pady=5)
            Label(window_add_books, text='Autor', font=fonte, bg='red').grid(row=2, pady=5)
            Label(window_add_books, text='Páginas', font=fonte, bg='red').grid(row=3, pady=5)
            Label(window_add_books, text='Cidade da editora', font=fonte, bg='red').grid(row=4, pady=5)
            Label(window_add_books, text='Editora', font=fonte, bg='red').grid(row=5, pady=5)
            Label(window_add_books, text='Ano da edição', font=fonte, bg='red').grid(row=6, pady=5)

            fonte_entry = 'arial 15 bold'
            global ano_aquisicao
            ano_aquisicao = Entry(window_add_books, width=40, font=fonte_entry)
            ano_aquisicao.grid(row=0, column=1)
            global titulo
            titulo = Entry(window_add_books, width=40, font=fonte_entry)
            titulo.grid(row=1, column=1)
            global autor
            autor = Entry(window_add_books, width=40, font=fonte_entry)
            autor.grid(row=2, column=1)
            global paginas
            paginas = Entry(window_add_books, width=40, font=fonte_entry)
            paginas.grid(row=3, column=1)
            global cidade_editora
            cidade_editora = Entry(window_add_books, width=40, font=fonte_entry)
            cidade_editora.grid(row=4, column=1)
            global editora
            editora = Entry(window_add_books, width=40, font=fonte_entry)
            editora.grid(row=5, column=1)
            global ano_edicao
            ano_edicao = Entry(window_add_books, width=40, font=fonte_entry)
            ano_edicao.grid(row=6, column=1)

            # função para inserir livros lidos no Firebase
            def inserir_livro_estante():

                # obtém a referência da database no Firebase
                referencia = firebase_admin.db.reference()

                # obtém a referência da child livrosLidos e armazena na variável postar_livro
                postar_livro = referencia.child('minhaBBT')

                # cria a instância para postar um livro no Firebase
                novo_post = postar_livro.push()

                # cria um dicionario com os dados do livro {id_livro, título, autor, páginas, início da leitura, fim da leitura, cidade da editora, editora, ano da edição}
                dicionario_livro = {
                    'titulo': titulo.get(),
                    'autor': autor.get(),
                    'paginas': paginas.get(),
                    'cidadeEditora': cidade_editora.get(),
                    'editora': editora.get(),
                    'anoEdicao': ano_edicao.get(),
                }

                add_book_msg_box = messagebox.askquestion('Inserir livro na estante',
                                                          'Você tem certeza que deseja inserir o livro "' + titulo.get() + '" na sua estante?')

                if add_book_msg_box == 'yes':

                    # posta os dados do livro no Firebase
                    novo_post.set(dicionario_livro)
                    # exibe uma mensagem confirmando que os dados foram postados com sucesso
                    messagebox.showinfo('Cadastro de livros na minha estante', 'Livro inserido com sucesso!')

                    # função para limpar os campos
                    def limpar_campos():
                        titulo.delete(0, 'end')
                        autor.delete(0, 'end')
                        paginas.delete(0, 'end')
                        cidade_editora.delete(0, 'end')
                        editora.delete(0, 'end')
                        ano_edicao.delete(0, 'end')

                    # executa a função para deixar os campos limpos
                    limpar_campos()
                    window_add_books.focus()

                else:
                    # ToDo: função para voltar ao formulário
                    window_add_books.destroy()

            btn_adicionar = Button(window_add_books, text='INSERIR', width=14, font=fonte, bg='red',
                                   command=inserir_livro_estante).grid(row=7, column=1, sticky=W, padx=10, pady=10)

            btn_sair = Button(window_add_books, text='SAIR', width=14, font=fonte, bg='red',
                              command=window_add_books.destroy).grid(row=7, column=1, sticky=N, padx=10, pady=10)

        # =============================== TREEVIEW ===============================
        # cria a TreeView
        # style para configurar a Treeview
        style = ttk.Style(self.minha_bbt_window)
        style.theme_use("clam")

        tree = ttk.Treeview(self.minha_bbt_window, selectmode='browse',
                            column=('column1', 'column2', 'column3', 'column4', 'column5', 'column6'), show='headings')
        # define as colunas da Treeview
        tree.column('column1', width=350, minwidth=350, stretch=YES, anchor=N)
        tree.heading('#1', text='Título')
        tree.column('column2', width=250, minwidth=250, stretch=YES, anchor=N)
        tree.heading('#2', text='Autor')
        tree.column('column3', width=200, minwidth=200, stretch=YES, anchor=N)
        tree.heading('#3', text='Editora')
        tree.column('column4', width=100, minwidth=100, stretch=YES, anchor=N)
        tree.heading('#4', text='Cidade')
        tree.column('column5', width=100, minwidth=100, stretch=YES, anchor=N)
        tree.heading('#5', text='Ano da Edição')
        tree.column('column6', width=120, minwidth=120, stretch=YES, anchor=N)
        tree.heading('#6', text='Ano de aquisição')
        tree.grid(row=0, column=0)

        # pega a referência na database do Firebase
        referencia = db.reference()
        # pega os itens que estão catalogados na database
        livros_minha_estante = referencia.child('minhaBBT').get().items()
        total_livros_na_estante = 0

        # pega cada elemento (key) do Firebase
        for elemento in livros_minha_estante:
            # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
            dados = elemento[1]

            # insere os dados do Firesabe na TreeView
            tree.insert('', END, values=(
                dados['titulo'], dados['autor'], dados['editora'], dados['cidadeEditora'], dados['anoEdicao']))
            total_livros_na_estante += 1

        # LABEL
        # Label para exibir a quantidade de livros lidos no ano selecionado
        Label(self.minha_bbt_window, text='Total de livros na minha estante: ' + str(total_livros_na_estante),
              font='arial 20 bold', bg='red').grid(row=1, column=0, pady=10)

        # =============================== BUTTON ===============================
        fonte_btn = 'arial 15 bold'
        self.btn_cadastrar_livro = Button(self.minha_bbt_window, text='CADASTRAR', width=20, font=fonte_btn, bg='red',
                                          bd=5, command=formulario_add_books).grid(row=2, column=0, sticky=N, padx=10,
                                                                                   pady=10)

        self.btn_sair = Button(self.minha_bbt_window, text='SAIR', width=20, font=fonte_btn, bg='red', bd=5,
                               command=self.minha_bbt_window.destroy).grid(row=3, column=0, sticky=N, padx=10, pady=10)

        # =============================== EXECUÇÃO DA JANELA ===============================
        self.minha_bbt_window.mainloop()


try:
    LIVROS_LIDOS()
except:
    raise Exception('A janela não pode ser criada!')
