#!/usr/bin/env python
# encoding: utf-8
"""
classe_no_finger.py

Created by Paulo Passos on 2015-11-27.
Copyright (c) 2015 __UnB__. All rights reserved.
"""
import time
import socket
from Queue import Queue
from threading import Thread, Condition               # Importa modulo socket

N = 6
queue = []
MAX_PING = 6
MAX_NO = 2**N
suces = Queue(2)
condition = Condition()
condPerco = Condition()
class No:
	def __init__(self, endereco, sock):	
		self.root = ()
		self.atalho = {} # conterao o (ID, IP, Porta) do no que quada a chave correspondente
		self.chaves = {} # conetem as chaves do No corrente
		self.sucessor = ()
		self.sucessorIm = ()
		self.antecessor = ()

		self.host, self.port = endereco
		self.clien = sock # Retirar se for o caso
		
def escutarRede(no, sock):
	print "Escutando Rede... "
	global queue
	global suces
	while True:
		#OBS: Os formatos de msg a serem enviadas e recebidos serao do tipo:  comando|noId|noHost|noPorta
		comando, endereco = sock.recvfrom(1024)
		comando = comando.split('|')
		#print str(comando) + " aki" #OBS RETIRAR
		
		if comando[0] == 'novo': # Novo No
			no.id = int(comando[4])
			no.root = (int(comando[1]), comando[2], int(comando[3]))
			inserirNo(no, no.root, sock)
	
		if comando[0] == 'root':
			msg = comando
			inserirRoot(no, msg)
		
		if comando[0] == 'suc':	
			env =  str(	no.sucessor[0]) +'|'+ str(no.sucessor[1]) +'|'+ str(no.sucessor[2])
			print "Enviando sucessor: " + env + " para " + str(endereco)
			sock.sendto(env, endereco)
			
		if comando[0] == 'sucP':
			env =  'sucR' +'|'+  str(no.sucessor[0]) +'|'+ str(no.sucessor[1]) +'|'+ str(no.sucessor[2])
			sock.sendto(env, endereco)
			
		if comando[0] == 'sucR':
			suces.put((int(comando[1]), comando[2], int(comando[3])))
			
		if comando[0] == 'ant':
			env =  str(no.antecessor[0]) +'|'+ str(no.antecessor[1]) +'|'+ str(no.antecessor[2])
			print "Enviando antecessor: " + env + " para " + str(endereco)
			sock.sendto(env, endereco)
		
		if comando[0] == 'atuSuc':
			no.sucessor = (int(comando[1]), comando[2], int(comando[3]))
			print "Atualizado sucessor de: " + str(no.id) + " para " + str(no.sucessor)
			# atualizar finger table

		if comando[0] =='atuSucIm':
			no.sucessorIm = (int(comando[1]), comando[2], int(comando[3]))
			print "Atualizado sucessorIm de: " + str(no.id) + " para " + str(no.sucessorIm)

		if comando[0] == 'atuAnt':
			no.antecessor = (int(comando[1]), comando[2], int(comando[3]))
			print "Atualizado antecessor de: " + str(no.id) + " para " + str(no.antecessor)
		
		if comando[0] == 'cheio':
			print 'A rede ja esta cheia!!! Nao eh possivel inserir mais nos no DHT'
		
		if comando[0] == 'ping':
			#print 'pong'
			sock.sendto('pong', endereco)
			
		if comando[0] == 'pong':
			condition.acquire()
			queue.pop(0)
			condition.release()
			
def inserirRoot(no, msg):
	no.id = int(msg[1])
	no.root = (int(msg[1]), msg[2], int(msg[3]))
	
	no.sucessor = (int(msg[1]), msg[2], int(msg[3])) # pode ser tirado posteriormente
	no.antecessor = (int(msg[1]), msg[2], int(msg[3]))
	no.sucessorIm = (int(msg[1]), msg[2], int(msg[3])) # Sucessor do Sucessor
		
	"""
	#finguer table
	for i in range(N):
		no.derivacao[i] = (no.id + (2**i)) % (2**N)
		no.finguer[i] = no.id		
	"""	
"""
def inserirNo(no, no1, sock):
	noEnt = (no.id, no.host, no.port)
	if no1[0] > noEnt[0]:
		# pede antecessor do root
		antNo1 = encontrarAntecessor(no1, sock)
		while (no1[0] > noEnt[0]) and (antNo1[0] < no1[0]):
			no1 = antNo1
			antNo1 = encontrarAntecessor(no1, sock)

		if no1[0] > noEnt[0]:
			print no1
			no.sucessor = no1
			no.sucessorIm = encontrarSucessor(no1, sock)
			no.antecessor = antNo1
			atualizarAnt(no1, noEnt, sock)
			suc = encontrarSucessor(no.sucessorIm, sock)
			atualizarSucIm(no1, suc, sock)
			atualizarSuc(antNo1, noEnt, sock)
			atualizarSucIm(antNo1, no1, sock)
		else:
			no.sucessor = encontrarSucessor(no1, sock)
			no.sucessorIm = encontrarSucessor(no.sucessor, sock)
			no.antecessor = no1
			atualizarSuc(no1, noEnt, sock)
			atualizarAnt(no.sucessor, noEnt, sock)
			atualizarSucIm(no1, no.sucessor, sock)
	else:
		sucNo1 = encontrarSucessor(no1, sock)
		while (no1[0] < noEnt[0]) and (sucNo1[0] > no1[0]):	
			no1 = sucNo1
			sucNo1 = encontrarSucessor(no1, sock)
		if no1[0] < noEnt[0]:
			print sucNo1
			no.sucessor = sucNo1
			no.sucessorIm = encontrarSucessor(sucNo1, sock)
			no.antecessor = no1
			atualizarSuc(no1, noEnt, sock)
			atualizarSucIm(no1, sucNo1, sock)
			atualizarAnt(sucNo1, noEnt, sock)
			sucIm = encontrarSucessor(no.sucessorIm, sock)
			atualizarSucIm(sucNo1, sucIm, sock)
			suc = encontrarSucessor(sucIm, sock)
			atualizarSucIm(no.sucessorIm, suc, sock)

		else:
			no.sucessor = no1
			no.sucessorIm = sucNo1
			no.antecessor = encontrarAntecessor(no1, sock)
			atualizarAnt(no1, noEnt, sock)
			sucIm = encontrarSucessor(sucNo1, sock)
			atualizarSucIm(no1, sucIm, sock)
			atualizarSuc(no.antecessor, noEnt, sock)
			atualizarSucIm(no.antecessor, no1, sock)
			antAnt = encontrarAntecessor(no.antecessor, sock)
			atualizarSucIm(antAnt, noEnt, sock)
	print "No: " + str(noEnt) + " Ant " + str(no.antecessor) + " Suc " + str(no.sucessor)
"""	
def inserirNo(no, no1, sock):
	noEnt = (no.id, no.host, no.port)
	root = no1
	if no1[0] > noEnt[0]:
		# pede antecessor do root
		antNo1 = encontrarAntecessor(no1, sock)
		while (no1[0] > noEnt[0]) and (antNo1[0] < no1[0]):
			no1 = antNo1
			antNo1 = encontrarAntecessor(no1, sock)

		if no1[0] > noEnt[0]:
			print no1
			no.sucessor = no1
			no.antecessor = antNo1
			atualizarAnt(no1, noEnt, sock)
			atualizarSuc(antNo1, noEnt, sock)
		else:
			no.sucessor = encontrarSucessor(no1, sock)
			no.antecessor = no1
			atualizarSuc(no1, noEnt, sock)
			atualizarAnt(no.sucessor, noEnt, sock)
	else:
		sucNo1 = encontrarSucessor(no1, sock)
		while (no1[0] < noEnt[0]) and (sucNo1[0] > no1[0]):	
			no1 = sucNo1
			sucNo1 = encontrarSucessor(no1, sock)
		if no1[0] < noEnt[0]:
			print sucNo1
			no.sucessor = sucNo1
			no.antecessor = no1
			atualizarSuc(no1, noEnt, sock)
			atualizarAnt(sucNo1, noEnt, sock)

		else:
			no.sucessor = no1
			no.antecessor = encontrarAntecessor(no1, sock)
			atualizarAnt(no1, noEnt, sock)
			atualizarSuc(no.antecessor, noEnt, sock)
			
	atualizarSucIm(no.antecessor, no.sucessor, sock)
	no1 = (no.id, no.host, no.port)
	if no.antecessor != no.sucessor:
		print "10"
		no.sucessorIm = encontrarSucessor(no.sucessor, sock)
		print "12"
		atualizarIm(no1, no.sucessor, sock)
		print "13"
	else:
		print "11"
		no.sucessorIm = no1
	print "No: " + str(noEnt) + " Ant " + str(no.antecessor) + " Suc " + str(no.sucessor) + " SucIm " + str(no.sucessorIm)
		
def atualizarSuc(no, suc, sock):
	noId, noHost, noPort = no
	sucId, sucHost, sucPort = suc
	env = 'atuSuc' + '|' + str(sucId) + '|' + sucHost + '|' + str(sucPort)
	sock.sendto(env, (noHost, noPort))

def atualizarSucIm(no, sucIm, sock):
	noId, noHost, noPort = no
	sucId, sucHost, sucPort = sucIm
	env = 'atuSucIm' + '|' + str(sucId) + '|' + sucHost + '|' + str(sucPort)
	sock.sendto(env, (noHost, noPort))

def atualizarAnt(no, ant, sock):
	noId, noHost, noPort = no
	antId, antHost, antPort = ant
	env = 'atuAnt' + '|' + str(antId) + '|' + antHost + '|' + str(antPort)
	sock.sendto(env, (noHost, noPort))
############################################################
# Enconta o sucessor de um no 
def encontrarSucessor(no, sock):
	noId, noHost, noPort = no
	sock.sendto('suc', (noHost, noPort))
	noSuc, endereco = sock.recvfrom(1024)
	noSuc = noSuc.split('|', 3)
	noSuc = (int(noSuc[0]), noSuc[1], int(noSuc[2]))

	return noSuc
	

def encontrarAntecessor(no, sock):
	noId, noHost, noPort = no
	sock.sendto('ant', (noHost, noPort))
	noAnt, endereco = sock.recvfrom(1024)
	noAnt = noAnt.split('|', 3)
	noAnt = (int(noAnt[0]), noAnt[1], int(noAnt[2]))

	return noAnt
##############################################################
def sucessor(no, sock):
	global suces
	noId, noHost, noPort = no

	sock.sendto('sucP', (noHost, noPort))
	noSuc = suces.get()

	return noSuc


def atualizarIm(no1, sucNo1, sock):
	ns = (no1[0], no1[1], no1[2])
	
	sucIm = encontrarSucessor(sucNo1, sock)
	print "1"
	while sucIm[0] != no1[0]:
		print "2"
		suc = sucIm
		sucIm = encontrarSucessor(suc, sock)
		atualizarSucIm(sucNo1, sucIm, sock)
		sucNo1 = suc
		print "3"			

	return None

	
def ping(no, sock):
	global queue
	while True:
		if no.id != no.sucessor[0]:
			condition.acquire()
			if len(queue) == MAX_PING:
				print "No " + str(no.sucessor) + " nao responde!" # mudar sucessor
				print "Atualizando sucessor..."
				print "Novo sucessor " + str(no.sucessor)
				print "SucessorIm " + str(no.sucessorIm)
				
				no.sucessor = no.sucessorIm
				no.sucessorIm = sucessor(no.sucessor, sock) # problema se o sucessor de sucessorIm for o proprio no da problema
				
				print "Novo sucessor " + str(no.sucessor)
				print "SucessorIm " + str(no.sucessorIm)
			message = 'ping'
			queue.append(message)
			serverName = no.sucessor[1]
			serverPort = no.sucessor[2]
			sock.sendto(message,(serverName,serverPort))

			print "Emitiu ping"
			condition.release()
			time.sleep(1)

				
def entrarDHT(destino, no, sock):
	comando = 'Hello'
	sock.sendto(comando, destino)

def percorrerDHT(no, sock):
	root = no.root
	ns = (root[0], root[1], root[2])
	if root == None:
		print "DHT vazio"
		return None
	else:
		print "###########################################"
		print "#               NOS DA DHT               #"
		print "###########################################"
		print "No " + str(ns[0]) + ": porta " + str(ns[2])
		ns = sucessor(ns, sock)

		while ns[0] != root[0]:
			print "No " + str(ns[0]) + ": porta " + str(ns[2])
			ns = sucessor(ns, sock)

			"""
			if(root.nomeArq == arq):
				return str("No: " + str(no[0]))
			"""
		print "-------------------------------------------"
		print ""	
		return None
	
def menu(no, sock):
	while True:
		print "O que deseja fazer?"
		print "1 - Entrar na rede"
		print "2 - Iniciar ping"
		print "3 - Percorrer rede"
		print "4 - Ver sucessor 1 e 2"	
		comando = raw_input("Digite um inteiro: ")
		if comando == '1':
			rendezvous = (socket.gethostbyname(socket.gethostname()), 12345)
			t2 = Thread(target=entrarDHT, args=(rendezvous, no, sock))
			t2.start()
			t2.join()
		# ver caso do ping qndo so tem um no na rede	
		if comando == '2':
			ping(no, sock)
		if comando == '3':
			percorrerDHT(no, sock)
		if comando == '4':
			print "Antecessor de " + str(no.id) + " eh " + str(no.antecessor)
			print "Sucessor de " + str(no.id) + " eh " + str(no.sucessor)
			print "SucessorIm de " + str(no.id) + " eh " + str(no.sucessorIm)
			


def	main():
	host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
	porta = raw_input("Escreva um numero inteiro para a porta: ") # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala
	porta = int(porta)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP 	
	sock.bind((host, porta)) # Espera conecoes no endereco e porta fornecidos
	
	ender = (host, porta) 
	n1 = No(ender, sock)

	t = Thread(target=escutarRede, args=(n1,sock))
	t.start()
	menu(n1, sock)
	
	while True:
		pass

	
if __name__ == "__main__":
	main()


