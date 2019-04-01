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
        self.client_sync()
        self.client_transmission(data)
        self.client_encerramento()

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ')
        self.server_sync()
        payload = self.server_transmission()
        self.server_encerramento()

        return(payload, len(payload))

    def client_sync(self):
        sync1 = False
        sync2 = False
        payload = (0).to_bytes(1, byteorder="big")
        sync_package = self.tx.cria_package(payload, 1, 0, 0, 0)
        sync_package3 = self.tx.cria_package(payload, 3, 0, 0, 0)
        print(sync_package)
        self.tx.sendBuffer(sync_package)
        timer = time.time()
        while not sync1:
            data, _ = self.rx.getNData()
            payload, tipo, ok, _, _, _ = self.rx.desfaz_package(
                data)
            if tipo == 2 and ok:
                sync1 = True
                print("recebeu tipo 2")
                break

            run_time = time.time() - timer
            if run_time > 5:
                print("Error: not receive type 2 ---------> Reenviando tipo 1")
                self.tx.sendBuffer(sync_package)
                timer = time.time()

        self.tx.sendBuffer(sync_package3)
        timer = time.time()
        while not sync2:
            data, _ = self.rx.getNData()
            payload, tipo, ok, _, _, _ = self.rx.desfaz_package(
                data)
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
        sync_package2 = self.tx.cria_package(payload_nulo, 2, 0, 0, 0)
        sync_package40 = self.tx.cria_package(payload_nulo, 40, 0, 0, 0)

        while not sync1:
            data, _ = self.rx.getNData()
            _, tipo, ok, _, _, _ = self.rx.desfaz_package(
                data)
            if tipo == 1 and ok:
                sync1 = True
                print("recebeu tipo 1")
                break

        self.tx.sendBuffer(sync_package2)
        print("Enviou tipo 2")
        timer = time.time()
        while not sync2:
            data, _ = self.rx.getNData()
            _, tipo, ok, _, _, _ = self.rx.desfaz_package(
                data)
            if tipo == 3 and ok:
                sync2 = True
                print("recebeu tipo 3")
                break

            run_time = time.time() - timer
            if run_time > 5.0:
                print("Erro: Type 3 not received --------> Reenviando tipo 2")
                self.tx.sendBuffer(sync_package2)
                timer = time.time()
        self.tx.sendBuffer(sync_package40)

    def client_transmission(self, payload):
        payloadnulo = (0).to_bytes(1, byteorder="big")
        timer = time.time()
        lista_pacotes, total_pacotes = self.separa_pacotes(payload)

        for i in range(len(lista_pacotes)):
            sync_package4 = self.tx.cria_package(
                lista_pacotes[i], 4, i+1, len(lista_pacotes), 0)
            self.tx.sendBuffer(sync_package4)
            print("Mandou o pacote {0}/{1}".format(i+1, len(lista_pacotes)))
            while True:
                data, _ = self.rx.getNData()
                payload, tipo, ok, _, n_total, pacote_esperado = self.rx.desfaz_package(
                    data)
                if tipo == 5 and ok:
                    sync1 = True
                    print("recebeu tipo 5")
                    break
                elif tipo == 6 and ok:
                    self.tx.sendBuffer(sync_package4)
                    print("recebeu tipo 6")
                    timer = time.time()

                elif tipo == 8 and ok:
                    sync_package8 = self.tx.cria_package(
                        lista_pacotes[pacote_esperado], 4, pacote_esperado, n_total, 0)
                    self.tx.sendBuffer(sync_package8)

                run_time = time.time() - timer
                if run_time > 4:
                    print("Tipo 5 ou 6 NAO recebido ------> Reenviando tipo 4 | {0} / {1}  Tamanho:{2} bytes".format(
                        i+1, total_pacotes, len(lista_pacotes[i])))
                    self.tx.sendBuffer(sync_package4)
                    timer = time.time()

    def server_transmission(self):
        payloadnulo = (0).to_bytes(1, byteorder="big")
        sync_package5 = self.tx.cria_package(payloadnulo, 5, 0, 0, 0)
        sync_package6 = self.tx.cria_package(payloadnulo, 6, 0, 0, 0)
        lista_fragmentada = []
        pacote_davez = 1
        while True:
            data, size = self.rx.getNData()
            payload, tipo, ok, n_pacote, total_pacotes, _ = self.rx.desfaz_package(
                data)

            # if n_pacote != pacote_davez:
            #   print("ERRO: Deveria ter recebido {0} e recebeu {1}".format(pacote_davez, n_pacote))
            #  while True:
            ##     sync_package8 = self.tx.cria_package(payloadnulo, 8, 0, 0, pacote_davez)
            #   self.tx.sendBuffer(sync_package8)

            if tipo == 4 and ok:
                if n_pacote != pacote_davez:
                    print("ERRO: Deveria ter recebido {0} e recebeu {1}".format(
                        pacote_davez, n_pacote))
                    sync_package8 = self.tx.cria_package(
                        payloadnulo, 8, 0, 0, pacote_davez)
                    self.tx.sendBuffer(sync_package8)
                    timer = time.time()
                    while True:
                        payload, tipo, ok, n_pacote, total_pacotes, pacote_esperado = self.rx.desfaz_package(
                            data)
                        if tipo == 4 and ok:
                            break
                        run_time = time.time() - timer
                        if run_time > 5:
                            self.tx.sendBuffer(sync_package8)

                pacote_davez += 1
                lista_fragmentada.append(payload)
                self.tx.sendBuffer(sync_package5)
                sync1 = True
                print(
                    "recebeu tipo 4 | {0}/{1} CORRETO, ENVIA 5".format(n_pacote, total_pacotes))
                if n_pacote == total_pacotes:
                    break

            elif tipo == 4 and not ok:
                self.tx.sendBuffer(sync_package6)
                print("Recebeu tipo 4 INCORRETO, Envia 6")

        compilado = bytes.fromhex("FF")
        for fragment in lista_fragmentada:
            compilado += fragment

        compilado = compilado[1:]

        return compilado

    def client_encerramento(self):
        time.sleep(4)
        payloadnulo = (0).to_bytes(1, byteorder="big")
        sync_package7 = self.tx.cria_package(payloadnulo, 7, 0, 0, 0)
        print("enviou tipo 7")
        self.tx.sendBuffer(sync_package7)

    def server_encerramento(self):
        encerra = False
        package_arbitrario = bytes.fromhex("F5 A3 AA C3 C3 B5 B4")
        timer = time.time()
        while not encerra:
            data, _ = self.rx.getNData()
            _, tipo, _, _, _, _ = self.rx.desfaz_package(
                data)
            if tipo == 7:
                print("recebeu tipo 7, conexao encerrada")
                break
            run_time = time.time() - timer
            if run_time > 10:
                break

    def separa_pacotes(self, data):
        lista_pacotes = []
        while len(data) > 128:
            pacote = data[0:128]
            data = data[128:]
            lista_pacotes.append(pacote)

        if len(data) > 0:
            pacote = data
            lista_pacotes.append(pacote)
        return lista_pacotes, len(lista_pacotes)
