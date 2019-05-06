import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


signal = np.loadtxt('/home/mathieu/Documents/S4/ProjetBille/MesureCoupe/denoised_cut_mes_cam_bille1_1.txt')
signal = signal[:,2]

sr = 500000
S = np.abs(librosa.stft(signal))

plt.figure()
librosa.display.specshow(librosa.amplitude_to_db(S,ref=np.max),y_axis='log', x_axis='time',sr = sr)
plt.title('Entrée spectrogramme')
plt.colorbar(format='%+2.0f dB')
plt.show()