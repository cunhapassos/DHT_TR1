import socket

def Main():
    host = '127.0.0.1' 	#Endereco IP do Servidor
    port = 5000			#Porta que o Servidor esta

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP
    s.bind((host,port))


    print "Servidor Iniciado."
    while True:
        data, addr = s.recvfrom(1024)	 #Recebe um dado de ate 1024 bytes retorna tambem o endereco de quem enviou
        print "mensagem de: " + str(addr)
        print "Do usuario conectado: " + str(data)
        data = str(data).upper()
        print "Enviado: " + str(data)
        s.sendto(data, addr) # retorna mensagem em maisculo para cliente
    c.close()

if __name__ == '__main__':
    Main()

