import socket
import random
import md5
from classe_no import *
from classe_socket import *

K = 7 # numero de bits
class DHT:
	
	def __init__(self):
		self.tamanho_rede = 2**K
		self.nos = {}
		self.ids = []
		self.root = {} # root (id:(IP, Porta))
		
		#Inicializa o servidor rendezvous
		host = socket.gethostname()
		porta = 12345
		servidor = (host, porta)
		s = socketUDP(servidor)
		
		while msg != "QSAIR": 
			msg, orig = serv.receber(1024)
			
			if (msg == 'Hello') and (len(self.nos) < K-1):
				print ("No "+ str(no[0])+" diz: "+ msg)
				id = self.gerarID(1)
				print(id)
				env = str(id)
				s.enviar(env, orig)	# envia ID do no
				self.nos[id] = (no[0], no[1]) # acrescenta novo no (com seu ip e porta ) ao dicionario de nos
				
				# OBS: verificar caso de n conseguir ter sucesso na entrega da mensagem
				if self.root == None:
					env = 'root' 
					s.enviar(env, orig) # informa ao no que ele eh o root
				else:
					env = str(self.root)
					s.enviar(env, orig) # informa ao no qual no eh o root
					
					
			elif #  PAREI AKI
			
			
		serv.desconectar()
"""
		while True:
			try:
				"""
					Falta tratar ordem das mensagens
					Falta tratar chegada de mensagens duplicadas no servidor
				"""
				msg, no = s.recvfrom(1024)
				dest = (no[0], no[1])
				
				if (msg == 'Hello') and (len(self.nos) < K-1):
					print ("No "+ str(no[0])+" diz: "+ msg)
					id = self.gerarID(1)
					print(id)
					env = str(id)
					s.sendto(env, dest) # envia ID do no
					s.settimeout(2) # inicia aguardo de resposta Ack timeOut 

					
					
				elif(msg == 'Ack_id'): # recebe o Ack do ID que foi enviado
					print ("No "+ str(no[0])+" diz: "+ msg + "\n")
					#s.settimeout(None)
					if self.root == None: # se a rede ainda na possui root
						env = 'root'
						s.sendto(env, dest) # Envia informacao que o no eh o root
						s.settimeout(2) # inicia aguardo de resposta Ack timeOut 
					else:
						self.nos[id] = (no[0], no[1]) # acrescenta novo no (com seu ip e porta ) ao dicionario de nos
						env = str(self.root)
						s.sendto(env, dest)
					
				elif (msg == 'Ack_root'): # recebe o Ack que o noh sabe que eh o root
					s.settimeout(None)
					self.nos[id] = (no[0], no[1]) # acrescenta novo no (com seu ip e porta ) ao dicionario de nos
					root[id] = (no[0], no[1]) # coloca o primeiro no que entrou na rede como root
				
				elif len(self.nos) == K-1:
					print "A rede ja esta cheia!\n"
					s.sendto("RC", dest) # informa a um no que deseja entrar na rede  que a rede esta cheia
					
			except socket.timeout: # se nao receber os retornos 
				s.sendto(env, dest)
				s.settimeout(2)
		s.close()
"""	
	# Gera id do novo no	
	def gerarID(self, op = 1):
		if op == 1:
			id = int(random.uniform(0, K - 1)) # gera id aleatorio entre 0 e 
			while (id in self.nos): # verifica se o id ja exites na lista de nos
				id = int(random.uniform(0, K - 1))
			#m = md5.new()
			#m.update(str(id))
			#return long(m.hexdigest(), 16)
			return id
		else:
			id = 2^(int(random.uniform(1, K)))
			while (id in self.nos): # verifica se o id ja exites na lista de nos
				id = 2^(int(random.uniform(1, K)))

		
		
def main():
	rede = DHT()
	rede.iniciar_rendezvous()
		
if __name__ == "__main__":
	main()
	