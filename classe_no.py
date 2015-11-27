import socket               # Importa modulo socket
from classe_socket import *

N = 6
MAX_NO = 2**N
class No:
	def __init__(self, endereco):
		
		self.root ={}
		self.derivacao = {}
		self.sucessor = {}
		self.antecessor = {}
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
			self.root["rootID"] = int(msg[1])
			self.root["rootHost"] = msg[2]
			self.root["rootPorta"] = int(msg[3])
			
			if msg[0] == msg[1]:
				# preecncher table finger
				for i in range(N):
					self.derivacao[i] = (self.id + (2**i)) % (MAX_NO)
					finger = {"indice": i, "deriv": self.derivacao[i], "id": int(msg[1]), "host": msg[2], "porta": int(msg[3])}
					self.tabelaFinger[i] = finger 
				
				self.sucessor = {"id": msg[1], "host": msg[2], "porta": msg[3]} # pode ser tirado posteriormente
				self.antecessor = {"id": msg[1], "host": msg[2], "porta": msg[3]} 
				self.escutarRede()
			
			else:
				
				print "Inserindo No no DHT..."
				self.inserirNoDHT()
				print "Ant " + str(self.antecessor) + " Suc " + str(self.sucessor)
				self.escutarRede()
				# buscar local no DHT circular
				# inserir novo no
				# atualizar finger table
	
	
		
	# Inserir um no no DHT
	def inserirNoDHT(self):
		print "Root: " + str(self.root)
		no = (self.id, self.host, self.port)
		no1 = (self.root["rootID"], self.root["rootHost"], self.root["rootPorta"])
		noSuc = self.encontrarSucessor(no, no1)
		noAnt = self.encontrarAntecessor(noSuc)
		
		self.sucessor["id"] = noSuc[0]
		self.sucessor["host"] = noSuc[1]
		self.sucessor["porta"] = noSuc[2]
		self.antecessor["id"] = noAnt[0]
		self.antecessor["host"] = noAnt[1]
		self.antecessor["porta"] = noAnt[2]

 		
		self.atualizarSuc(noAnt, no)
		self.atualizarAnt(noSuc, no)
		
	
	def atualizarSuc(self, no, suc):
		noId, noHost, noPort = no
		sucId, sucHost, sucPort = suc
		env = 'atuSuc' + '|' + str(sucId) + '|' + sucHost + '|' + str(sucPort)
		
		self.clien.enviar(env, (noHost, noPort))
		
	def atualizarAnt(self, no, ant):
		noId, noHost, noPort = no
		antId, antHost, antPort = ant
		env = 'atuAnt' + '|' + str(antId) + '|' + antHost + '|' + str(antPort)

		self.clien.enviar(env, (noHost, noPort))
		
	######OBS : ESSA FUNCAO AINDA ESTA COM PROBLEMA - N ESTA INSERINDO NA ORDEM CERTA	
	# Enconta o sucessor de um no DHT a partir de outro no
	def encontrarSucessor(self, no, no1):
		# nesse caso No e No1  do tipo (id, host, port)
		noId, noHost, noPort = no
		no1Id, no1Host, no1Port = no1

		# envia mensagem ao no1 perguntando quem eh seu sucessor
		self.clien.enviar('suc', (no1Host, no1Port))
		noSuc, endereco = self.clien.receber(1024)
		noSuc = noSuc.split('|', 3)
		noSuc = (int(noSuc[0]), noSuc[1], int(noSuc[2]))
		
		print "NoId "+ str(noId) + " no1Id " + str(no1Id) + " noSuc[0] " + str(noSuc[0])
		"""
		if not((noId > no1Id) ^ (noSuc[0] > no1Id)):
			print "NoId "+ str(noId) + " no1Id " + str(no1Id) + " noSuc[0] " + str(noSuc[0])
			return self.encontrarSucessor(no, (int(noSuc[0]), noSuc[1], int(noSuc[2])))
		"""
		if noSuc[0] == no1Id:
			return noSuc
		elif no1Id > noSuc[0] > noId:
			return noSuc
		elif noId > no1Id > noSuc[0]:
			return noSuc
		elif not(noSuc[0] > noId > no1Id):
			return self.encontrarSucessor(no, (int(noSuc[0]), noSuc[1], int(noSuc[2])))
		else:
			return noSuc
	
	def encontrarAntecessor(self, no):
		noId, noHost, noPort = no
		self.clien.enviar('ant', (noHost, noPort))
		noAnt, endereco = self.clien.receber(1024)
		noAnt = noAnt.split('|', 3)
		noAnt = (int(noAnt[0]), noAnt[1], int(noAnt[2]))
		
		return noAnt
	
	
	def escutarRede(self):
		while True:
			comando, endereco = self.clien.receber(1024)
			comando = comando.split('|')
			
			if comando[0] == 'suc':	
				env =  str(self.tabelaFinger[0]["id"]) +'|'+ str(self.tabelaFinger[0]["host"]) +'|'+ str(self.tabelaFinger[0]["porta"])
				print "Enviando sucessor: " + env
				self.clien.enviar(env, endereco)
			if comando[0] == 'ant':
				env =  str(self.antecessor["id"]) +'|'+ str(self.antecessor["host"]) +'|'+ str(self.antecessor["porta"])
				print "Enviando antecessor: " + env
				self.clien.enviar(env, endereco)
			if comando[0] == 'atuSuc':
				self.sucessor["id"] = comando[1]
				self.sucessor["host"] = comando[2]
				self.sucessor["porta"] = comando[3]
				# atualizar finger table
			
			if comando[0] == 'atuAnt':
				self.antecessor["id"] = comando[1]
				self.antecessor["host"] = comando[2]
				self.antecessor["porta"] = comando[3]
				# atualizar finger table	
			#CONTINUAR IMPLEMENTACAO AKI
	
def	main():
	
	host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
	porta = raw_input("Escreva um numero inteiro para a porta: ") # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala
	ender = (host, int(porta))

	n1 = No(ender)
	rendezvous = (socket.gethostbyname(socket.gethostname()), 12345)
	n1.entrarDHT(rendezvous)

	
if __name__ == "__main__":
	main()
