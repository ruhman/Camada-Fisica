import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

fs = 44100
t=5

def som(list):
    f1 = list[0]
    f2 = list[1]


    om=(2 * np.pi *f1)
    om1=(2 * np.pi *f2)

    time=np.linspace(0, t, fs*t)
    a = np.sin(time*om)
    b = np.sin(time*om1)

    y=a+b

    plt.close("all")
    plt.plot(time, y)
    plt.xlim(0,0.015)
    plt.xlabel('tempo')
    plt.ylabel('Onda')
    sd.play(y, fs)
    sd.wait()
    plt.show()