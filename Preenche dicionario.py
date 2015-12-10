#!/usr/bin/env python
# encoding: utf-8

import hashlib

def	main():
    d = {}
    cont = 6
    
    while cont != 0:
        arq = raw_input("Digite o nome do arquivo: ")
        strHash = hashlib.md5(arq)
        print strHash.hexdigest()
        #print type(strHash.hexdigest()
        
        mod = int(strHash.hexdigest(), 16) % 2
        print "Valor em modulo: "+str(mod)
        
        if d.has_key(mod):
            print "Tem chave"
            d[mod].append(arq)
            print d
        else:
            print "Nao tem chave"
            d[mod] = [arq]
            print d
        
        cont -= 1
    
    #print d

if __name__ == "__main__":
	main()
