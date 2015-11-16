import socket
import random
import md5

K = 2 # numero de bits
class DHT:
	
	def __init__(self):
		self.tamanho_rede = 2**K
		self.nos = {}
		self.ids = []
		
		#Inicializa o servidor rendezvous
		host = socket.gethostname()
		port = 12345
		orig = (host, port)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind((host, port))

		print "Servidor Iniciado"

		while True:
			try:
				"""
					Falta tratar ordem das mensagens
					Falta tratar chegada de mensagens duplicadas no servidor
					Falta gerar ID unico
				"""
				msg, no = s.recvfrom(1024)
				dest = (no[0], no[1])
				if (msg == 'Hello'):
					print ("No "+ str(no[0])+" diz: "+ msg)
					id = self.gerarID()
					print(id)
					s.sendto(str(id), dest)
					s.settimeout(2) # inicia aguardo de resposta Ack timeOut 
				if(msg == 'Ack'):
					print ("No "+ str(no[0])+" diz: "+ msg)
					s.settimeout(None) 
			except socket.timeout: # se nao receber o ack
				s.sendto(id, dest)
				s.settimeout(2)
		s.close()
	
	# Gera id do novo no	
	def gerarID(self):
		id = int(random.uniform(0, 2**K))
		m = md5.new()
		m.update(str(id))
		return long(m.hexdigest(), 16)
	


def main():
	rede = DHT()
	rede.iniciar_rendezvous()
		
if __name__ == "__main__":
	main()
	