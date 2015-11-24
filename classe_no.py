import socket               # Importa modulo socket
from classe_socket import *

m = 6
class No:
	def __init__(self, endereco):
		self.id = None
		self.derivacao = {}
		self.tabelaFinger = {}
		
		self.host, self.port = endereco
		self.clien = socketUDP(endereco) # Cria um socket
		
	# solicita entrada na rede DHT
	def entrarDHT(self, destino):
		env = 'Hello'
		self.clien.enviar(env, destino)
		msg, endereco = self.clien.receber(1024)
		
		print msg
		
		if msg == 'RC':
			print "Nao posso entra, rede cheia! \n"
		
		else:
			msg = msg.split('|', 4)	
			self.id = int(msg[0]) 
			#self.root[msg[1]] = [msg[2], msg[3]]

			if msg[0] == msg[1]:
				# preecncher table finger
				self.root = self
				for i in range(m):
					self.derivacao[i] = (self.id + (2**i)) % (2**m)
					self.tabelaFinger[i] = self 
				self.antecessor = self
			else:
				print "teste"
				# buscar local no DHT circular
				# inserir novo no
				# atualizar finger table
	
	# Encontra sucessor de um no
	def sucessor(self, no):
		return no.self.tabelaFinger[0]
		
	# Encontra posicao de um no no DHT
	def encontrarPos(self, no):
	
		# envia mensagem ao root perguntando quem eh seu sucessor
		dest = (self.root.host, self.root.port)
		self.clien.enviar('suc', dest)
		msg, endereco= self.clien.receber(1024)	
		# verifica se o id do sucessor do root eh maior que seu id
		
		#CONTINUAR IMPLEMENTACAO AKI
		
		# se for, insere entre o root e o sucessor do root
		# se n for envia mensagem ao sucessor do root repetindo o processo
		return "teste"
		
	def escutarRede(self):
		while True:
			msg = self.clien.receber(1024)
			print msg
			if msg == 'suc':	
				env =  str(self.tabelaFinger[0].id) +'|'+ str(self.tabelaFinger[0].host) +'|'+ str(self.tabelaFinger[0].port)
				self.clien.enviar(env, dest)
			#CONTINUAR IMPLEMENTACAO AKI
	
def	main():
	
	host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
	port = 12346 # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala
	ender = (host, port)

	n1 = No(ender)
	rendezvous = (socket.gethostbyname(socket.gethostname()), 12345)
	n1.entrarDHT(rendezvous)
	#n1.iniciarTabAtalhos(n1)
	#n1.imprimirTabAtalhos(n1)
	
if __name__ == "__main__":
	main()
