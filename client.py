import socket
import sys
import _thread
import ast

HOST = socket.gethostbyname(socket.gethostname()) # Endereco IP do Cliente
PORT = 5000                                       # Porta que o Cliente está rodando


def send_file(con,cliente):
	#Parte da funcao retirada de: https://gist.github.com/giefko/2fa22e01ff98e72a5be2
	print('Conectado com: ', cliente, con)
	filename = con.recv(1024).decode('utf-8')
	print(filename)
	try:
		f = open(filename,'rb')
		fr = f.read(1024)
		while (fr):
			con.send(fr)
			print('Sent ',repr(fr))
			fr = f.read(1024)
		f.close()
		print('Envio feito!')
	except:
		print("Erro ao enviar arquivo: ", sys.exc_info()[0])
	con.close()


def open_connection(host, port):
	myHOST = host
	myPORT = int(port)
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (myHOST, myPORT)
	try:
		tcp.bind(orig)
		tcp.listen(1)

		while True:
			con, cliente = tcp.accept()
			print('aceito')
			_thread.start_new_thread(send_file, tuple([con, cliente]))

		tcp.close()
	except:
		print("Erro ao abrir conexao: ", sys.exc_info()[0])
# ---------------------------------------------

def receive_file(tcp):
	#Parte da funcao retirada de: https://gist.github.com/giefko/2fa22e01ff98e72a5be2
	try:
		with open('received_file', 'wb') as f:
			print('Arquivo aberto')
			while True:
				print('Downloading...')
				data = tcp.recv(1024)
				print('data=%s', (data))
				if not data:
				    break
				# write data to a file
				f.write(data)

		f.close()
		print('Arquivo baixado com sucesso.')
	except:
		print("Erro ao receber arquivo: ", sys.exc_info()[0])
	tcp.close()
	print('Conexão encerrada.')


def connect_peer(infos):
	print(infos)
	infos_dict = ast.literal_eval(infos[1:-1])
	print(infos_dict.values())

	cHOST = infos_dict['host']
	cPORT = int(infos_dict['port'])
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (cHOST, cPORT)
	try:
		tcp.connect(dest)
		tcp.send((infos_dict['path']).encode('utf-8'))
		receive_file(tcp)
	except:
		print("Erro ao conectar com cliente: ", sys.exc_info())

def main():
	print("Deseja abrir a conexão com outros clientes? (sim)")
	res = input()
	if res == 'sim':
		print("Informe a porta: ")
		port = input()
		# print("Informe o host: ")
		host = ''
		_thread.start_new_thread(open_connection, tuple([host, port]))

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
