import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import *


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

# função para adicionar livros na lista de livros que quero ler
def adicionar_livros_lista():
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
    messagebox.showinfo('Lista de livros a serem lidos', 'Livro inserido com sucesso!')


#função da janela de cadastro dos livros que quero ler
def formulario_cadastro_livros_ler():
    janela_livros_ler = Toplevel()
    janela_livros_ler.title('Cadastro de livros na lista de leitura')
    Label(janela_livros_ler, text='Título').grid(row=0)
    Label(janela_livros_ler, text='Autor').grid(row=1)

    global titulo_livros_ler
    titulo_livros_ler = Entry(janela_livros_ler)
    titulo_livros_ler.grid(row=0, column=1)
    global autor_livros_ler
    autor_livros_ler = Entry(janela_livros_ler)
    autor_livros_ler.grid(row=1, column=1)

    btn_adicionar = Button(janela_livros_ler, text='Inserir', command=adicionar_livros_lista).grid(row=9, column=1,
                                                                                                   sticky=W, pady=4)


#função para exibir a lista de livros que quero ler
def exibir_lista_ler():
    # pega a referência na database do Firebase
    referencia = db.reference()
    # pega os itens que estão catalogados na database
    livros_ler = referencia.child('livrosLer').get().items()
    # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
    janela_livros_ler = Toplevel()
    # título da janela
    janela_livros_ler.title('LISTA DE LIVROS QUE DESEJO LER')
    # cria a variável t do tipo scrolledtext (uma caixa de texto com barra de rolagem) para inserir os dados
    t = scrolledtext.ScrolledText(janela_livros_ler)
    # pega cada elemento (key) do Firebase
    for elemento in livros_ler:
        # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
        dados = elemento[1]
        # para cada chave, valor do dicionário dos dados
        for chave, valor in dados.items():
            # se a chave for igual a autor
            if chave == 'autor':
                # armazena o nome do autor(es) na variável autor
                autor = 'Autor(es): ' + valor
            # se a chave for igual a título
            if chave == 'titulo':
                # armazena o título do livro na variável título
                titulo = 'Título: ' + valor
                # insere as informações numa lista com a formatação aqui definida
                t.insert(END, '\n' + '\n' + autor + '\n' + titulo + '\n' + '\n' + '*' * 50)
    # empacota a variável t para ser exibida
    t.pack()


# função para deletar registros da lista de livros a serem lidos
def deletar_livros_ler():
    janela = Toplevel()
    label = tk.Label(janela, text='Selecione o livro para deletar', font=FONTE)
    label.pack(pady=10, padx=10)
    listbox = Listbox(janela, selectmod=SINGLE, width=60)
    # pega a referência na database do Firebase
    referencia = db.reference()
    # pega os itens que estão catalogados na database
    livros_ler = referencia.child('livrosLer').get().items()
    # pega cada elemento (key) do Firebase
    for elemento in livros_ler:
        # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
        dados = elemento[1]
        # para cada chave, valor do dicionário dos dados
        for chave, valor in dados.items():
            if chave == 'autor':
                autor = 'Autor: ' + valor
            # se a chave for igual a título
            if chave == 'titulo':
                # armazena o título do livro na variável título
                titulo = 'Título: ' + valor
                # insere as informações numa lista com a formatação aqui definida
                listbox.insert(END, titulo + ', ' + autor)
    listbox.pack()

    # função para deletar a opção selecionada na listbox
    def deletar():
        # obtém a posição do item selecionado na lista
        posicao = int(listbox.curselection()[0])
        # cria a variável selecionado com o título do livro selecionado na listbox
        selecionado = listbox.get(posicao)
        # cria a variável valor_editado para ficar igual ao título do livro selecionado para deletar
        valor_editado = 'Título: ' + valor + ', ' + autor
        # se o valor_editado for igual ao selecionado na listbox executa o bloco
        if valor_editado == selecionado:
            # pega a key do Firebase, que corresponde ao elemento na posição [0]
            key_firebase = elemento[0]
            # cria a variável deletar_referencia com o caminho da key selecionada para ser deletada
            deletar_referencia = referencia.child('livrosLer').child(key_firebase)
            # deleta a key do título do livro que foi selecionado na listbox
            deletar_referencia.delete()
            messagebox.showinfo('Lista de livros a serem lidos', 'Livro deletado com sucesso!')
            janela.destroy()

    btn_deletar = Button(janela, text='Deletar', command=deletar)
    btn_deletar.pack()


#função para exibir a lista de livros que li em determinado ano
def exibir_lista_lidos():
    # Cria formulario
    formulario = Toplevel()
    formulario.title = 'Escolha um ano'

    # Evento On Click do botão Ok
    def exibir_lista():
        # pega o ano que está no spinner e converte para string
        ano = spinner.get()
        # mostra uma mensagem na janela informando o ano selecionado
        txt = 'Você selecionou: ' + spinner.get()
        # cria um Label para exibir as informações
        texto = Label(formulario, text=txt)
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
        # cria a variável t do tipo scrolledtext para inserir os dados
        t = scrolledtext.ScrolledText(janela_livros_lidos)
        # pega cada elemento (key) do Firebase
        for elemento in livros_lidos:
            # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
            dados = elemento[1]
            # para cada chave, valor do dicionário dos dados
            for chave, valor in dados.items():
                if chave == 'anoEdicao':
                    ano_edicao = 'Ano de Edição: ' + valor
                # se a chave for igual a autor
                if chave == 'autor':
                    # armazena o nome do autor(es) na variável autor
                    autor = 'Autor(es): ' + valor
                if chave == 'cidadeEditora':
                    cidade_editora = valor
                if chave == 'editora':
                    editora = 'Editora: ' + valor
                if chave == 'fimLeitura':
                    fim_leitura = 'Término da leitura: ' + valor
                if chave == 'id_livro':
                    id_livro = valor
                if chave == 'inicioLeitura':
                    inicio_leitura = 'Início da leitura: ' + valor
                if chave == 'paginas':
                    paginas = 'Páginas: ' + valor
                # se a chave for igual a título
                if chave == 'titulo':
                    # armazena o título do livro na variável título
                    titulo = 'Título: ' + valor
                    # insere as informações numa lista com a formatação aqui definida
                    t.insert(END,
                             '\n' + '\n' + id_livro + '\n' + autor + '\n' + titulo + '\n' + paginas + '\n' + inicio_leitura + '\n' + fim_leitura + '\n' + editora + ', ' + cidade_editora + '\n' + ano_edicao + '\n' + '\n' + '*' * 50)
        # empacota a variável t para ser exibida
        t.pack()

    # Evento On Click do botão Atualizar
    def janela_atualizar_livro_lido():
        # pega o ano que está no spinner e converte para string
        ano = spinner.get()
        # mostra uma mensagem na janela informando o ano selecionado
        txt = 'Você selecionou: ' + spinner.get()
        # cria um Label para exibir as informações
        texto = Label(formulario, text=txt)
        # localiza o Label na janela
        texto.grid(row=2, sticky=W, padx=20)
        # pega a referência na database do Firebase
        referencia = db.reference()
        # pega os itens que estão catalogados na database
        livros_lidos_atualizar = referencia.child('livrosLidos').child(ano).get().items()
        # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
        janela_livros_lidos = Toplevel()
        # título da janela
        janela_livros_lidos.title('Livros lidos em ' + ano)
        # cria a variável t do tipo scrolledtext para inserir os dados
        listbox = Listbox(janela_livros_lidos, selectmod=SINGLE, width=60)
        # pega cada elemento (key) do Firebase
        for elemento in livros_lidos_atualizar:
            # pega a posição [1] do elemento (que se refere aos dados de título e autor, a posição [0] se refere à key do Firebase
            dados = elemento[1]
            # para cada chave, valor do dicionário dos dados
            for chave, valor in dados.items():
                # se a chave for igual a título
                if chave == 'titulo':
                    # armazena o título do livro na variável título
                    titulo = 'Título: ' + valor
                    # insere as informações numa lista com a formatação aqui definida
                    listbox.insert(END, titulo)
        listbox.pack()

        # função para atualizar o livro selecionado
        def formulario_atualizar_livro_selecionado():
            janela_atualizar_livro = Toplevel()
            janela_atualizar_livro.title('Atualização de livro')

            # função para atualizar a opção selecionada na listbox
            def atualizar():
                # obtém a posição do item selecionado na lista
                posicao = int(listbox.curselection()[0])
                # cria a variável selecionado com o título do livro selecionado na listbox
                selecionado_listbox = listbox.get(posicao)
                selecionado = selecionado_listbox[8:]

                # pega a key do Firebase, que corresponde ao elemento na posição [0]
                dados_firebase = referencia.child('livrosLidos').child(ano).get().items()
                for chave, dicionario in dados_firebase:
                    for item, valor in dicionario.items():
                        if valor == selecionado:
                            # cria a variável deletar_referencia com o caminho da key selecionada para ser deletada
                            global key_firebase_atualizar_livro
                            key_firebase_atualizar_livro = chave
                            pegar_referencia = referencia.child('livrosLidos').child(ano).child(
                                key_firebase_atualizar_livro).get().items()
                            for indice, informacao in pegar_referencia:
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

            atualizar()

            Label(janela_atualizar_livro, text='Ano de leitura').grid(row=0)
            Label(janela_atualizar_livro, text='id livro').grid(row=1)
            Label(janela_atualizar_livro, text='Título').grid(row=2)
            Label(janela_atualizar_livro, text='Autor').grid(row=3)
            Label(janela_atualizar_livro, text='Páginas').grid(row=4)
            Label(janela_atualizar_livro, text='Início da leitura').grid(row=5)
            Label(janela_atualizar_livro, text='Fim da leitura').grid(row=6)
            Label(janela_atualizar_livro, text='Cidade da editora').grid(row=7)
            Label(janela_atualizar_livro, text='Editora').grid(row=8)
            Label(janela_atualizar_livro, text='Ano da edição').grid(row=9)

            ano_lido_entry = StringVar(janela_atualizar_livro, value=ano)
            ano_leitura_atualizar_livro = Entry(janela_atualizar_livro, textvariable=ano_lido_entry, width=40)
            id_livro_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_id_livro)
            id_livro_atualizar_livro = Entry(janela_atualizar_livro, textvariable=id_livro_lido_entry, width=40)
            titulo_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_titulo_lido)
            titulo_atualizar_livro = Entry(janela_atualizar_livro, textvariable=titulo_lido_entry, width=40)
            autor_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_autor_lido)
            autor_atualizar_livro = Entry(janela_atualizar_livro, textvariable=autor_lido_entry, width=40)
            paginas_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_paginas_lidos)
            paginas_atualizar_livro = Entry(janela_atualizar_livro, textvariable=paginas_lido_entry, width=40)
            inicio_leituro_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_inicio_leitura_lido)
            inicio_leitura_atualizar_livro = Entry(janela_atualizar_livro, textvariable=inicio_leituro_lido_entry,
                                                   width=40)
            fim_leitura_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_fim_leitura_lido)
            fim_leitura_atualizar_livro = Entry(janela_atualizar_livro, textvariable=fim_leitura_lido_entry, width=40)
            cidade_editora_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_cidade_editora_lido)
            cidade_editora_atualizar_livro = Entry(janela_atualizar_livro, textvariable=cidade_editora_lido_entry,
                                                   width=40)
            editora_lido_entry = StringVar(janela_atualizar_livro, value=atualizar_editora_lido)
            editora_atualizar_livro = Entry(janela_atualizar_livro, textvariable=editora_lido_entry, width=40)
            ano_edicao_lido_entry = StringVar(janela_atualizar_livro, value=autalizar_edicao_ano_lido)
            ano_edicao_atualizar_livro = Entry(janela_atualizar_livro, textvariable=ano_edicao_lido_entry, width=40)
            ano_leitura_atualizar_livro.grid(row=0, column=1)
            id_livro_atualizar_livro.grid(row=1, column=1)
            titulo_atualizar_livro.grid(row=2, column=1)
            autor_atualizar_livro.grid(row=3, column=1)
            paginas_atualizar_livro.grid(row=4, column=1)
            inicio_leitura_atualizar_livro.grid(row=5, column=1)
            fim_leitura_atualizar_livro.grid(row=6, column=1)
            cidade_editora_atualizar_livro.grid(row=7, column=1)
            editora_atualizar_livro.grid(row=8, column=1)
            ano_edicao_atualizar_livro.grid(row=9, column=1)

            def inserir_atualizacao_livro_lido():
                referencia_atualizar_livro = referencia.child('livrosLidos').child(ano).child(
                    key_firebase_atualizar_livro)

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
                # posta os dados do livro no Firebase
                referencia_atualizar_livro.set(dicionario_livro_atualizado)
                messagebox.showinfo('Atualização de livros lidos', 'Atualização realizada com sucesso!')

            btn_inserir_atualizacao = Button(janela_atualizar_livro, text='Atualizar',
                                             command=inserir_atualizacao_livro_lido)
            btn_inserir_atualizacao.grid(row=10, column=1)

        btn_atualizar_livro = Button(janela_livros_lidos, text='Atualizar',
                                     command=formulario_atualizar_livro_selecionado)
        btn_atualizar_livro.pack()



    # Cria componentes da janela de seleção do ano para exibir os livros lidos no ano selecionado
    descricao = Label(formulario, text="Selecione um ano entre 2013 e 2019")
    # cria um spinner, de ano de 2013 ao ano de 2019
    spinner = Spinbox(formulario, from_=2013, to=2019)
    # cria um Button, com o comando exibir_lista para exibir a lista de livros no ano selecionado
    botao = Button(formulario, text="Ok", command=exibir_lista)
    # button para atualizar um livro lido
    btn_atualizar = Button(formulario, text='Atualizar', command=janela_atualizar_livro_lido)
    # volta à janela anterior
    btn_voltar = Button(formulario, text='Voltar', command=formulario.destroy)
    # Alinha componentes na tela
    descricao.grid(row=0, sticky=W, padx=20)
    spinner.grid(row=1, sticky=W, padx=20)
    botao.grid(row=3, sticky=W, padx=20, pady=10)
    btn_atualizar.grid(row=3, sticky=W, padx=50)
    btn_voltar.grid(row=3, sticky=W, padx=110)
    # executa a janela de seleção do ano a ser exibido a lista de livros lidos
    mainloop()


#função para inserir livros lidos no Firebase
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
    # posta os dados do livro no Firebase
    novo_post.set(dicionario_livro)
    messagebox.showinfo('Cadastro de livros lidos', 'Livro inserido com sucesso!')

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

    limpar_campos()


#função para adicionar livros lidos no Firebase
def formulario_adicionar_livros_lidos():
    janela_cadastro_livros = Toplevel()
    janela_cadastro_livros.title('Cadastro de livros lidos')
    Label(janela_cadastro_livros, text='Ano de leitura').grid(row=0)
    Label(janela_cadastro_livros, text='id livro').grid(row=1)
    Label(janela_cadastro_livros, text='Título').grid(row=2)
    Label(janela_cadastro_livros, text='Autor').grid(row=3)
    Label(janela_cadastro_livros, text='Páginas').grid(row=4)
    Label(janela_cadastro_livros, text='Início da leitura').grid(row=5)
    Label(janela_cadastro_livros, text='Fim da leitura').grid(row=6)
    Label(janela_cadastro_livros, text='Cidade da editora').grid(row=7)
    Label(janela_cadastro_livros, text='Editora').grid(row=8)
    Label(janela_cadastro_livros, text='Ano da edição').grid(row=9)

    global ano_leitura_lido
    ano_leitura_lido = Entry(janela_cadastro_livros, width=40)
    ano_leitura_lido.grid(row=0, column=1)
    global id_livro_lido
    id_livro_lido = Entry(janela_cadastro_livros, width=40)
    id_livro_lido.grid(row=1, column=1)
    global titulo_lido
    titulo_lido = Entry(janela_cadastro_livros, width=40)
    titulo_lido.grid(row=2, column=1)
    global autor_lido
    autor_lido = Entry(janela_cadastro_livros, width=40)
    autor_lido.grid(row=3, column=1)
    global paginas_lido
    paginas_lido = Entry(janela_cadastro_livros, width=40)
    paginas_lido.grid(row=4, column=1)
    global inicio_leitura_lido
    inicio_leitura_lido = Entry(janela_cadastro_livros, width=40)
    inicio_leitura_lido.grid(row=5, column=1)
    global fim_leitura_lido
    fim_leitura_lido = Entry(janela_cadastro_livros, width=40)
    fim_leitura_lido.grid(row=6, column=1)
    global cidade_editora_lido
    cidade_editora_lido = Entry(janela_cadastro_livros, width=40)
    cidade_editora_lido.grid(row=7, column=1)
    global editora_lido
    editora_lido = Entry(janela_cadastro_livros, width=40)
    editora_lido.grid(row=8, column=1)
    global ano_edicao_lido
    ano_edicao_lido = Entry(janela_cadastro_livros, width=40)
    ano_edicao_lido.grid(row=9, column=1)

    btn_adicionar = Button(janela_cadastro_livros, text='Inserir', command=inserir_livros_lidos).grid(row=10, column=1,
                                                                                                      sticky=W, pady=4)


# função para inserir livros que tenho em casa no Firebase
def inserir_livros_estante():
    # obtém a referência da database no Firebase
    referencia = firebase_admin.db.reference()
    # obtém a referência da child minhaBBT e armazena na variável postar_livro
    postar_livro = referencia.child('minhaBBT')

    # cria a instância para postar um livro no Firebase
    novo_post = postar_livro.push()

    # cria um dicionario com os dados do livro {id_livro, título, autor, páginas, início da leitura, fim da leitura, cidade da editora, editora, ano da edição}
    dicionario_livro = {
        'titulo': titulo_estante.get(),
        'autor': autor_estante.get(),
        'paginas': paginas_estante.get(),
        'cidadeEditora': cidade_editora_estante.get(),
        'editora': editora_estante.get(),
        'anoEdicao': ano_edicao_estante.get(),
    }
    # posta os dados do livro no Firebase
    novo_post.set(dicionario_livro)


# função para adicionar livros da minha estante no Firebase
def formulario_adicionar_livros_estante():
    janela_cadastro_livros_estante = Toplevel()
    janela_cadastro_livros_estante.title('Cadastro de livros lidos')
    Label(janela_cadastro_livros_estante, text='Título').grid(row=0)
    Label(janela_cadastro_livros_estante, text='Autor').grid(row=1)
    Label(janela_cadastro_livros_estante, text='Páginas').grid(row=2)
    Label(janela_cadastro_livros_estante, text='Cidade da editora').grid(row=3)
    Label(janela_cadastro_livros_estante, text='Editora').grid(row=4)
    Label(janela_cadastro_livros_estante, text='Ano da edição').grid(row=5)

    global titulo_estante
    titulo_estante = Entry(janela_cadastro_livros_estante)
    titulo_estante.grid(row=0, column=1)
    global autor_estante
    autor_estante = Entry(janela_cadastro_livros_estante)
    autor_estante.grid(row=1, column=1)
    global paginas_estante
    paginas_estante = Entry(janela_cadastro_livros_estante)
    paginas_estante.grid(row=2, column=1)
    global cidade_editora_estante
    cidade_editora_estante = Entry(janela_cadastro_livros_estante)
    cidade_editora_estante.grid(row=3, column=1)
    global editora_estante
    editora_estante = Entry(janela_cadastro_livros_estante)
    editora_estante.grid(row=4, column=1)
    global ano_edicao_estante
    ano_edicao_estante = Entry(janela_cadastro_livros_estante)
    ano_edicao_estante.grid(row=5, column=1)

    btn_adicionar = Button(janela_cadastro_livros_estante, text='Inserir', command=inserir_livros_estante).grid(row=7,
                                                                                                                column=1,
                                                                                                                sticky=W,
                                                                                                                pady=4)


# função para exibir a lista de livros que tenho na minha estante
def exibir_lista_estante():
    # pega a referência na database do Firebase
    referencia = db.reference()
    # pega os itens que estão catalogados na database
    livros_estante = referencia.child('minhaBBT').get().items()
    # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
    janela_livros_estante = Toplevel()
    # título da janela
    janela_livros_estante.title('LISTA DE LIVROS QUE TENHO EM CASA')
    # cria a variável t do tipo scrolledtext para inserir os dados
    t = scrolledtext.ScrolledText(janela_livros_estante)
    # pega cada elemento (key) do Firebase
    for elemento in livros_estante:
        # pega a posição [1] do elemento (que se refere aos dados do livro (autor, título, editora, etc.), a posição [0] se refere à key do Firebase
        dados = elemento[1]
        # para cada chave, valor do dicionário dos dados
        for chave, valor in dados.items():
            if chave == 'anoEdicao':
                ano_edicao = valor
            # se a chave for igual a autor
            if chave == 'autor':
                # armazena o nome do autor(es) na variável autor
                autor = 'Autor(es): ' + valor
            if chave == 'cidadeEditora':
                cidade_editora = valor
            if chave == 'editora':
                editora = 'Editora: ' + valor
            if chave == 'paginas':
                paginas = 'Páginas: ' + valor
            # se a chave for igual a título
            if chave == 'titulo':
                # armazena o título do livro na variável título
                titulo = 'Título: ' + valor
                # insere as informações numa lista com a formatação aqui definida
                t.insert(END,
                         '\n' + titulo + '\n' + autor + '\n' + paginas + '\n' + editora + ', ' + cidade_editora + ', ' + ano_edicao + '\n' + '\n' + '*' * 50)
    # empacota a variável t para ser exibida
    t.pack()


#define a fonte que será usada nos botões das páginas
FONTE = ("Verdana", 12)


#classe principal do programa
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
        for F in (PaginaPrincipal, PaginaListaLer, PaginaLidos, PaginaBbt):
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
        # define o título da janela
        self.winfo_toplevel().title('Rafa BBT')
        label = tk.Label(self, text='BBT do Rafael Said', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_livros_ler = tk.Button(self, text='Livros que quero ler', command= lambda: controller.show_frame(PaginaListaLer))
        btn_livros_ler.pack()

        btn_livros_lidos = tk.Button(self, text='Livros lidos', command=lambda: controller.show_frame(PaginaLidos))
        btn_livros_lidos.pack()

        btn_minha_bbt = tk.Button(self, text='Minha BBT', command=lambda: controller.show_frame(PaginaBbt))
        btn_minha_bbt.pack()


#classe da lista de livros a serem lidos
class PaginaListaLer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Lista de livros a serem lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_exibir = tk.Button(self, text='Exibir lista de leitura', command=exibir_lista_ler)
        btn_exibir.pack()

        btn_cadastrar = tk.Button(self, text='Cadastrar livro', command=formulario_cadastro_livros_ler)
        btn_cadastrar.pack()

        btn_deletar = tk.Button(self, text='Deletar livro', command=deletar_livros_ler)
        btn_deletar.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()


#classe da lista de livros lidos, separadas por ano
class PaginaLidos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Livros lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_exibir = tk.Button(self, text='Exibir lista', command=exibir_lista_lidos)
        btn_exibir.pack()

        btn_cadastrar = tk.Button(self, text='Cadastrar', command=formulario_adicionar_livros_lidos)
        btn_cadastrar.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()


#classe de catalogação dos livros que tenho em casa
class PaginaBbt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Minha BBT', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_exibir = tk.Button(self, text='Exibir estante de livros', command=exibir_lista_estante)
        btn_exibir.pack()

        btn_cadastrar = tk.Button(self, text='Cadastrar livro', command=formulario_adicionar_livros_estante)
        btn_cadastrar.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()

app = BbtRafa()
app.mainloop()