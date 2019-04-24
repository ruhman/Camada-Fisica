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


class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica = fisica
        self.buffer = bytes(bytearray())
        self.threadStop = False
        self.threadMutex = True
        self.READLEN = 1024
        self.crc = CRC()

    def thread(self):
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )

        # if self.getBufferLen() < size:
        #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        size = 0
        time_out = time.time()
        package_arbitrario = bytes.fromhex("F5 A3 AA C3 C3 B5 B4")

        while(self.getBufferLen() > size or self.getBufferLen() == 0):
            time.sleep(0.5)
            size = self.getBufferLen()
            run_time = time.time() - time_out

            if run_time > 4:
                return (package_arbitrario, len(package_arbitrario))

        return(self.getBuffer(size), size)

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def desfaz_package(self, package):
        # Faz o desempacotamento dos dados baseado-se no protocolo GG7.
        # Separa o payload do restante e verifica se o tamanho do payload esta correto
        ok = True
        found_eop = False
        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FE FD FC")
        head = package[0:10]
        tipo = int(head[0])
        n_pacote = int(head[4])
        total_pacotes = int(head[5])
        pacote_esperado = int(head[6])
        crc_chegou = int.from_bytes(head[7:], byteorder="big")
        package = package[10:]
        payload_size = int.from_bytes(head[1:4], byteorder="big")

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
        crc_calculado = self.crc.encodeData(payload)
        crc_calculado = int(crc_calculado, 2)
        if crc_calculado == crc_chegou:
            encoding = True
        else:
            encoding = False

        return payload, tipo, ok, n_pacote, total_pacotes, pacote_esperado, encoding
