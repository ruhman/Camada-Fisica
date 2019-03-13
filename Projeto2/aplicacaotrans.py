
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
# 17/02/2018
#  Aplicação - Transmissor
####################################################

print("comecou")

from enlace import *
import time
from array import array
import tkinter as tk
from tkinter.filedialog import askopenfilename
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem14101"  # Mac    (variacao de)
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

    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    # como fazer isso
    print("gerando dados para transmissao :")

    with open("xd_favicon.png", "rb") as image:
        image_byte = image.read()
        img_byte = bytearray(image_byte)
    txLen = len(img_byte)

    # Transmite dado
    print(" Tamanho da imagem: {0} bytes".format(txLen))
    print("tentado transmitir .... {0} bytes".format(txLen))
    com.sendData(img_byte)

    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
