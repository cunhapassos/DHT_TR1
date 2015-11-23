#!/usr/bin/env python
# encoding: utf-8
"""
testeClienteSocketUDP.py

Created by Paulo Passos on 2015-11-22.
Copyright (c) 2015 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import socket
from socketUDP import *

host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
port = 12346 # como o ip do cliente e servidor sao iguais a porta deve ser diferente, caso contrario da pala 
orig = (host, port)
dest = (host, 12345)
serv = socketUDP(orig)

print('Para sair use QSAIR') 
msg = raw_input("Escreva a mensagem: ")

while msg != "QSAIR": 
	serv.enviar(msg, dest)
	msg = raw_input("Escreva a mensagem: ")

serv.desconectar()
