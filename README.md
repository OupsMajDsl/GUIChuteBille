# Interface de synchronisation de signaux audio/vidéo pour les mesures de chute de bille sur une surface liquide

Interface pour synchroniser video et audio sur le projet goutte

# Dépendances

- PyQt5
- Numpy
- Scipy
- Matplotlib
- OpenCV

# Utilisation de l'interface

Il faut modifier les variables contenant les chemins des différents fichiers: pour la vidéo, la variable`self.pathVid`,  pour le fichier de mesures`self.pathTxt`, et le fichier de configuration de la vidéo, `self.pathCih`. Les mesures des positions du point d'impact et des capteurs doivent aussi être modifiées si besoin. 
