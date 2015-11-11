import socket

def Main():
    host = '127.0.0.1'	#Endereco IP do Servidor
    port = 5001			#Porta que o Servidor esta

    server = ('127.0.0.1',5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP
    s.bind((host, port))	#Esperara conexoes no endereco e porta fornecidos

    message = raw_input("-> ")
    while message != 'q':
        s.sendto(message, server)
        data, addr = s.recvfrom(1024)
        print 'Recebido pelo servidor: ' + str(data)
        message = raw_input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
