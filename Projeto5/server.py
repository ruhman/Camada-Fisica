
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
# 17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *
import time
from array import array

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem14401"  # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)
baudrate = 115200


print("porta COM aberta com sucesso")


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # verificar que a comunicação foi aberta
    print("comunicação aberta")

    # Faz a recepção dos dados

    print("Recebendo dados .... ")
    rxBuffer, nRx = com.getData()
    x = open('test2.png', 'wb')
    x.write(rxBuffer)
    x.close()

    # log
    print("Lido              {0} bytes ".format(nRx))

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
