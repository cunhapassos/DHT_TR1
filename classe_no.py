#!/usr/bin/env python
# encoding: utf-8
"""
classe_no_finger.py

Created by Paulo Passos on 2015-11-27.
Copyright (c) 2015 __UnB__. All rights reserved.
"""
import time
import socket
import threading               # Importa modulo socket
from classe_socket import *

N = 6
MAX_NO = 2**N
class No:
<<<<<<< Updated upstream
	def __init__(self, endereco, sock, arquivo):
=======
	def __init__(self, endereco, sock):	
		self.sucessor = ()
>>>>>>> Stashed changes
		self.sucessorIm = ()
		self.antecessor = ()
		#self.derivacao = {}
		self.atalho = {}
		self.root = ()

		self.host, self.port = endereco
		self.clien = sock
		self.nomeArq = arquivo
		
	# solicita entrada na rede DHT
def entrarDHT(destino, no, sock):
	comando = 'Hello'
	sock.enviar(comando, destino)
	msg, endereco = sock.receber(1024)
	
	if msg == 'RC':
		print "Nao posso entrar, a rede esta cheia! \n"
	else:
		msg = msg.split('|', 4)	
		no.id = int(msg[0])
		no.root = (int(msg[1]), msg[2], int(msg[3]))
		
		if msg[0] == msg[1]:
			no.sucessor = (int(msg[1]), msg[2], int(msg[3])) # pode ser tirado posteriormente
			no.antecessor = (int(msg[1]), msg[2], int(msg[3]))
			no.sucessorIm = (int(msg[1]), msg[2], int(msg[3])) # Sucessor do Sucessor
			#escutarRede(self, sock)
			
			#finguer table
			for i in range(N):
				no.derivacao[i] = (no.id + (2**i)) % (2**N)
				no.atalho[i] = no.id
		else:
			no = (no.id, no.host, no.port)
			no.inserirNo(no, no.root, sock)
			#escutarRede(self, sock)
							
def inserirNo(no, no1, sock):
	if no1[0] > no[0]:
		# pede antecessor do root
		antNo1 = encontrarAntecessor(no1, sock)
		while (no1[0] > no[0]) and (antNo1[0] < no1[0]):
			no1 = antNo1
			antNo1 = encontrarAntecessor(no1, sock)

		if no1[0] > no[0]:
			no.sucessor = no1
			no.sucessorIm = encontrarSucessor(no1, sock)
			no.antecessor = antNo1
			atualizarAnt(no1, no, sock)
			atualizarSuc(antNo1, no, sock)
			atualizarSucIm(antNo1, no1, sock)
		else:
			no.sucessor = encontrarSucessor(no1, sock)
			no.sucessorIm = encontrarSucessor(no.sucessor, sock)
			no.antecessor = no1
			atualizarSuc(no1, no, sock)
			atualizarAnt(no.sucessor, no, sock)
			atualizarSucIm(no1, no.sucessor, sock)
	else:
		sucNo1 = encontrarSucessor(no1, sock)
		while (no1[0] < no[0]) and (sucNo1[0] > no1[0]):	
			no1 = sucNo1
			sucNo1 = encontrarSucessor(no1, sock)
		if no1[0] < no[0]:
			no.sucessor = sucNo1
			no.sucessorIm = encontrarSucessor(sucNo1, sock)
			no.antecessor = no1
			atualizarSuc(no1, no, sock)
			atualizarAnt(sucNo1, no, sock)
			atualizarSucIm(no1, sucNo1, sock)
		else:
			no.sucessor = no1
			no.sucessorIm = sucNo1
			no.antecessor = encontrarAntecessor(no1, sock)
			atualizarAnt(no1, no, sock)
			atualizarSuc(no.antecessor, no, sock)
			atualizarSucIm(no.antecessor, no1, sock)
	print "No: " + str(no) + " Ant " + str(no.antecessor) + " Suc " + str(no.sucessor)
	
	
def escutarRede(no, sock):
	print "Escutando Rede: "
	while True:
		comando, endereco = sock.sock.recvfrom(1024)
		comando = comando.split('|')
		print str(comando) + " aki"
		if comando[0] == 'suc':	
			env =  str(	no.sucessor[0]) +'|'+ str(no.sucessor[1]) +'|'+ str(no.sucessor[2])
			print "Enviando sucessor: " + env + " para " + str(endereco)
			sock.enviar(env, endereco)
		if comando[0] == 'ant':
			env =  str(no.antecessor[0]) +'|'+ str(no.antecessor[1]) +'|'+ str(no.antecessor[2])
			print "Enviando antecessor: " + env + " para " + str(endereco)
			sock.enviar(env, endereco)
		if comando[0] == 'atuSuc':
			no.sucessor = (comando[1], comando[2], comando[3])
			print "Atualizado sucessor de: " + str(no.id) + " para " + str(no.sucessor)
			# atualizar finger table
		
		if comando[0] =='atuSucIm':
			no.sucessorIm = (comando[1], comando[2], comando[3])
			print "Atualizado sucessorIm de: " + str(no.id) + " para " + str(no.sucessorIm)
		
		if comando[0] == 'atuAnt':
			no.antecessor = (comando[1], comando[2], comando[3])
			print "Atualizado antecessor de: " + str(no.id) + " para " + str(no.antecessor)
		
		if comando[0] == 'ping':
			print 'pong'
			sock.enviar('pong', endereco)

			# atualizar finger table	
			#CONTINUAR IMPLEMENTACAO AKI
			
def atualizarSuc(no, suc, sock):
	noId, noHost, noPort = no
	sucId, sucHost, sucPort = suc
	env = 'atuSuc' + '|' + str(sucId) + '|' + sucHost + '|' + str(sucPort)
	sock.enviar(env, (noHost, noPort))

def atualizarSucIm(no, sucIm, sock):
	noId, noHost, noPort = no
	sucId, sucHost, sucPort = sucIm
	env = 'atuSucIm' + '|' + str(sucId) + '|' + sucHost + '|' + str(sucPort)
	sock.enviar(env, (noHost, noPort))

def atualizarAnt(no, ant, sock):
	noId, noHost, noPort = no
	antId, antHost, antPort = ant
	env = 'atuAnt' + '|' + str(antId) + '|' + antHost + '|' + str(antPort)
	sock.enviar(env, (noHost, noPort))

# Enconta o sucessor de um no 
def encontrarSucessor(no, sock):
	noId, noHost, noPort = no
	sock.enviar('suc', (noHost, noPort))
	noSuc, endereco = sock.receber(1024)
	noSuc = noSuc.split('|', 3)
	noSuc = (int(noSuc[0]), noSuc[1], int(noSuc[2]))

	return noSuc

def encontrarAntecessor(no, sock):
	noId, noHost, noPort = no
	sock.enviar('ant', (noHost, noPort))
	noAnt, endereco = sock.receber(1024)
	noAnt = noAnt.split('|', 3)
	noAnt = (int(noAnt[0]), noAnt[1], int(noAnt[2]))

	return noAnt

def ping(sock, no):
	
	noId, noHost, noPorta = no.sucessor
	if noId != no.root[0]:
		print "ping"
		sock.enviar('ping', (noHost, int(noPorta)))
		msg, end = sock.receber(1024)
		if msg != 'pong':
			print "Sucessor de " + str(no.id) + " nao responde!"
			noId, noHost, noPorta = no.sucessorIm
			
			sock.enviar('ping', (noHost, int(noPorta)))
			msg, end = sock.receber(1024)
			if msg == 'pong':
				print "Atualizando sucessor..."
				no.sucessor = no.sucessorIm
				no.sucessorIm = encontrarSucessor(no.sucessor)
				no.atualizarAnt(no.sucessor, (no.id, no.host, no.port))
			else:
				print "Nao foi posivel recuperar a rede!"

def buscarArq(no, arq):
	verif = raw_input("Deseja buscar algum arquivo? (y/n)")
	while(verif == "y"):
		arq = raw_input("Qual arquivo deseja buscar? ")
		endBusca = percorrerDHT(no, arq)
		if (endBusca == None):
			print "Não foi possivel encontrar o arquivo na rede"
		else:
			print "Arquivo encontrado no "+endBusca
		verif = raw_input("Deseja buscar algum arquivo? (y/n)")
	
def percorrerDHT(root, arq):
	if root == None:
		print "DHT vazio"
		return None
	else:
		print "Nos DHT"
		no = root
		while no != root:
			no = encontrarSucessor(no)
			if(root.nomeArq == arq):
				return str("No: " + str(no[0]))
		return None		

	
	
def	main():
	
	host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
	porta = raw_input("Escreva um numero inteiro para a porta: ") # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala
	ender = (host, int(porta))
	arquivo = raw_input("Digite o nome do arquivo que contem o nó: ")
	clien = socketUDP(ender) # Cria um socket

	n1 = No(ender, clien, arquivo)
	rendezvous = (socket.gethostbyname(socket.gethostname()), 12345)
	t = threading.Thread(target=escutarRede, args=(n1,clien))
<<<<<<< Updated upstream
	t1 = threading.Thread(target=buscarArq, args=(n1,arquivo))
=======
	#t2 = threading.Thread(target=entrarDHT, args=(rendezvous, n1, clien))
>>>>>>> Stashed changes
	#t.daemon = True
	#t2.daemon = True
	t.start()
<<<<<<< Updated upstream
	t1.start()
	clien.desconectar
=======
	#entrarDHT(rendezvous, n1, clien)
	#t2.start()
	while True:
		pass
	#clien.desconectar
>>>>>>> Stashed changes

	
if __name__ == "__main__":
	main()


