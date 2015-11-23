import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
dest = (host, port)

#s.connect(dest)
c = True

s.sendto('Hello', dest)
s.settimeout(2)
while c:
	try:
		id, servidor = s.recvfrom(1024)
		print ("Servidor "+ str(servidor[0])+" diz: "+ id)
		s.sendto('Ack', dest)
		s.settimeout(None)
		c = False 
	except socket.timeout: # se nao receber o ID
		s.sendto('Hello', dest)

s.close()                     # Close the socket when done