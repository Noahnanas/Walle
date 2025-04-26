#include <Servo.h>

//pour chaque servo un tb {pin, angle_min, angle_max, position initial, sens, vitesse }

const int servoConfig[6][6] = {
  {2, 78, 112, 112, 1, 0},  // lid_L
  {9, 90, 90, 90, 1, 0},    // lid_R
  {3, 50, 94, 95, 1, 0.5},    // eyebrow_L
  {10, 90, 90, 90, 1, 1},   // eyebrow_R
  {4, 55, 175, 120, -1, 0},    // UD_L
  {11, 90, 90, 90, 1, 2}    // UD_R
};

Servo slid_L, slid_R, seyebrow_L, seyebrow_R, sUD_L, sUD_R;
Servo* servos[] = {&slid_L, &slid_R, &seyebrow_L, &seyebrow_R, &sUD_L, &sUD_R};
String servoNames[] = {"lid_L", "lid_R", "eyebrow_L", "eyebrow_R", "UD_L", "UD_R"};

const int microMax=2350;
const int microMin=570;

String serie = "";

void variation(int nb);
void lose(int nb);
void move(int nb,int angle);

void setup() {
  for (int i = 0; i < 6; i++) {
    servos[i]->write(servoConfig[i][3]);
    servos[i]->attach(servoConfig[i][0]);         
    //move(i,servoConfig[i][3]);           
  }
  pinMode(13,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
  if (Serial.available() > 0) {
    serie = Serial.readStringUntil('\n');
    serie.trim();
    digitalWrite(13,HIGH);

    if (serie.indexOf('=') != -1) {
      String Name = serie.substring(0, serie.indexOf('='));
      if (Name=="varier"){
        Serial.println(serie.substring(serie.indexOf('=') + 1).toInt());
        variation(serie.substring(serie.indexOf('=') + 1).toInt());
      }
      else {
        int angle = serie.substring(serie.indexOf('=') + 1).toInt();

        int servoIndex = getServoIndex(Name);
          if (servoIndex != -1) {
            Serial.println(Name+", angle :"+String(angle));
            move(servoIndex,angle);
            lose(servoIndex);
          }
      }
    }
    else if (serie.indexOf('%') != -1) {
      String servoName = serie.substring(0, serie.indexOf('%'));
      float angle = serie.substring(serie.indexOf('%') + 1).toFloat();

      int servoIndex = getServoIndex(servoName);
        if (servoIndex != -1) {
        int mappedAngle = map(angle * 100, 0, 100, servoConfig[servoIndex][1], servoConfig[servoIndex][2]);
        Serial.println(servoName+", map angle :"+String(mappedAngle));
        move(servoIndex,mappedAngle);
        }
    }
    else if (serie=="blink"){
      blink();
    }

    digitalWrite(13,LOW);
  }
}

int getServoIndex(String name) {
  for (int i = 0; i < 6; i++) {
    if (servoNames[i] == name) {
      return i;
    }
  }
}

void blink() {
  slid_L.write(servoConfig[0][1]);
  slid_R.write(servoConfig[1][1]);
  delay(100);
  slid_L.write(servoConfig[0][2]);
  slid_R.write(servoConfig[1][2]);
}

void move(int nb,int angle){
  Servo* servo = servos[nb];

  if (servoConfig[nb][5]!=0){
  int angleMicro = map(angle,0,180,microMin,microMax);
  int initialAngle = servo->readMicroseconds();
    if (angleMicro > initialAngle) {
      for (int angle = initialAngle; angle <= angleMicro; angle++) {
      servo->writeMicroseconds(angle);
      delay(servoConfig[nb][5]);
      }
    }
    else {
      for (int angle = initialAngle; angle >= angleMicro; angle--) {
      servo->writeMicroseconds(angle);
      delay(servoConfig[nb][5]);
      }
    }
  }
  else{
    servo ->write(angle);
  }
}

void variation(int nb) {
  Servo* servo = servos[nb];
  int initial = servo->read();
  move(nb,servoConfig[nb][1]);
  move(nb,servoConfig[nb][2]);
  move(nb,initial);
  lose(nb);
}

void lose(int nb) {
  Servo* servo = servos[nb];
  int angle = servo->read();
  delay(10);
  servo->write(angle+5*servoConfig[nb][4]);
  Serial.println("+ lose angle :"+String(angle+5*servoConfig[nb][4]));
  delay(10);
  servo->write(angle);
}