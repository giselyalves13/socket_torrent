import socket
import sys
import _thread
import ast

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000          # Porta que o Servidor esta


# class Peer:  Colocar send file e open connection numa classe Peer diferente de client.

def send_file(con,cliente):
	#Parte da funcao retirada de: https://gist.github.com/giefko/2fa22e01ff98e72a5be2
	print('Conectado com: ', cliente, con)
	filename = con.recv(1024).decode('utf-8')
	print(filename)
	f = open(filename,'rb')
	fr = f.read(1024)
	while (fr):
		con.send(fr)
		print('Sent ',repr(fr))
		fr = f.read(1024)
	f.close()

	print('Done sending')
	con.send(('Thank you for connecting').encode('utf-8'))
	con.close()


def open_connection(port):
	myHOST = '127.0.0.1'
	myPORT = int(port)
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (myHOST, myPORT)
	tcp.bind(orig)
	tcp.listen(1)

	while True:
		con, cliente = tcp.accept()
		print('aceito')
		_thread.start_new_thread(send_file, tuple([con, cliente]))

	tcp.close()
# ---------------------------------------------

def receive_file(tcp):
	#Parte da funcao retirada de: https://gist.github.com/giefko/2fa22e01ff98e72a5be2
	with open('received_file', 'wb') as f:
		print('file opened')
		while True:
			print('receiving data...')
			data = tcp.recv(1024)
			print('data=%s', (data))
			if not data:
			    break
			# write data to a file
			f.write(data)

	f.close()
	print('Successfully get the file')
	tcp.close()
	print('connection closed')


def connect_peer(infos):
	print(infos)
	infos_dict = ast.literal_eval(infos[1:-1])
	print(infos_dict.values())

	for i in infos_dict:
		print(i)
	print('oi: ', infos_dict['port'])
	cHOST = ''
	cPORT = int(infos_dict['port'])
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (cHOST, cPORT)
	tcp.connect(dest)
	tcp.send((infos_dict['path']).encode('utf-8'))
	receive_file(tcp)
	print('sei la')

def main():
	print("Deseja abrir a conexão com outros clientes? (sim)")
	res = input()
	if res == 'sim':
		print("Informe a porta: ")
		port = input()
		_thread.start_new_thread(open_connection, tuple([port]))

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)
	print ('Para sair use CTRL+X\n')
	while True :
		recv = tcp.recv(1024).decode('utf-8')
		print(recv)
		msg = input()
		if msg == "CLI":
			tcp.send(msg.encode('utf-8'))
			recv = tcp.recv(1024).decode('utf-8')
			connect_peer(recv)
			break
		elif msg == '\x18':
			break
		tcp.send(msg.encode('utf-8'))
	tcp.close()


main()
