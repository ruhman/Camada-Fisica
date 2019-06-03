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
# t = 9 #tempo de duração da gravação
f_carrier = 14000.0  # Hz
fs = 44100

##########################


def generateSin(f1, t):
    fs = 44100
    n = t*fs
    time = np.linspace(0, t, n)
    signal = np.sin(f1*time*2*np.pi)
    return signal, time


def normalize(data):
    dmax = max(abs(data))
    normalized = []
    for i in range(len(data)):
        norma = data[i] / dmax
        normalized.append(norma)

    return normalized


def filtra_sinal(data, samplerate):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    N, beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = signal.lfilter(taps, 1.0, data)

    return yFiltrado


# exemplo de filtragem do sinal yAudioNormalizado
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
signalMeu = signalMeu()
data, samplerate = sf.read('elikevin.wav')
raw_data = data[:, 0]
tempo_audio = len(raw_data)/fs
t = np.linspace(0, tempo_audio, len(raw_data))

normalized_data = normalize(raw_data)

f_signal = filtra_sinal(normalized_data, samplerate)

carrier, timez = generateSin(f_carrier, tempo_audio)
modulated_signal = carrier*f_signal

# sd.play(modulated_signal, fs)
# sd.wait()
scipy.io.wavfile.write('kevinModulado.wav', fs, modulated_signal)

#audio = sd.rec(int(duration*fs),fs,channels=1)
# sd.wait()
#audiozeras = audio[:,0]
# scipy.io.wavfile.write('kevinModulado.wav',samplerate,audiozeras)


# PLOTS
plt.plot(t, raw_data)
plt.title("Raw data")
plt.show()
signalMeu.plotFFT(raw_data, fs)
plt.plot(f_signal, fs)
plt.show()

plt.plot(t, normalized_data)
plt.title("Normalized data")
plt.show()
signalMeu.plotFFT(normalized_data, fs)

plt.plot(t, f_signal)
plt.title("Filtered signal")
plt.show()
signalMeu.plotFFT(f_signal, fs)


plt.plot(t, modulated_signal)
plt.title("Modulated data")
#plt.xlim(1.0, 1.25)
plt.show()
signalMeu.plotFFT(modulated_signal, fs)
