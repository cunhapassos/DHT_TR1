#!/usr/bin/env python
# encoding: utf-8
"""
classe_no_finger.py

Created by Paulo Passos on 2015-11-27.
Copyright (c) 2015 __MyCompanyName__. All rights reserved.
"""
import time
import socket
import threading               # Importa modulo socket
from classe_socket import *

N = 6
MAX_NO = 2**N
class No:
	def __init__(self, endereco, arq):
		self.sucessorIm = ()
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
				self.sucessor = (int(msg[1]), msg[2], int(msg[3])) # pode ser tirado posteriormente
				self.antecessor = (int(msg[1]), msg[2], int(msg[3]))
				self.sucessorIm = (int(msg[1]), msg[2], int(msg[3])) # Sucessor do Sucessor
				self.escutarRede()
				
				#finguer table
				for i in range(N):
					self.derivacao[i] = (self.id + (2**i)) % (2**N)
					self.atalho[i] = self.id
			else:
				no = (self.id, self.host, self.port)
				self.inserirNo(no, self.root)
				self.escutarRede()
							
	def inserirNo(self, no, no1):
		if no1[0] > no[0]:
			# pede antecessor do root
			antNo1 = encontrarAntecessor(no1, self.clien)
			while (no1[0] > no[0]) and (antNo1[0] < no1[0]):
				no1 = antNo1
				antNo1 = encontrarAntecessor(no1, self.clien)

			if no1[0] > no[0]:
				self.sucessor = no1
				self.sucessorIm = encontrarSucessor(no1, self.clien)
				self.antecessor = antNo1
				atualizarAnt(no1, no, self.clien)
				atualizarSuc(antNo1, no, self.clien)
				atualizarSucIm(antNo1, no1, self.clien)
			else:
				self.sucessor = encontrarSucessor(no1, self.clien)
				self.sucessorIm = encontrarSucessor(self.sucessor, self.clien)
				self.antecessor = no1
				atualizarSuc(no1, no, self.clien)
				atualizarAnt(self.sucessor, no, self.clien)
				atualizarSucIm(no1, self.sucessor, self.clien)
		else:
			sucNo1 = encontrarSucessor(no1, self.clien)
			while (no1[0] < no[0]) and (sucNo1[0] > no1[0]):	
				no1 = sucNo1
				sucNo1 = encontrarSucessor(no1, self.clien)
			if no1[0] < no[0]:
				self.sucessor = sucNo1
				self.sucessorIm = encontrarSucessor(sucNo1, self.clien)
				self.antecessor = no1
				atualizarSuc(no1, no, self.clien)
				atualizarAnt(sucNo1, no, self.clien)
				atualizarSucIm(no1, sucNo1, self.clien)
			else:
				self.sucessor = no1
				self.sucessorIm = sucNo1
				self.antecessor = encontrarAntecessor(no1, self.clien)
				atualizarAnt(no1, no, self.clien)
				atualizarSuc(self.antecessor, no, self.clien)
				atualizarSucIm(self.antecessor, no1, self.clien)
		print "No: " + str(no) + " Ant " + str(self.antecessor) + " Suc " + str(self.sucessor)
	
	
	def escutarRede(self):
		t = threading.Thread(target=ping, args=(self.clien, self))
		t.start()
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
				
			if comando[0] =='atuSucIm':
				self.sucessorIm = (comando[1], comando[2], comando[3])
				print "Atualizado sucessorIm de: " + str(self.id) + " para " + str(self.sucessorIm)
				
			if comando[0] == 'atuAnt':
				self.antecessor = (comando[1], comando[2], comando[3])
				print "Atualizado antecessor de: " + str(self.id) + " para " + str(self.antecessor)
				
			if comando[0] == 'ping':
				print 'pong'
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
	
	while True:
		time.sleep(3)
	
		noId, noHost, noPorta = no.sucessor
		if noId != no.root[0]:
			print "ping"
			if 'ack' != sock.enviar('ping', (noHost, int(noPorta))):
				print "Sucessor de " + str(no.id) + " nao responde!"
				noId, noHost, noPorta = no.sucessorIm

				if 'ack' == sock.enviar('ping', (noHost, noPorta)):
					print "Atualizando sucessor..."
					no.sucessor = no.sucessorIm
					no.sucessorIm = encontrarSucessor(no.sucessor)
					no.atualizarAnt(no.sucessor, (no.id, no.host, no.port))
				else:
					print "Nao foi posivel recuperar a rede!"
'''
def percorrerDHT(self, root):
	if root == None:
		print "DHT vazio"
	else:
		print "Nos DHT"
		no = root
		chave = self.Chave((no[1], no[2]))
		print "Elemento: " + str(no[0]) + " chave: " + str(chave)
		while no != root:
			no = self.encontrarSucessor(no)
			chave = self.Chave((no[1], no[2]))
			print "No: " + str(no[0]) + " chave: " + str(chave)
			
'''			

	
	
def	main():
	
	host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
	porta = raw_input("Escreva um numero inteiro para a porta: ") # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala
	ender = (host, int(porta))
	
	arquivo = raw_input("Digite o nome do arquivo que contem o nó: ")

	n1 = No(ender, arquivo)
	rendezvous = (socket.gethostbyname(socket.gethostname()), 12345)
	n1.entrarDHT(rendezvous)


	
if __name__ == "__main__":
	main()


