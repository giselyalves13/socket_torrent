import socket
import sys

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000          # Porta que o Servidor esta


def open_connection():
	pass	

def connect_client():
	pass

def main():
	print("Deseja abrir a conexão com outros clientes? (sim)")
	res = input()
	if res == 'sim':
		open_connection()

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
			connect_client()
			break
		elif msg == '\x18':
			break
		tcp.sendto(msg.encode('utf-8'), (dest))
		# except:
			# print("Unexpected error:", sys.exc_info()[0])

	tcp.close()
main()