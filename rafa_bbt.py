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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter as tk
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


#função da janela de cadastro dos livros que quero ler
def janela_cadastro_livros_ler():
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


# função para exibir a lista de livros que quero ler
def exibir_lista_ler():
    # pega a referência na database do Firebase
    referencia = db.reference()
    # pega os itens que estão catalogados na database
    livros_ler = referencia.child('livrosLer').get().items()
    # cria uma janela Toplevel (que irá aparecer após clicar no botão correspondente)
    janela_livros_ler = Toplevel()
    # título da janela
    janela_livros_ler.title('LISTA DE LIVROS QUE DESEJO LER')
    # cria a variável t do tipo Text para inserir os dados
    t = Text(janela_livros_ler)
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


# função para exibir a lista de livros que li em determinado ano
def exibir_lista_lidos():
    # Cria formulario
    formulario = Toplevel()
    formulario.title = 'Escolha um ano'

    # Evento On Click do botão
    def clique():
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
        janela_livros_lidos.title('LISTA DE LIVROS QUE DESEJO LER')
        # cria a variável t do tipo Text para inserir os dados
        t = Text(janela_livros_lidos)
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

    # Cria componentes da janela de seleção do ano para exibir os livros lidos no ano selecionado
    descricao = Label(formulario, text="Selecione um ano entre 2013 e 2019")
    # cria um spinner, de ano de 2013 ao ano de 2019
    spinner = Spinbox(formulario, from_=2013, to=2019)
    # cria um Button, com o comando clique para exibir a lista de livros no ano selecionado
    botao = Button(formulario, text="Ok", command=clique)
    # Alinha componentes na tela
    descricao.grid(row=0, sticky=W, padx=20)
    spinner.grid(row=1, sticky=W, padx=20)
    botao.grid(row=3, sticky=W, padx=20, pady=10)

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


# função para adicionar livros lidos no Firebase
def adicionar_livros_lidos():
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
    ano_leitura_lido = Entry(janela_cadastro_livros)
    ano_leitura_lido.grid(row=0, column=1)
    global id_livro_lido
    id_livro_lido = Entry(janela_cadastro_livros)
    id_livro_lido.grid(row=1, column=1)
    global titulo_lido
    titulo_lido = Entry(janela_cadastro_livros)
    titulo_lido.grid(row=2, column=1)
    global autor_lido
    autor_lido = Entry(janela_cadastro_livros)
    autor_lido.grid(row=3, column=1)
    global paginas_lido
    paginas_lido = Entry(janela_cadastro_livros)
    paginas_lido.grid(row=4, column=1)
    global inicio_leitura_lido
    inicio_leitura_lido = Entry(janela_cadastro_livros)
    inicio_leitura_lido.grid(row=5, column=1)
    global fim_leitura_lido
    fim_leitura_lido = Entry(janela_cadastro_livros)
    fim_leitura_lido.grid(row=6, column=1)
    global cidade_editora_lido
    cidade_editora_lido = Entry(janela_cadastro_livros)
    cidade_editora_lido.grid(row=7, column=1)
    global editora_lido
    editora_lido = Entry(janela_cadastro_livros)
    editora_lido.grid(row=8, column=1)
    global ano_edicao_lido
    ano_edicao_lido = Entry(janela_cadastro_livros)
    ano_edicao_lido.grid(row=9, column=1)

    btn_adicionar = Button(janela_cadastro_livros, text='Inserir', command=inserir_livros_lidos).grid(row=10, column=1,
                                                                                                      sticky=W, pady=4)

FONTE = ("Verdana", 12)


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
        label = tk.Label(self, text='BBT do Rafael Said', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_livros_ler = tk.Button(self, text='Livros que quero ler', command= lambda: controller.show_frame(PaginaListaLer))
        btn_livros_ler.pack()

        btn_livros_lidos = tk.Button(self, text='Livros lidos', command=lambda: controller.show_frame(PaginaLidos))
        btn_livros_lidos.pack()

        btn_minha_bbt = tk.Button(self, text='Minha BBT', command=lambda: controller.show_frame(PaginaBbt))
        btn_minha_bbt.pack()

class PaginaListaLer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Lista de livros a serem lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_exibir = tk.Button(self, text='Exibir lista de leitura', command=exibir_lista_ler)
        btn_exibir.pack()

        btn_cadastrar = tk.Button(self, text='Cadastrar livro', command=janela_cadastro_livros_ler)
        btn_cadastrar.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()

class PaginaLidos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Livros lidos', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_cadastrar = tk.Button(self, text='Cadastrar', command=adicionar_livros_lidos)
        btn_cadastrar.pack()

        btn_exibir = tk.Button(self, text='Exibir', command=exibir_lista_lidos)
        btn_exibir.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()


class PaginaBbt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Minha BBT', font=FONTE)
        label.pack(pady=10, padx=10)

        btn_cadastrar = tk.Button(self, text='Cadastrar livro', command=lambda: controller.show_frame(''))
        btn_cadastrar.pack()

        btn_exibir = tk.Button(self, text='Exibir estante de livros', command=lambda: controller.show_frame(''))
        btn_exibir.pack()

        btn_voltar = tk.Button(self, text='Voltar', command=lambda: controller.show_frame(PaginaPrincipal))
        btn_voltar.pack()

app = BbtRafa()
app.mainloop()