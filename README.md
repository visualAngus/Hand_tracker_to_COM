# Hand_tracker_to_COM

Pour faire fonctionner le projet il vous faut plusieurs choses :

### soft :
- python3
- cv2
- serial
- mediapipe
- arduino IDE

### matériels :
- carte arduino (UNO)
- servo moteurs
- PC de control
- webcam

#

### INSTALLATION :

1. Téléchargez le projet github, cliquez sur `code` puis `download zip`.
2. Décompressez le dossier.

#### installation des lib :
1. ouvrez la `cmd` puis écrivez :
   
   ```
   pip install opencv-python pyserial mediapipe
   ```
2. Si il n'y a aucune erreur passez au lancement sinon, demandez de l'aide.

#

### LANCEMENT :

1. Arduino :

   - Branchez la carte `arduino` en usb au PC.
   
   - Lancez l'application `Arduino IDE` puis dans `utils`, `type de carte` selectionnez `Arduino Uno`.
   - Selcetion ensuite de le menu `port` le port `COM` de votre carte.
   
   - Ouvrez le fichier `arduino_code.ino` dans `Arduino IDE`.
   - Changez les `pins` des differents moteurs.
     
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
   - cliquez ensuite sur `Téléverser`, une fois le téléversement fini passez à l'étape suivante.



2. Python :

   - Ouvrez votre IDE `python` puis chargez le fichier `main.py` changez `votre_port_COM` avec votre port `COM`.

      ```
      arduino = serial.Serial('votre_port_COM', 9600)
      ```
   - Branchez votre `webcam` sur l'ordinateur.
     
3. Lancement :

   - Executez le code `main.py`.
  
   - Lorsque la vidéo sera visible, ouvrez votre main fasse à la caméra puis appuiez sur `o`.
   - Ensuite fremez votre main fasse à la caméra puis appuiez sur `c`.
  
   - 
### Une fois tout cela fait la carte arduino devrait recevoir en direct les mouvements de votre main.
###### ps : votre main doit rester dans une position semblable à la posiotn de votre main lors de l'initialisation si vous souhaite changer drastiquement la position de la main, déplacez votre main puis refaites les étapes précédents. 


