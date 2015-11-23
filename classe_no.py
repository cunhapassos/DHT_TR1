import socket               # Import socket module

m = 6
class No:
	def __init__(self):
		self.id = None
		self.root = False
		self.sucessor = None
		self.antecessor = None

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
		host = socket.gethostname() # Get local machine name
		port = 12345                # Reserve a port for your service.
		dest = (host, port)

		#s.connect(dest)
		aux = True
		env = 'Hello'
		s.sendto(env, dest)
		s.settimeout(2)
		while aux:
			try:
				msg, origem = s.recvfrom(1024)
				dest = (origem[0], origem[1])
				
				if msg == 'RC':
					aux = False
					s.settimeout(None)
					
				elif msg == 'root':
					root = True
					self.sucessor = self
					self.antecessor = self
					env = 'Ack_root'
					s.sendto(env, dest)
					print "No "+ self.id + " eleito no Root!"
					aux = False 
					
				elif msg == 'ping':
					env = 'pong'
					s.sendto(env, dest)
				
				else:
					print ("Servidor "+ str(origem[0])+" diz: "+ msg)
					self.id = msg # recebe o Id que o servidor enviou
					env = 'Ack_id'
					s.sendto(env, dest)
					s.settimeout(None)
					
			except socket.timeout: # se nao receber o ID
				s.sendto(env, dest)
		s.close()                  # Close the socket when done
		
"""
	def entrarNoDHT(self, no): # enviar mensagens p outros no atualizarem suas tabelas de atalhos
		if (self == no):
			for i in range(m):
				derivacao = (self.id + (2**i)) % (2**m)
				self.tabAtalhos[derivacao] = self
				self.antecessor = self
		else:
			print "teste"
				
	def iniciarTabAtalhos(self, no): 
		for i in range(len(self.tabAtalhos)):
			derivacao = (self.id + (2**i)) % (2**m)
			self.tabAtalhos[derivacao] = self.id

	def imprimirTabAtalhos(self, no):
		print (self.tabAtalhos)
"""
def	main():
	n1 = No()
	#n1.iniciarTabAtalhos(n1)
	#n1.imprimirTabAtalhos(n1)
	
if __name__ == "__main__":
	main()
