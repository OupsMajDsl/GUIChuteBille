import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


signal = np.loadtxt('/media/mathieu/Nouveau nom/denoised_mesures_acous/denoised_mes_sh_b3_1.txt')
signal = signal[:,2]

sr = 500000
S = np.abs(librosa.stft(signal))

fig, ax = plt.subplots()
librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time',sr = sr)
ax.set_title('Entrée spectrogramme')
plt.show()