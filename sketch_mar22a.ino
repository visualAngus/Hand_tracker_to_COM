#include <Servo.h>

Servo monServo1;
Servo monServo2;
Servo monServo3;

void setup() {
  Serial.begin(9600);
  monServo1.attach(10);
  monServo2.attach(9);
  monServo3.attach(11);
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
      value = int(data);
      switch (value) {
        case '0':
          value = 0;
          break;
        case '1':
          value = 1;
          break;
        case '2':
          value = 2;
          break;
        case '3':
          value = 3;
          break;
        case '4':
          value = 4;
          break;
        case '5':
          value = 5;
          break;
        case '6':
          value = 6;
          break;
        case '7':
          value = 7;
          break;
        case '8':
          value = 8;
          break;
        case '9':
          value = 9;
          break;
        default:
          value = -1;
          break;
        }
        
        //Serial.println(value);   Print the converted value
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
      monServo1.write(angle_servo[1]);
      monServo2.write(angle_servo[2]);
      monServo3.write(angle_servo[3]);
    }
  }
}
