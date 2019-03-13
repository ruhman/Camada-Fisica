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
# from construct import *

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

        self.client_sync()
        self.client_transmission(data)
        self.client_encerramento()

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        self.server_sync()
        payload = self.server_transmission()
        self.server_encerramento()

        return(payload, len(payload))

    def cria_package(self, payload, tipo):
        # pega os dados e empacota com HEAD, EOP e byte Stuffing

        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FF FF FF")
        payload_size = len(payload)

        for i in range(len(payload)):

            if payload[i:i+4] == eop:
                p1 = payload[0:i]
                p2 = byte_stuff + payload[i:]
                payload = p1 + p2
        msg_type = (tipo).to_bytes(1, byteorder="big")
        msg_size = (payload_size).to_bytes(3, byteorder="big")
        head = msg_type + msg_size
        package = head + payload + eop

        return package

    def desfaz_package(self, package):
        # Faz o desempacotamento dos dados baseado-se no protocolo GG7.
        # Separa o payload do restante e verifica se o tamanho do payload esta correto
        ok = True
        found_eop = False
        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FF FF FF")
        head = package[0:4]
        tipo = int(head[0])
        package = package[4:]
        payload_size = int.from_bytes(head[1:], byteorder="big")
        for i in range(len(package)):
            if package[i:i+4] == eop:
                if package[i-1] == byte_stuff:
                    # retira os bytes stuff
                    p1 = package[0:i-1]
                    p2 = package[i:]
                    package = p1 + p2
                else:
                    found_eop = True
                    print("EOP encontrado na posição:{0}".format(i))
                    package = package[0:-4]
                    if len(package) != payload_size:
                        ok = False
                        print("ERRO! Número de Bytes do Payload diferentes do informado no HEAD. Bytes Payload recebido:{0}".format(
                            len(package)))
                        print("Bytes que foram enviados:{0}".format(
                            payload_size))
                    break
        if not found_eop:
            ok = False
            print("ERRO! EOP não encontrado")
        payload = package
        return payload, tipo, ok

    def client_sync(self):
        sync1 = False
        sync2 = False
        payload = (0).to_bytes(1, byteorder="big")
        sync_package = self.cria_package(payload, 1)
        sync_package3 = self.cria_package(payload, 3)
        self.tx.sendBuffer(sync_package)
        timer = time.time()
        while not sync1:
            data, _ = self.rx.getNData()
            payload, tipo, ok = self.desfaz_package(data)
            if tipo == 2 and ok:
                sync1 = True
                print("recebeu tipo 2")
                break

            run_time = time.time() - timer
            if run_time > 5:
                print("Error: not receive type 2 ")
                self.tx.sendBuffer(sync_package)
                print("Enviando tipo 1")
                timer = time.time()

        self.tx.sendBuffer(sync_package3)
        timer = time.time()
        while not sync2:
            data, _ = self.rx.getNData()
            payload, tipo, ok = self.desfaz_package(data)
            if tipo == 40 and ok:
                sync2 = True
                print("recebeu tipo 40")
                break
            run_time = time.time() - timer
            if run_time > 5.0:
                print("mandou tipo 3")
                self.tx.sendBuffer(sync_package3)
                timer = time.time()

    def server_sync(self):
        sync1 = False
        sync2 = False
        payload_nulo = (0).to_bytes(1, byteorder="big")
        sync_package2 = self.cria_package(payload_nulo, 2)
        sync_package40 = self.cria_package(payload_nulo, 40)

        while not sync1:
            data, _ = self.rx.getNData()
            _, tipo, ok, = self.desfaz_package(data)
            if tipo == 1 and ok:
                sync1 = True
                print("recebeu tipo 1")
                break

        self.tx.sendBuffer(sync_package2)
        timer = time.time()
        while not sync2:
            data, size = self.rx.getNData()
            payload, tipo, ok = self.desfaz_package(data)
            if tipo == 3 and ok:
                sync2 = True
                print("recebeu tipo 3")
                break

            run_time = time.time() - timer
            if run_time > 5.0:
                print("Erro: Type 3 note received")
                self.tx.sendBuffer(sync_package2)
                print("Mandou tipo 2")
                timer = time.time()
        self.tx.sendBuffer(sync_package40)

    def client_transmission(self, payload):
        sync_package4 = self.cria_package(payload, 4)
        self.tx.sendBuffer(sync_package4)
        sync1 = False
        timer = time.time()
        while not sync1:
            data, _ = self.rx.getNData()
            payload, tipo, ok = self.desfaz_package(data)
            if tipo == 5 and ok:
                sync1 = True
                print("recebeu tipo 5")
                break
            elif tipo == 6 and ok:
                self.tx.sendBuffer(sync_package4)
                print("recebeu tipo 6")
                timer = time.time()

            run_time = time.time() - timer
            if run_time > 5.0:
                print("Erro: type 5 or 6 not received")
                print("mandou tipo 4")
                self.tx.sendBuffer(sync_package4)
                timer = time.time()

    def server_transmission(self):
        payloadnulo = (0).to_bytes(1, byteorder="big")
        sync_package5 = self.cria_package(payloadnulo, 5)
        sync_package6 = self.cria_package(payloadnulo, 6)
        sync1 = False
        while not sync1:
            data, size = self.rx.getNData()
            payload, tipo, ok = self.desfaz_package(data)
            if tipo == 4 and ok:
                self.tx.sendBuffer(sync_package5)
                sync1 = True
                print("recebeu tipo 4 CORRETO, ENVIA 5")
                break
            elif tipo == 4 and not ok:
                self.tx.sendBuffer(sync_package6)
                print("Recebeu tipo 4 INCORRETO, Envia 6")

        return payload

    def client_encerramento(self):
        time.sleep(4)
        payloadnulo = (0).to_bytes(1, byteorder="big")
        sync_package7 = self.cria_package(payloadnulo, 7)
        print("enviou tipo 7")
        self.tx.sendBuffer(sync_package7)

    def server_encerramento(self):
        end = False
        while not end:
            data, _ = self.rx.getNData()
            _, tipo, _ = self.desfaz_package(data)
            if tipo == 7:
                print("recebeu tipo 7, conexao encerrada")
                break
