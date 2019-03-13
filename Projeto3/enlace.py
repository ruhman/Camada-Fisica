#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
# 17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX


class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica = fisica(name)
        self.rx = RX(self.fisica)
        self.tx = TX(self.fisica)
        self.connected = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """

        pacote, lenPayload = self.cria_package(data)
        self.tx.sendBuffer(pacote)
        return lenPayload

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ')
        data, size = self.rx.getNData()
        payload = self.desfaz_package(data)

        return(payload, len(payload))

    def cria_package(self, payload):

        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FF FF FF")
        payload_size = len(payload)

        for i in range(len(payload)):

            if payload[i:i+4] == eop:
                p1 = payload[0:i]
                p2 = byte_stuff + payload[i:]
                payload = p1 + p2

        head = (payload_size).to_bytes(12, byteorder="big")
        package = head + payload + eop
        print(len(payload))
        # print(package)
        return package, len(payload)

    def desfaz_package(self, package):

        head_size = 12
        found_eop = False
        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FF FF FF")
        head = package[0:head_size]
        package = package[head_size:]
        payload_size = int.from_bytes(head, byteorder="big")
        for i in range(len(package)):
            if package[i:i+4] == eop:
                if package[i-1] == byte_stuff:
                    p1 = package[0:i-1]
                    p2 = package[i:]
                    package = p1 + p2
                else:
                    found_eop = True
                    print("EOP encontrado na posição:{0}".format(i))
                    package = package[0:-4]
                    if len(package) != payload_size:
                        print("ERRO! Bytes Payload recebido:{0}".format(
                            len(package)))
                        print("Bytes que foram enviados:{0}".format(
                            payload_size))
                    break
        if not found_eop:
            print("ERRO! EOP não encontrado")
        payload = package
        # print(len(payload))
        return payload
