import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import math
import peakutils
from scipy import signal as sg
import sounddevice as sd
from itertools import zip_longest
from scipy.fftpack import fft

def filter(signal, cutoff_hz, fs):
        nyq_rate = fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        
        return(sg.lfilter(taps, 1.0, signal))

def fourier(sinal, fs):
        N  = len(sinal)
        T  = 1/fs
        if T != 0:
            xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
            yf = fft(sinal)
            return(xf, yf[0:N//2])
        else:
            return 0,0

def senoide(freq,sample,rate):
    x = np.linspace(0, len(sample)/rate, len(sample))
    y = np.sin(2 * math.pi * x * freq)
    return (x,y)

cutoff_hz = 3000
fs = 44100

#Le arquivos
m1, rate1 = sf.read('audios-prontos/m1.wav')
m2, rate2 = sf.read('audios-prontos/m2.wav')

#Filtro passa baixa
m1_filtered = filter(m1, cutoff_hz, rate1)
m2_filtered = filter(m2, cutoff_hz, rate2)

#Fourier dos audios + plot
f1, Y1 = fourier(m1_filtered, rate1)
plt.plot(f1, np.abs(Y1), label='m1')
f2, Y2 = fourier(m2_filtered, rate2)
plt.plot(f2, np.abs(Y2), label='m2')
plt.title('Modulo Fourrier (m1 e m2)')
plt.xlim(0,cutoff_hz)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#Freq arbritarias
fC1 = 5000
fC2 = 15000

t1, c1 = senoide(fC1,m1_filtered,rate1)
t2, c2 = senoide(fC2,m2_filtered,rate2)

# Fourrier c1 e c2 + plot
c1f, Y1c = fourier(c1, rate1)
c2f, Y2c = fourier(c2, rate2)
plt.plot(c1f, np.abs(Y1c), label='c1')
plt.plot(c2f, np.abs(Y2c), label='c2')
plt.title('Modulo Fourrier (c1 e c2)')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#Modular AM
am = c1*m1_filtered
am2 = c2*m2_filtered

# Fourrier AM Modulada + plot
amf, Y1f = fourier(am, rate1)
am2f, Y2f = fourier(am2, rate2)
plt.plot(amf, np.abs(Y1f), label='AM')
plt.plot(am2f, np.abs(Y2f), label='AM2')
plt.title('Modulo Fourrier (AM e AM2)')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

sd.play(am,rate1)
sd.wait()

sd.play(am2,rate2)
sd.wait()

result = [x + y for x, y in zip_longest(am, am2, fillvalue=0)]

# Fourrier da soma das AM Moduladas
sr, Yr = fourier(result, rate1)
plt.plot(sr, np.abs(Yr), label='Sinal resultante')
plt.title('Modulo Fourrier (AM + AM2)')
plt.show()

sd.play(result,rate1)
sd.wait()
print("Salvando arquivo como result.wav")
sf.write('result.wav', result, fs)