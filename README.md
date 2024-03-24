# Hand_tracker_to_COM

Pour faire fonctionner le projet il vous faut plusieurs choses :

### soft :
- Python 3
- OpenCV (cv2)
- PySerial
- MediaPipe
- Arduino IDE

### matériels :
- Carte Arduino (UNO)
- Servo-moteurs
- PC de contrôle
- Webcam

#

### INSTALLATION :

1. Téléchargez le projet GitHub, cliquez sur `Code` puis `Download ZIP`.
2. Décompressez le dossier.

#### installation des lib :
1. ouvrez l'invite de commande (`cmd`) et écrivez :
   
   ```
   pip install opencv-python pyserial mediapipe
   ```
2. Si aucune erreur n'apparaît, passez au lancement. Sinon, demandez de l'aide.

#

### LANCEMENT :

1. Arduino :

   - Branchez la carte Arduino en USB au PC.
   - Lancez l'application `Arduino IDE`.
   - Dans `Outils`, `Type de carte` selectionnez `Arduino Uno`.
   - Sélectionnez ensuite le port COM de votre carte dans le menu  `port`.
   - Ouvrez le fichier `arduino_code.ino` dans `Arduino IDE`.
   - Changez les `broches` des differents moteurs.
     
        ```
         void setup() {
           Serial.begin(9600);
           monServo1.attach(10); //<--- pouce
           monServo2.attach(9);  //<--- index
           monServo3.attach(11); //<--- majeur
           monServo4.attach(12); //<--- annulaire
           monServo5.attach(8);  //<--- auriculaire
         }
        ```
   - cliquez ensuite sur `Téléverser`. Une fois le téléversement fini passez à l'étape suivante.



2. Python :

   - Ouvrez votre IDE Python et chargez le fichier `main.py`.
   - Remplacez `votre_port_série` par le port COM de votre carte.

      ```
      arduino = serial.Serial('votre_port_série', 9600)
      ```
   - Branchez votre webcam sur l'ordinateur.
     
3. Lancement :

   - Executez le code `main.py`.
   - Lorsque la vidéo est visible, ouvrez votre main face à la caméra et appuyez sur `o`.
   - Ensuite, fermez votre main face à la caméra et appuyez sur `c`.

### Une fois tout cela fait la carte arduino devrait recevoir en direct les mouvements de votre main.
###### Remarque : Votre main doit rester dans une position semblable à la position de votre main lors de l'initialisation. Si vous souhaitez changer drastiquement la position de la main, déplacez votre main puis refaites les étapes précédentes.


