import socket
import random
import md5
from classe_no import *
from classe_socket import *


class DHT:
	
	def __init__(self):

		self.nos = {}
		self.ids = []

		self.root = {} # root (id:(IP, Porta))
		
		#Inicializa o servidor rendezvous
		host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
		porta = 12345
		servidor = (host, porta)
		serv = socketUDP(servidor)
		
		msg = ""
		while msg != "QSAIR": 
			msg, ender = serv.receber(1024)
			
			if (msg == 'Hello') and (len(self.nos) < MAX_NO - 1):
				print ("No "+ str(ender[0])+" diz: "+ msg)
				id = self.gerarID(1)
				
				print(id)
				
				#serv.enviar(env, ender)	# envia ID do no
				self.nos[id] = [ender[0], ender[1]] # acrescenta novo no (com seu ip e porta ) ao dicionario de nos
				
				# OBS: verificar caso de n conseguir ter sucesso na entrega da mensagem
				if not self.root: # se o dicionario esta vazio
					self.root[id] = [ender[0], ender[1]] 
					
					print "Root serv"
					env = str(id) +'|'+ str(id) +'|'+ str(ender[0]) +'|'+ str(ender[1])
					serv.enviar(env, ender) # informa ao no que ele eh o root
				else:
					rootID = self.root.keys()
					rootIP, rootPorta = self.root[rootID[0]]
					
					env = str(id) +'|'+ str(rootID[0]) +'|'+ str(rootIP) +'|'+ str(rootPorta) 
					serv.enviar(env, ender) # informa ao no qual no eh o root
					
			elif len(self.nos) == MAX_NO - 1:
				print "A rede ja esta cheia!\n"
				serv.enviar("RC", ender) # informa a um no que deseja entrar na rede  que a rede esta cheia
		serv.desconectar()

	# Gera id do novo no	
	def gerarID(self, op = 1):
		if op == 1:
			id = int(random.uniform(0, MAX_NO - 1)) # gera id aleatorio entre 0 e 
			while (id in self.nos): # verifica se o id ja exites na lista de nos
				id = int(random.uniform(0, MAX_NO - 1))
			#m = md5.new()
			#m.update(str(id))
			#return long(m.hexdigest(), 16)
			return id
		else:
			id = 2^(int(random.uniform(1, MAX_NO)))
			while (id in self.nos): # verifica se o id ja exites na lista de nos
				id = 2^(int(random.uniform(1, MAX_NO)))
			return id
		
		
def main():
	rede = DHT()
	rede.iniciar_rendezvous()
		
if __name__ == "__main__":
	main()
	