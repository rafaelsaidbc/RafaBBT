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
        self.bbt_window = Tk()
        self.bbt_window.configure(background='red')
        self.bbt_window.title('RAFA BBT | By Rafa Said')
        self.bbt_window.resizable(False, False)
        self.bbt_window.wm_iconbitmap('bbt.ico')

        # ========================== FUNÇÕES ========================== #
        # função para exibir a lista de livros que li em determinado ano
        def exibir_lista_lidos():
            # Cria o formulario para inserção dos dados
            formulario = Toplevel(bg='red')
            formulario.wm_iconbitmap('bbt.ico')
            formulario.title('RAFA BBT')

            # Evento On Click do botão Ok, para exibir a lista de livros no ano selecionado
            def exibir_lista():

                # pega o ano que está no spinner e converte para string
                ano = spinner.get()

                messagebox.showinfo('Livros lidos', 'Você selecionou ' + ano + ', clique OK para contiuar...')

                # mostra uma mensagem na janela informando o ano selecionado
                txt = 'Você selecionou: ' + spinner.get()
                # cria um Label para exibir as informações
                texto = Label(formulario, text=txt, bg='red')
                # localiza o Label na janela
                texto.grid(row=2, sticky=W, padx=20)
                # pega a referência na database do Firebase
                referencia = db.reference()
                # pega os itens que estão catalogados na database
                livros_lidos = referencia.child('livrosLidos').child(ano).get().items()
                # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
                janela_livros_lidos = Toplevel()
                # título da janela
                janela_livros_lidos.title('Livros lidos em ' + ano)
                janela_livros_lidos.configure(background='red')

                # cria a TreeView
                # style para configurar a Treeview
                style = ttk.Style(janela_livros_lidos)
                style.theme_use("clam")

                tree = ttk.Treeview(janela_livros_lidos, selectmode='browse',
                                    column=('column1', 'column2', 'column3', 'column4', 'column5'), show='headings')
                # define as colunas da Treeview
                tree.column('column1', width=350, minwidth=350, stretch=YES, anchor=N)
                tree.heading('#1', text='Título')
                tree.column('column2', width=250, minwidth=250, stretch=YES, anchor=N)
                tree.heading('#2', text='Autor')
                tree.column('column3', width=150, minwidth=150, stretch=YES, anchor=N)
                tree.heading('#3', text='Editora')
                tree.column('column4', width=100, minwidth=100, stretch=YES, anchor=N)
                tree.heading('#4', text='Cidade')
                tree.column('column5', width=100, minwidth=100, stretch=YES, anchor=N)
                tree.heading('#5', text='Ano da Edição')
                tree.grid(row=0, column=0)

                # pega os itens que estão catalogados na database
                livros_lidos = referencia.child('livrosLidos').child(ano).get().items()
                quantidade_livros_lidos = 0

                # pega cada elemento (key) do Firebase
                for elemento in livros_lidos:
                    # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
                    dados = elemento[1]

                    # insere os dados do Firesabe na TreeView
                    tree.insert('', END, values=(
                    dados['titulo'], dados['autor'], dados['editora'], dados['cidadeEditora'], dados['anoEdicao']))
                    quantidade_livros_lidos += 1

                # Label para exibir a quantidade de livros lidos no ano selecionado
                Label(janela_livros_lidos, text='Total de livros lidos em ' + ano + ': ' + str(quantidade_livros_lidos),
                      font='arial 15 bold', bg='red').grid(row=1, column=0, pady=10)

                # Evento On Click do botão Atualizar, para atualizar os dados de um livro lido
                def atualizar_livro_lido():

                    # obtem as informações do item selecionado na TreeView
                    tree.bind("<TreeviewSelect>")
                    titulo = tree.item(tree.selection())['values'][0]
                    messagebox.askquestion('RAFA BBT',
                                           'Você tem certeza que deseja atualizar as informações do livro "' + titulo + '"?')

                    reference_database = db.reference().child('livrosLidos')
                    dicionario_database = reference_database.get()
                    # pega cada elemento (key) do Firebase
                    for dados_db in dicionario_database.items():
                        dados_book = dados_db[1]
                        for chave, livro in dados_book.items():
                            if livro['titulo'] == titulo:
                                key_firebase = chave
                                break
                    referencia_atualizar = reference_database.child(ano).child(key_firebase).get().items()

                    # função para exibir o formulário de atualização do livro selecionado
                    def formulario_atualizar_livro():

                        janela_atualizar_livro = Toplevel()
                        janela_atualizar_livro.title('Atualização de livro')
                        janela_atualizar_livro.wm_iconbitmap('bbt.ico')
                        janela_atualizar_livro.configure(background='red')

                        for indice, informacao in referencia_atualizar:
                            if indice == "anoEdicao":
                                global autalizar_edicao_ano_lido
                                autalizar_edicao_ano_lido = informacao
                            if indice == 'autor':
                                global atualizar_autor_lido
                                atualizar_autor_lido = informacao
                            if indice == 'cidadeEditora':
                                global atualizar_cidade_editora_lido
                                atualizar_cidade_editora_lido = informacao
                            if indice == 'editora':
                                global atualizar_editora_lido
                                atualizar_editora_lido = informacao
                            if indice == 'fimLeitura':
                                global atualizar_fim_leitura_lido
                                atualizar_fim_leitura_lido = informacao
                            if indice == 'id_livro':
                                global atualizar_id_livro
                                atualizar_id_livro = informacao
                            if indice == 'inicioLeitura':
                                global atualizar_inicio_leitura_lido
                                atualizar_inicio_leitura_lido = informacao
                            if indice == 'paginas':
                                global atualizar_paginas_lidos
                                atualizar_paginas_lidos = informacao
                            if indice == 'titulo':
                                global atualizar_titulo_lido
                                atualizar_titulo_lido = informacao

                        # define as labels do formulário de atualização do livro
                        fonte = 'arial 12 bold'
                        Label(janela_atualizar_livro, text='Ano de leitura', font=fonte, bg='red').grid(row=0)
                        Label(janela_atualizar_livro, text='id livro', font=fonte, bg='red').grid(row=1)
                        Label(janela_atualizar_livro, text='Título', font=fonte, bg='red').grid(row=2)
                        Label(janela_atualizar_livro, text='Autor', font=fonte, bg='red').grid(row=3)
                        Label(janela_atualizar_livro, text='Páginas', font=fonte, bg='red').grid(row=4)
                        Label(janela_atualizar_livro, text='Início da leitura', font=fonte, bg='red').grid(row=5)
                        Label(janela_atualizar_livro, text='Fim da leitura', font=fonte, bg='red').grid(row=6)
                        Label(janela_atualizar_livro, text='Cidade da editora', font=fonte, bg='red').grid(row=7)
                        Label(janela_atualizar_livro, text='Editora', font=fonte, bg='red').grid(row=8)
                        Label(janela_atualizar_livro, text='Ano da edição', font=fonte, bg='red').grid(row=9)

                        # define as Entry do formulário com StringVar, formato permitido para as informações serem inseridas a partir dos dados recebidos do Firebase
                        fonte_entry = 'arial 15 bold'
                        ano_lido_entry = StringVar(janela_atualizar_livro, value=ano)
                        ano_leitura_atualizar_livro = Entry(janela_atualizar_livro, textvariable=ano_lido_entry,
                                                            width=40, font=fonte_entry)
                        id_livro_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_id_livro)
                        id_livro_atualizar_livro = Entry(janela_atualizar_livro, textvariable=id_livro_lido_entry,
                                                         width=40, font=fonte_entry)
                        titulo_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_titulo_lido)
                        titulo_atualizar_livro = Entry(janela_atualizar_livro, textvariable=titulo_lido_entry, width=40,
                                                       font=fonte_entry)
                        autor_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_autor_lido)
                        autor_atualizar_livro = Entry(janela_atualizar_livro, textvariable=autor_lido_entry, width=40,
                                                      font=fonte_entry)
                        paginas_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_paginas_lidos)
                        paginas_atualizar_livro = Entry(janela_atualizar_livro, textvariable=paginas_lido_entry,
                                                        width=40, font=fonte_entry)
                        inicio_leituro_lido_entry = StringVar(janela_atualizar_livro,
                                                              value=atualizar_inicio_leitura_lido)
                        inicio_leitura_atualizar_livro = Entry(janela_atualizar_livro,
                                                               textvariable=inicio_leituro_lido_entry,
                                                               width=40, font=fonte_entry)
                        fim_leitura_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_fim_leitura_lido)
                        fim_leitura_atualizar_livro = Entry(janela_atualizar_livro, textvariable=fim_leitura_lido_entry,
                                                            width=40, font=fonte_entry)
                        cidade_editora_lido_entry = StringVar(janela_atualizar_livro,
                                                              value=atualizar_cidade_editora_lido)
                        cidade_editora_atualizar_livro = Entry(janela_atualizar_livro,
                                                               textvariable=cidade_editora_lido_entry,
                                                               width=40, font=fonte_entry)
                        editora_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_editora_lido)
                        editora_atualizar_livro = Entry(janela_atualizar_livro, textvariable=editora_lido_entry,
                                                        width=40, font=fonte_entry)
                        ano_edicao_lido_entry = StringVar(janela_atualizar_livro, value=autalizar_edicao_ano_lido)
                        ano_edicao_atualizar_livro = Entry(janela_atualizar_livro, textvariable=ano_edicao_lido_entry,
                                                           width=40, font=fonte_entry)
                        # define a localização das informações no formulário/janela
                        ano_leitura_atualizar_livro.grid(row=0, column=1, padx=8, pady=10)
                        id_livro_atualizar_livro.grid(row=1, column=1, padx=8, pady=10)
                        titulo_atualizar_livro.grid(row=2, column=1, padx=8, pady=10)
                        autor_atualizar_livro.grid(row=3, column=1, padx=8, pady=10)
                        paginas_atualizar_livro.grid(row=4, column=1, padx=8, pady=10)
                        inicio_leitura_atualizar_livro.grid(row=5, column=1, padx=8, pady=10)
                        fim_leitura_atualizar_livro.grid(row=6, column=1, padx=8, pady=10)
                        cidade_editora_atualizar_livro.grid(row=7, column=1, padx=8, pady=10)
                        editora_atualizar_livro.grid(row=8, column=1, padx=8, pady=10)
                        ano_edicao_atualizar_livro.grid(row=9, column=1, padx=8, pady=10)

                        # função para inserir as informações atualizadas sobre o livro no Firebase
                        def inserir_atualizacao_livro_lido():
                            messagebox.askquestion('Atualização de livro',
                                                   'Você atualizará as informações. Tem certeza?')

                            # define a referência como a mesma key utilizada para recuperar os dados utilizados para preenchimento das Entry
                            referencia_atualizar_livro = referencia.child('livrosLidos').child(ano).child(
                                key_firebase)

                            # cria um dicionario com os dados do livro {id_livro, título, autor, páginas, início da leitura, fim da leitura, cidade da editora, editora, ano da edição}
                            dicionario_livro_atualizado = {
                                'id_livro': id_livro_atualizar_livro.get(),
                                'titulo': titulo_atualizar_livro.get(),
                                'autor': autor_atualizar_livro.get(),
                                'paginas': paginas_atualizar_livro.get(),
                                'inicioLeitura': inicio_leitura_atualizar_livro.get(),
                                'fimLeitura': fim_leitura_atualizar_livro.get(),
                                'cidadeEditora': cidade_editora_atualizar_livro.get(),
                                'editora': editora_atualizar_livro.get(),
                                'anoEdicao': ano_edicao_atualizar_livro.get(),
                            }
                            # posta os dados do livro no Firebase, na mesma key selecionada para atualização
                            referencia_atualizar_livro.set(dicionario_livro_atualizado)
                            # exibe uma mensagem de confirmação da atualização dos dados do livro
                            messagebox.showinfo('Atualização de livros lidos', 'Atualização realizada com sucesso!')

                        btn_inserir_atualizacao = Button(janela_atualizar_livro, text='ATUALIZAR',
                                                         command=inserir_atualizacao_livro_lido, font='arial 15 bold',
                                                         width=15, bg='red', bd=5).grid(row=10, column=1, pady=10,
                                                                                        padx=5, sticky=W)
                        btn_sair_atualizacao = Button(janela_atualizar_livro, text='SAIR',
                                                      command=janela_atualizar_livro.destroy, font='arial 15 bold',
                                                      width=15, bg='red', bd=5).grid(row=10, column=1, pady=10, padx=5,
                                                                                     sticky=E)

                    # abre a janela de atualização do livro
                    formulario_atualizar_livro()

                # botão para atualizar livro
                btn_update_book = Button(janela_livros_lidos, text="ATUALIZAR", command=atualizar_livro_lido, bd=5,
                                         fg='black', bg='red', font=('arial', 15, 'bold'), width=20).grid(row=2,
                                                                                                          column=0,
                                                                                                          pady=10,
                                                                                                          sticky=N)
                btn_sair = Button(janela_livros_lidos, text="SAIR", command=janela_livros_lidos.destroy, bd=5,
                                  fg='black', bg='red', font=('arial', 15, 'bold'), width=20).grid(row=3, column=0,
                                                                                                   pady=10, sticky=N)

            # função para exibir all books já lidos
            # Evento On Click do botão Ok, para exibir a lista de livros no ano selecionado
            def exibir_lista_todos():

                # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
                janela_livros_lidos = Toplevel()
                # título da janela
                janela_livros_lidos.title('Livros que li de 2013 a 2019')

                # cria a TreeView
                # style para configurar a Treeview
                style = ttk.Style(janela_livros_lidos)
                style.theme_use("clam")
                style.configure('Treeview', rowheight=30, background='#red')

                tree = ttk.Treeview(janela_livros_lidos, selectmode='browse',
                                    column=('column1', 'column2', 'column3', 'column4', 'column5', 'column6'),
                                    show='headings')
                # define as colunas da Treeview
                tree.column('column1', width=100, minwidth=100, stretch=YES, anchor=N)
                tree.heading('#1', text='Ano de leitura')
                tree.column('column2', width=350, minwidth=350, stretch=YES, anchor=N)
                tree.heading('#2', text='Título')
                tree.column('column3', width=250, minwidth=250, stretch=YES, anchor=N)
                tree.heading('#3', text='Autor')
                tree.column('column4', width=150, minwidth=150, stretch=YES, anchor=N)
                tree.heading('#4', text='Editora')
                tree.column('column5', width=100, minwidth=100, stretch=YES, anchor=N)
                tree.heading('#5', text='Cidade')
                tree.column('column6', width=100, minwidth=100, stretch=YES, anchor=N)
                tree.heading('#6', text='Ano da Edição')
                tree.grid(row=0, column=0)

                # pega a referência na database do Firebase
                referencia = db.reference()

                # pega os itens que estão catalogados na database
                livros_lidos = referencia.child('livrosLidos').get().items()
                total_lidos = 0

                # pega cada elemento (key) do Firebase
                for todos_livros_ano in livros_lidos:
                    dados_livro = todos_livros_ano[1]
                    for chave, livro in dados_livro.items():
                        tree.insert('', END, values=(
                        todos_livros_ano[0], livro['titulo'], livro['autor'], livro['editora'], livro['cidadeEditora'],
                        livro['anoEdicao']), tags='vermelho')
                        total_lidos += 1

                Label(janela_livros_lidos, text='Total de livros lidos entre 2013 e 2019: ' + str(total_lidos),
                      font='arial 10 bold').grid(row=1, column=0)

            # Cria componentes da janela de seleção do ano para exibir os livros lidos no ano selecionado
            descricao = Label(formulario, text="Selecione um ano entre 2013 e 2019", bg='red', font='arial 12 bold',
                              pady=10)
            # cria um spinner, do ano de 2013 ao ano de 2019
            spinner = Spinbox(formulario, from_=2013, to=2019)

            # ================================= VER TODOS OS LIVROS =================================
            btn_todos_livros = Button(formulario, text="TODOS OS LIVROS", command=exibir_lista_todos, bd=5, fg='black',
                                      bg='red', font=('arial', 10, 'bold'), width=20)

            # cria um Button, com o comando exibir_lista para exibir a lista de livros no ano selecionado
            btn_exibir_lista = Button(formulario, text="OK", command=exibir_lista, bd=5, fg='black', bg='red',
                                      font=('arial', 10, 'bold'), width=20)

            # volta à janela anterior
            btn_sair = Button(formulario, text='SAIR', command=formulario.destroy, bd=5, fg='black', bg='red',
                              font=('arial', 10, 'bold'), width=20)

            # Alinha componentes na tela
            descricao.grid(row=0, sticky=N, padx=20)
            spinner.grid(row=1, sticky=N, columnspan=20, padx=20, pady=20)
            btn_exibir_lista.grid(row=3, sticky=N, padx=2, pady=10)
            btn_todos_livros.grid(row=4, sticky=N, padx=2, pady=10)
            btn_sair.grid(row=5, sticky=N, padx=2, pady=10)

            # executa a janela de seleção do ano a ser exibido a lista de livros lidos
            mainloop()

        # função para adicionar livros lidos no Firebase
        def formulario_adicionar_livros_lidos():

            fonte = 'arial 12 bold'

            janela_cadastro_livros = Toplevel()
            janela_cadastro_livros.title('Cadastro de livros lidos')
            janela_cadastro_livros.wm_iconbitmap('bbt.ico')
            janela_cadastro_livros.configure(background='red')

            Label(janela_cadastro_livros, text='Ano de leitura', font=fonte, bg='red').grid(row=0, pady=5)
            Label(janela_cadastro_livros, text='id livro', font=fonte, bg='red').grid(row=1, pady=5)
            Label(janela_cadastro_livros, text='Título', font=fonte, bg='red').grid(row=2, pady=5)
            Label(janela_cadastro_livros, text='Autor', font=fonte, bg='red').grid(row=3, pady=5)
            Label(janela_cadastro_livros, text='Páginas', font=fonte, bg='red').grid(row=4, pady=5)
            Label(janela_cadastro_livros, text='Início da leitura', font=fonte, bg='red').grid(row=5, pady=5)
            Label(janela_cadastro_livros, text='Fim da leitura', font=fonte, bg='red').grid(row=6, pady=5)
            Label(janela_cadastro_livros, text='Cidade da editora', font=fonte, bg='red').grid(row=7, pady=5)
            Label(janela_cadastro_livros, text='Editora', font=fonte, bg='red').grid(row=8, pady=5)
            Label(janela_cadastro_livros, text='Ano da edição', font=fonte, bg='red').grid(row=9, pady=5)

            fonte_entry = 'arial 15 bold'
            global ano_leitura_lido
            ano_leitura_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            ano_leitura_lido.grid(row=0, column=1)
            global id_livro_lido
            id_livro_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            id_livro_lido.grid(row=1, column=1)
            global titulo_lido
            titulo_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            titulo_lido.grid(row=2, column=1)
            global autor_lido
            autor_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            autor_lido.grid(row=3, column=1)
            global paginas_lido
            paginas_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            paginas_lido.grid(row=4, column=1)
            global inicio_leitura_lido
            inicio_leitura_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            inicio_leitura_lido.grid(row=5, column=1)
            global fim_leitura_lido
            fim_leitura_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            fim_leitura_lido.grid(row=6, column=1)
            global cidade_editora_lido
            cidade_editora_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            cidade_editora_lido.grid(row=7, column=1)
            global editora_lido
            editora_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            editora_lido.grid(row=8, column=1)
            global ano_edicao_lido
            ano_edicao_lido = Entry(janela_cadastro_livros, width=40, font=fonte_entry)
            ano_edicao_lido.grid(row=9, column=1)

            # função para inserir livros lidos no Firebase
            def inserir_livros_lidos():

                # obtém a referência da database no Firebase
                referencia = firebase_admin.db.reference()

                # obtém a referência da child livrosLidos e armazena na variável postar_livro
                postar_livro = referencia.child('livrosLidos').child(ano_leitura_lido.get())

                # cria a instância para postar um livro no Firebase
                novo_post = postar_livro.push()

                # cria um dicionario com os dados do livro {id_livro, título, autor, páginas, início da leitura, fim da leitura, cidade da editora, editora, ano da edição}
                dicionario_livro = {
                    'id_livro': id_livro_lido.get(),
                    'titulo': titulo_lido.get(),
                    'autor': autor_lido.get(),
                    'paginas': paginas_lido.get(),
                    'inicioLeitura': inicio_leitura_lido.get(),
                    'fimLeitura': fim_leitura_lido.get(),
                    'cidadeEditora': cidade_editora_lido.get(),
                    'editora': editora_lido.get(),
                    'anoEdicao': ano_edicao_lido.get(),
                }

                add_book_msg_box = messagebox.askquestion('Inserir livro lido',
                                                          'Você tem certeza que deseja inserir o livro "' + titulo_lido.get() + '" no banco de dados?')

                if add_book_msg_box == 'yes':

                    # posta os dados do livro no Firebase
                    novo_post.set(dicionario_livro)
                    # exibe uma mensagem confirmando que os dados foram postados com sucesso
                    messagebox.showinfo('Cadastro de livros lidos', 'Livro inserido com sucesso!')

                    # função para limpar os campos
                    def limpar_campos():
                        id_livro_lido.delete(0, 'end')
                        titulo_lido.delete(0, 'end')
                        autor_lido.delete(0, 'end')
                        paginas_lido.delete(0, 'end')
                        inicio_leitura_lido.delete(0, 'end')
                        fim_leitura_lido.delete(0, 'end')
                        cidade_editora_lido.delete(0, 'end')
                        editora_lido.delete(0, 'end')
                        ano_edicao_lido.delete(0, 'end')

                    # executa a função para deixar os campos limpos
                    limpar_campos()
                    janela_cadastro_livros.focus()

                else:
                    # ToDo: função para voltar ao formulário
                    janela_cadastro_livros.destroy()

            btn_adicionar = Button(janela_cadastro_livros, text='INSERIR', width=14, font=fonte, bg='red', bd=5,
                                   command=inserir_livros_lidos).grid(row=10, column=1, sticky=W, padx=10, pady=10)

            btn_sair = Button(janela_cadastro_livros, text='SAIR', width=14, font=fonte, bg='red', bd=5,
                              command=janela_cadastro_livros.destroy).grid(row=10, column=1, sticky=N, padx=10, pady=10)

        # ============================ LABELS ============================
        Label(self.bbt_window, text='LIVROS LIDOS POR RAFA SAID', width=25, bg='red', fg='black',
              font='arial 30 bold').grid(row=0, column=0, sticky=W, padx=10, pady=10)

        # ============================ BUTTON ============================
        self.livros_lidos = Button(self.bbt_window, text='EXIBIR LISTA', width=20, bg='red', fg='black',
                                   font='arial 20 bold', bd=5, command=exibir_lista_lidos).grid(row=1, column=0,
                                                                                                sticky=N, padx=5,
                                                                                                pady=8)

        self.cadastrar_livros_lidos = Button(self.bbt_window, text='CADASTRAR', width=20, bg='red', fg='black',
                                             font='arial 20 bold', bd=5,
                                             command=formulario_adicionar_livros_lidos).grid(row=2, column=0, sticky=N,
                                                                                             padx=5, pady=8)

        self.sair = Button(self.bbt_window, text='SAIR', width=20, bg='red', fg='black', font='arial 20 bold', bd=5,
                           command=self.bbt_window.destroy).grid(row=3, column=0, sticky=N, padx=5, pady=8)

        # ========== EXECUÇÃO DA JANELA ==========
        self.bbt_window.mainloop()


try:
    LIVROS_LIDOS()
except:
    raise Exception('A janela não pode ser criada!')
