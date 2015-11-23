#!/usr/bin/env python
# encoding: utf-8
"""
testeServSocketUDP.py

Created by Paulo Passos on 2015-11-22.
Copyright (c) 2015 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import socket
from socketUDP import *

host = socket.gethostbyname(socket.gethostname()) # obtem o endereco IP da maquina local a partir do hostname da maquina local
port = 12345
orig = (host, port)
msg =" "

serv = socketUDP(orig)


while msg != "QSAIR": 
	msg, orig = serv.receber(1024)
	print (str(orig[0])+" diz: " +msg)

serv.desconectar()

