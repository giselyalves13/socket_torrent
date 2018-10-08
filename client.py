import socket
import sys
import _thread

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000          # Porta que o Servidor esta

def conectado(con,cliente):
	con.sendall(("Envie o nome do filme: " ).encode('utf-8'))

def open_connection(port):
	myHOST = '127.0.0.1'
	myPORT = int(port)
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (myHOST, myPORT)
	tcp.bind(orig)
	tcp.listen(1)

	while True:
		con, cliente = tcp.accept()
		_thread.start_new_thread(conectado, tuple([con, cliente]))

	tcp.close()


def connect_client(infos):
	print(infos)

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
		# try:
		recv = tcp.recv(1024).decode('utf-8')
		print(recv)
		msg = input()
		if msg == "CLI":
			connect_client(recv)
			break
		elif msg == '\x18':
			break
		tcp.sendto(msg.encode('utf-8'), (dest))
		# except:
			# print("Unexpected error:", sys.exc_info()[0])

	tcp.close()
main()
