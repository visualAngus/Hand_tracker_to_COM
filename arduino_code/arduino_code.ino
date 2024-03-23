#include <Servo.h>

Servo monServo1;
Servo monServo2;
Servo monServo3;
Servo monServo4;
Servo monServo5;

void setup() {
   Serial.begin(9600);
   monServo1.attach(10); //<--- pouce
   monServo2.attach(9);  //<--- index
   monServo3.attach(11); //<--- majeur
   monServo4.attach(12); //<--- annulaire
   monServo5.attach(8);  //<--- auriculaire
 }

int servoAngle = 0;
int count = 100;
bool isCalibrating = false;
int value = -1;
int angle_servo[5];
bool servo_count = false;
int global_count = 0;
bool listen_yes = false;

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();

    if (data == '*') {
      isCalibrating = !isCalibrating;
      count = 100;
    }
    if (data == '$'){
      servo_count = !servo_count;
      count = 100;
      angle_servo[global_count] = servoAngle;
      global_count = global_count+1;
      servoAngle = 0;
    }
    if (isCalibrating) {
      const int offset = data - '0';
      if (0 <= offset && offset <= 9) {
        value = offset;
      } else {
        value = -1;
      }
      
      if (value != -1){
        servoAngle = servoAngle+value*count;
        count = count/10;
      }
    }
      

    if (!isCalibrating and global_count>=4) {
      global_count = 0;
      for (int angle:angle_servo ) {
        Serial.println(angle);
      }
      //Serial.println(servoAngle);
      monServo1.write(angle_servo[0]);
      monServo2.write(angle_servo[1]);
      monServo3.write(angle_servo[2]);
      monServo3.write(angle_servo[3]);
      monServo3.write(angle_servo[4]);
    }
  }
}
