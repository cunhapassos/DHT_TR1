import socket

host = socket.gethostname()
port = 12345
orig = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

print "Servidor Iniciado"
#c = True

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
			id = '1'
			s.sendto(id, dest)
			s.settimeout(2) # inicia aguardo de resposta Ack timeOut 
		if(msg == 'Ack'):
			print ("No "+ str(no[0])+" diz: "+ msg)
			s.settimeout(None) 
	except socket.timeout: # se nao receber o ack
		s.sendto(id, dest)
		s.settimeout(2)

s.close()