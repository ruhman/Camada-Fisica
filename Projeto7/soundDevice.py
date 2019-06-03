import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import time as tm
import math
import peakutils
from scipy.fftpack import fft
from scipy import signal as window
from matplotlib import animation 


fs = 44100
duration = 1

figura = plt.figure(figsize = (10,4), facecolor="w")
figura.canvas.set_window_title("Grafico")
eixoX1 = figura.add_subplot(1,1,1)

sd.default.samplerate = fs
sd.default.channels = 1
arquivo_audio = "./audio/recebido"

def generateFilePath(fileName, counter):
    return fileName + str(counter) + ".wav"

def record_to_file(file, data, fs):
    sf.write(file, data, fs)

def soundDecoder(i):
    time=1
    tempo=np.linspace(0, time, fs*time)
    audio = sd.rec(int(duration*fs), fs, channels=1)
    sd.wait()
    y = audio[:,0]
    record_to_file(generateFilePath(arquivo_audio, 1), y, fs)
    ff = ouveAudio(y)
    if ff != 0:
        a0 = str(ff[0])
        a1 = str(ff[1])
        b = tom(ff[0], ff[1])
        eixoX1.clear()
        plt.xlim(0.01,0.02)
        eixoX1.plot(tempo[0:1000000], y[0:1000000])
        ax1 = figura.add_subplot(1,2,2)
        ax1.set_xlabel('Frequencia')
        ax1.set_ylabel('Decibel')
        ax1.plot(ff[2],ff[3])
        print("frequencias: {0} Hz, {1}Hz".format(a0,a1))
        print("tom: {}".format(b))
        print("-----------------------------------------")

def fourier(sinal, fs):
        N  = len(sinal)
        T  = 1/fs
        if T != 0:
            xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
            yf = fft(sinal)
            return(xf, yf[0:N//2])
        else:
            return 0,0

def ouveAudio(y):
    if arquivo == 0:
        fs=44100
        X, Y = fourier(y, fs)

        if Y.any() != 0:
            return processaSom(Y,X)
        else:
            return 0
        
    else:
        y, fs = sf.read(arquivo.rstrip())
        X, Y = fourier(y, fs)

        if Y.any() != 0:
            return processaSom(Y,X)
        else:
            return 0

def processaSom(Y,X):
    ymax = 20000
    new_y =[]
    for y in Y:
        new_y.append(10*math.log(np.abs(y)/ymax))

    array_y = np.array(new_y)

    indexes = peakutils.indexes(array_y, thres=0.86, min_dist=0)
    peaks_list = []
    for e in indexes:
        peaks_list.append(e)
        
    max1 = max(peaks_list)
    peaks_list.remove(max1)
    max2 = max(peaks_list)
    return(max2, max1, X, new_y)

def tom(f1, f2):
    f1real = np.linspace(f1-10,f1+10,21)
    f2real = np.linspace(f2-10,f2+10,21)
    if 697 in f1real:
        if 1209 in f2real:
            return "1"
        elif 1336 in f2real:
            return "2"
        elif 1477 in f2real:
            return "3"

    elif 770 in f1real:
        if 1209 in f2real:
            return "4"
        elif 1336 in f2real:
            return "5"
        elif 1477 in f2real:
            return "6"

    elif 852 in f1real:
        if 1209 in f2real:
            return "7"
        elif 1336 in f2real:
            return "8"
        elif 1477 in f2real:
            return "9"

    elif 941 in f1real:
        return "0"
    else:
        return "Opa deu ruim"

print("Escolha modo: 1 - Ouvir 2 - Arquivo")
modo = int(input(""))
if modo == 1:
    arquivo = 0
if modo == 2:
    print ("Diretorio do arquivo (arraste pro terminal): ")
    arquivo = input("")


decoder = animation.FuncAnimation(figura, soundDecoder, interval=1000)

plt.show()




