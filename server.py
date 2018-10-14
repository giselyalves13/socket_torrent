import socket
import _thread
import re
import sys
import time
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-west-1')
table = dynamodb.Table('filmes')

HOST = socket.gethostbyname(socket.gethostname()) # Endereco IP do Servidor
PORT = 5000                                       # Porta que o Servidor está rodando

film_list = ['Indiana Jones','Blade Runner']
film_info = {'Indiana Jones': [{'init': '20', 'end': '60','host': '', 'port': '5001', 'path': 'caminho.mp4'}],
             'Blade Runner': [{'init': '20', 'end': '60', 'host': '', 'port' : '5002', 'path': 'caminho.mp4'}]}
keys = ['init', 'end', 'host', 'port', 'path']
# init: byte de inicio do arquivo(Se é que isso da certo), end: byte de fim

def save(info, cliente):
    film_name = info[0]

    if str(film_name) in film_info:
        info.remove(info[0])
        dict_info = dict(zip(keys, info))
        film_info[str(film_name)].append(dict_info)

def get_movies():
    response = client.scan(TableName='filmes')
    return response

def insert_movie(movie):
    table.put_item(
        Item={
            'titulo' : movie['titulo'],
            'clients': [
                {'init': movie['init'], 'end': movie['end'],'host': movie['host'], 'port': movie['port'], 'path': movie['path']}
            ]
        }
    )

def browse_movies(con,cliente):
    while True:
        # try:
        for i, film in enumerate(film_list):
            con.sendall((str(film)+": Envie "+str(i)+"\n").encode('utf-8'))
        response = con.recv(1024).decode('utf-8')
        print(response)
        if film_list[int(response)]:
            film_name = film_list[int(response)]
            con.sendall(("Para se conectar com o cliente envie 'CLI'").encode('utf-8'))
            if con.recv(1024).decode('utf-8') == 'CLI':
                con.sendall(str(film_info[film_name]).encode('utf-8'))
            break
        else:
            con.sendall(("Opção inválida").encode('utf-8'))
            continue
    # except:
    # print("Unexpected error:", sys.exc_info()[0])

def send_movie(con, cliente):
    con.sendall(("Envie a informação do filme seguindo o padrão: \n nome do filme | %/ inicio | %/ fim | host | porta").encode('utf-8'))
    response = con.recv(1024).decode('utf-8')
    print(response)
    response = response.split("|")
    print(response)
    save(response, cliente)


def conectado(con, cliente):
    print ('Conectado por', cliente)

    while True:
    # try:
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
    # except:
        # print("Unexpected error:", sys.exc_info()[0])
    print ('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

def main():
    #Server baseado em:  https://wiki.python.org.br/SocketBasico
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    print(get_movies())

    while True:
        con, cliente = tcp.accept()
        _thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()

main()
