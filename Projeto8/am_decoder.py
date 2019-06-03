import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy import signal
from signalTeste import *

# Configurações iniciais
cutoff_hz = 4000.0
ripple_db = 60.0  # dB
t = 9  # tempo de duração da gravação
f_carrier = 14000.0  # Hz
fs = 44100

##########################


def generateSin(f1, t):
    fs = 44100
    n = t*fs
    time = np.linspace(0, t, n)
    signal = np.sin(f1*time*2*np.pi)
    return signal, time


def filtra_sinal(data, samplerate):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    N, beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = signal.lfilter(taps, 1.0, data)

    return yFiltrado


def record():
    duration = 11
    audio = sd.rec(int(duration*fs), fs, channels=1)
    sd.wait()
    audiozeras = audio[:, 0]
    return audiozeras


data = record()
# scipy.io.wavfile.write('kevinModulado.wav', fs, data)
signalMeu = signalMeu()
data, samplerate = sf.read('kevinModulado.wav')
tempo_audio = len(data)/44100
time = np.linspace(0, tempo_audio, len(data))

carrier, timez = generateSin(f_carrier, tempo_audio)

demodulate = data * carrier

finalsignal = filtra_sinal(demodulate, fs) * 8
sd.play(finalsignal, fs)
print("Som tocou")


plt.plot(time, finalsignal)
plt.title("Demodulated data")
plt.show()

signalMeu.plotFFT(finalsignal, fs)
