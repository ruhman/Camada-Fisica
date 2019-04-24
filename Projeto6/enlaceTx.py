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

# Threads
import threading
from crc import CRC

# Class


class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica = fisica
        self.buffer = bytes(bytearray())
        self.transLen = 0
        self.empty = True
        self.threadMutex = False
        self.threadStop = False
        self.crc = CRC()

    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen = self.fisica.write(self.buffer)
                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen = 0
        self.buffer = data
        self.threadMutex = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)

    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)

    def cria_package(self, payload, tipo, n_pacote, total_pacotes, pacote_esperado):
        # pega os dados e empacota com HEAD, EOP e byte Stuffing

        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FE FD FC")
        payload_size = len(payload)
        crc_payload = self.crc.encodeData(payload)
        crc_payload = int(crc_payload, 2)

        for i in range(len(payload)):

            if payload[i:i+4] == eop:
                p1 = payload[0:i]
                p2 = byte_stuff + payload[i:]
                payload = p1 + p2

        msg_type = (tipo).to_bytes(1, byteorder="big")
        msg_size = (payload_size).to_bytes(3, byteorder="big")
        msg_n = (n_pacote).to_bytes(1, byteorder="big")
        total_n = (total_pacotes).to_bytes(1, byteorder="big")
        pacote_e = (pacote_esperado).to_bytes(1, byteorder="big")
        msg_crc = (crc_payload).to_bytes(3, byteorder="big")
        head = msg_type + msg_size + msg_n + total_n + pacote_e + msg_crc
        package = head + payload + eop
        overhead = len(package) / len(payload)
        print("OverHead:{0}".format(overhead))
        print(len(payload))
        return package
