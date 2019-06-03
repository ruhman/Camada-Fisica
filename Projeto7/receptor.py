import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal as sg
import soundfile as sf
from scipy.fftpack import fft


def filter(signal, cutoff_hz, fs):
    nyq_rate = fs/2
    width = 5.0/nyq_rate
    ripple_db = 60.0  # dB
    N, beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    return(sg.lfilter(taps, 1.0, signal))


def fourier(sinal, fs):
    N = len(sinal)
    T = 1/fs
    if T != 0:
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(sinal)
        return(xf, yf[0:N//2])
    else:
        return 0, 0


fs = 44100
duration = 6
cutoff_hz = 3000

print("Favor digitar: 1- Ouvir 2- Arquivo ")
modo = int(input(""))

if modo == 1:
    # Ouvir audio
    audio = sd.rec(int(duration*fs), fs, channels=1)
    sd.wait()
    print("Estou ouvindo")

    y = audio[:, 0]
else:
    y, rate1 = sf.read('som1.wav')
    print("Peguei arquivo")

# Fourrier audio recebido
f, Y = fourier(y, fs)
plt.plot(f, np.abs(Y), label='audio recebido')
plt.show()

# Portadora:

fC1 = 5000
fC2 = 15000

t = np.linspace(0, len(y)/fs, len(y))

c1 = np.sin(2*math.pi*fC1*t)
c2 = np.sin(2*math.pi*fC2*t)

m1L = y*c1
f1, Y1 = fourier(m1L, fs)
plt.plot(f1, np.abs(Y1), label='audio recebido')

m2L = y*c2
f2, Y2 = fourier(m2L, fs)
plt.plot(f2, np.abs(Y2), label='audio recebido')
plt.show()

m1 = filter(m1L, cutoff_hz, fs)
m2 = filter(m2L, cutoff_hz, fs)

# Fourrier (m1F e m2F)
m1f, m1y = fourier(m1, fs)
plt.plot(m1f, np.abs(m1y), label='m1')

m2f, m2y = fourier(m2, fs)
plt.plot(m2f, np.abs(m2y), label='m2')
plt.xlim(0, cutoff_hz)
plt.show()

sf.write('m1r.wav', m1, fs)
sf.write('m2r.wav', m2*2, fs)
