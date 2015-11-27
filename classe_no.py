import socket               # Importa modulo socket
from classe_socket import *

N = 6
MAX_NO = 2**N
class No:
	def __init__(self, endereco):
		
		self.derivacao = {}
		self.tabelaFinger = {}

		self.host, self.port = endereco
		self.clien = socketUDP(endereco) # Cria um socket
		
	# solicita entrada na rede DHT
	def entrarDHT(self, destino):
		
		comando = 'Hello'
		self.clien.enviar(comando, destino)
		msg, endereco = self.clien.receber(1024)
		
		if msg == 'RC':
			print "Nao posso entrar, a rede esta cheia! \n"
		else:
			msg = msg.split('|', 4)	
			self.id = int(msg[0])
			self.root = (int(msg[1]), msg[2], int(msg[3]))
			
			if msg[0] == msg[1]:
				self.sucessor = (msg[1], msg[2], msg[3]) # pode ser tirado posteriormente
				self.antecessor = (msg[1], msg[2], msg[3])
				self.escutarRede()
			else:
				no = (self.id, self.host, self.port)
				self.inserirNo(no, self.root)
				self.escutarRede()
							
	def inserirNo(self, no, no1):

		if no1[0] > no[0]:
			# pede antecessor do root
			antNo1 = self.encontrarAntecessor(no1)
			while (no1[0] > no[0]) and (antNo1[0] < no1[0]):
				no1 = antNo1
				antNo1 = self.encontrarAntecessor(no1)

			if no1[0] > no[0]:
				self.sucessor = no1
				self.antecessor = antNo1
				self.atualizarAnt(no1, no)
				self.atualizarSuc(antNo1, no)
			else:
				self.sucessor = self.encontrarSucessor(no1)
				self.antecessor = no1
				self.atualizarAnt(self.sucessor, no)
				self.atualizarSuc(no1, no)
		else:
			sucNo1 = self.encontrarSucessor(no1)
			while (no1[0] < no[0]) and (sucNo1[0] > no1[0]):	
				no1 = sucNo1
				sucNo1 = self.encontrarSucessor(no1)
			if no1[0] < no[0]:
				self.sucessor = sucNo1
				self.antecessor = no1
				self.atualizarAnt(sucNo1, no)
				self.atualizarSuc(no1, no)
			else:
				self.sucessor = no1
				self.antecessor = self.encontrarAntecessor(no1)
				self.atualizarAnt(no1, no)
				self.atualizarSuc(self.antecessor, no)
		print "No: " + str(no) + " Ant " + str(self.antecessor) + " Suc " + str(self.sucessor)
	
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
			
	# Enconta o sucessor de um no 
	def encontrarSucessor(self, no):
		noId, noHost, noPort = no
		self.clien.enviar('suc', (noHost, noPort))
		noSuc, endereco = self.clien.receber(1024)
		noSuc = noSuc.split('|', 3)
		noSuc = (int(noSuc[0]), noSuc[1], int(noSuc[2]))
		
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
				env =  str(	self.sucessor[0]) +'|'+ str(self.sucessor[1]) +'|'+ str(self.sucessor[2])
				print "Enviando sucessor: " + env + " para " + str(endereco)
				self.clien.enviar(env, endereco)
			if comando[0] == 'ant':
				env =  str(self.antecessor[0]) +'|'+ str(self.antecessor[1]) +'|'+ str(self.antecessor[2])
				print "Enviando antecessor: " + env + " para " + str(endereco)
				self.clien.enviar(env, endereco)
			if comando[0] == 'atuSuc':
				self.sucessor = (comando[1], comando[2], comando[3])
				print "Atualizado sucessor de: " + str(self.id) + " para " + str(self.sucessor)
				# atualizar finger table
			
			if comando[0] == 'atuAnt':
				self.antecessor = (comando[1], comando[2], comando[3])
				print "Atualizado antecessor de: " + str(self.id) + " para " + str(self.antecessor)
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
