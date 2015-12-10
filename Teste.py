#!/usr/bin/env python
# encoding: utf-8

import time
import socket
import threading               # Importa modulo socket
import os
import hashlib

conexao = False
N = 6
MAX_NO = 2**N
class No:
	def __init__(self, endereco, sock):	
		self.root = ()
		self.atalho = {} # conterao o (ID, IP, Porta) do no que quada a chave correspondente
		self.chaves = [] # conetem as chaves do No corrente
		self.sucessor = ()
		self.sucessorIm = ()
		self.antecessor = ()

		self.host, self.port = endereco
		self.clien = sock # Retirar se for o caso

def calculaHash(nome):
	strHash = hashlib.md5(nome)
	mod = int(strHash.hexdigest(), 16) % MAX_NO
	return mod

def criarArquivo():
	nomeArq = raw_input("Digite o nome do arquivo a ser criado: ")
	valHash = calculaHash(nomeArq)
	print chaves
	#chaves = (valHash, nomeArq)
	#print str(valHash)
	print "Arquivo criado com sucesso"
	print chaves

def buscarArquivo():
	nomeArq = raw_input("Digite o nome do arquivo que se deseja realiza a busca: ")
	print "Arquivo existente na base"

def desconectarBase():
     global conexao
     conexao = False
     print "No desconectado do servidor"
    
	

def opcaoInvalida():
	print "Opcao de menu invalida!"

funcMenu = {1 : criarArquivo,
			2 : buscarArquivo,
			3 : desconectarBase }

def switch(x):
	try:
		funcMenu[x]()
	except:
		opcaoInvalida()

def menu(ender):
    global conexao
    conexao = True
    
    while conexao == True:
        os.system("clear")
        print "==========================================================="
        print "=  IP do no: "+ender[0]+" | Porta: "+str(ender[1])+"                      ="
        print "==========================================================="
        print "                         MENU"
        print " 1 - Criar arquivo"
        print " 2 - Buscar arquivo na rede"
        print " 3 - Desconectar"
        print ""
        
        opcao = input(" Escolha uma opcao: ")
        
        switch(opcao)
        
        print "Conexao: "+str(conexao)
		
        pause = raw_input("Tecle Enter para continuar...")
		
		
		
	    
def	main():
	host = socket.gethostbyname(socket.gethostname())
	porta = raw_input("Escreva um numero inteiro para a porta: ")
	porta = int(porta)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP 	
	sock.bind((host, porta)) # Espera conecoes no endereco e porta fornecidos
	
	ender = (host, porta)

	menu(ender)

	
if __name__ == "__main__":
	main()

