import socket

class socketUDP:
	
	# Cria ou recebe um socket UDP
	def __init__(self, (host, porta)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP 	
		self.sock.bind((host, porta)) # Espera conecoes no endereco e porta fornecidos
		print host + " esta aguardando conexoes..."
	
	def enviar(self, msg, dest):
		self.sock.settimeout(0.2) # deifine um tempo para aguardar o retorno de mensagem enviada
		flag = 0
		
		#print "Enviando mensagem para " + dest[0]
		self.sock.sendto(msg, dest)
		
		while flag < 20:
			#print "Aguardando ack..."
			
			try:
				dado, orig = self.sock.recvfrom(1024)
				dados = dado.split('|', 1)
				#print "0 " + dados[0] + " 1 "+ dados[1] + str(dest) + str(orig)
				if (dados[0] == 'ack') and (dados[1] == msg) and (dest == orig):
					#print "Ack recebido, Enviando ackr!"
					ackr = 'ackr|' + dados[1]
					self.sock.sendto(ackr, dest)
					self.sock.settimeout(None)
					return 'ack'
				
			except socket.timeout:
				self.sock.sendto(msg, dest)
				flag += 1
		return 'nack'
	# OBS: falta tratar casos em que nunca se recebe o ack aou ackr de volta, talvez colocar um contador no lugar da flag resolva		
	def receber(self, tam):
		self.sock.settimeout(None)
		msg, orig = self.sock.recvfrom(tam)
		flag = 0
		
		self.sock.settimeout(0.2)
		pacote = 'ack|' + msg
		self.sock.sendto(pacote, orig)
		
		while flag < 20:
			try:
				dado, orig1 = self.sock.recvfrom(1024)
				dados = dado.split('|', 1)
				#print "0 " + dados[0] + " 1 "+ dados[1] + str(orig) + str(orig1)
				if (dados[0] == 'ackr') and (dados[1] == msg) and (orig == orig1):
					self.sock.settimeout(None)
					return (msg, orig)	
			except socket.timeout:
				self.sock.sendto(pacote, orig)
				flag += 1
		return ('nack', orig) 
				
	def desconectar(self):
		print "Encerrando conexao..."
		self.sock.close()
		 