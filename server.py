import socket
import _thread
import re
import sys
import time
import pickle

HOST = socket.gethostbyname(socket.gethostname()) # Endereco IP do Servidor
PORT = 5000                                       # Porta que o Servidor está rodando

film_info = {'Indiana Jones': [{'host': '', 'port': '5001', 'path': 'caminho.mp4'}],
             'Blade Runner': [{'host': '', 'port' : '5002', 'path': 'caminho.mp4'}]}
keys = ['host', 'port', 'path']
# init: byte de inicio do arquivo(Se é que isso da certo), end: byte de fim

def load_file():
    try:
        with open('film_db.pkl', 'rb') as f:
            global film_info
            film_info = pickle.load(f)
    except:
        print("Problema ao abrir o arquivo de filmes: ", sys.exc_info())

def save(info, cliente):
    film_name = info[0]

    try:
        if str(film_name) in film_info:
            info.remove(info[0])
            dict_info = dict(zip(keys, info))
            film_info[str(film_name)].append(dict_info)
        else:
            info.remove(info[0])
            dict_info = dict(zip(keys, info))
            film_info[film_name] = dict_info
        with open('film_db.pkl', 'wb+') as f:
            pickle.dump(film_info, f, pickle.HIGHEST_PROTOCOL)
    except:
        print(sys.exc_info())

def browse_movies(con,cliente):
    load_file()
    try:
        while True:
            data = ''
            for i, film in enumerate(film_info.keys()):
                data = data + "\n " + str(film) +": Envie "+str(i)
            con.sendall(data.encode('utf-8'))
            response = int(con.recv(1024).decode('utf-8'))
            print(response)
            if response < len(film_info) and response >= 0:
                con.sendall(("Para se conectar com o cliente envie 'CLI'").encode('utf-8'))
                if con.recv(1024).decode('utf-8') == 'CLI':
                    con.sendall(str(film_info.values()[response]).encode('utf-8'))
                break
            else:
                con.sendall(("Opção inválida").encode('utf-8'))
                continue
    except:
        print("Erro ao buscar filmes:", sys.exc_info())

def send_movie(con, cliente):
    con.sendall(("Envie a informação do filme seguindo o padrão: \n nome do filme | host | porta | caminho").encode('utf-8'))
    response = con.recv(1024).decode('utf-8')
    print(response)
    response = response.split("|")
    print(response)
    save(response, cliente)


def conectado(con, cliente):
    print ('Conectado por', cliente)

    while True:
        try:
            directive = "Envie 1 para consultar os filmes do menu ou 2 para enviar um filme para o menu"
            con.sendall(directive.encode('utf-8'))
            response = con.recv(1024).decode('utf-8')
            print(response)
            if response == "1":
                browse_movies(con,cliente)
                break
            elif response =="2":
                send_movie(con,cliente)
                break
            else:
                con.sendall(("Opção invalida").encode('utf-8'))
                continue
        except:
            print("Erro com o servidor:", sys.exc_info()[0])
    print ('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

def main():
    #Server baseado em:  https://wiki.python.org.br/SocketBasico
    print('Servidor inicializado.')
    print('Aguardando conexão de clientes...')
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    load_file()
    while True:
            con, cliente = tcp.accept()
            _thread.start_new_thread(conectado, tuple([con, cliente]))
    tcp.close()

main()
