#include <Servo.h>

#define ENA 2
#define ENB 3
#define IN1 22
#define IN2 24
#define IN3 26
#define IN4 28

struct ServoConfig {
  String name;       
  Servo servo;
  int pin;           
  int angle_min;
  int angle_min_micro;     
  int angle_max;
  int angle_max_micro;
  int initial_angle;
  int current_angle;
  int aim_angle;     
  bool dir;         
  int speed;
  bool need_update;       
  long last_update;
  long last_blink;  
};

#define nb_servos 9
#define micro_min 570
#define micro_max 2350


ServoConfig servos[nb_servos] = {
  {"lid_L", Servo(), 8, 78, 0, 112, 0, 112, 0, 0, false, 0, false, 0},
  {"lid_R", Servo(), 11, 75, 0, 107, 0, 75, 0, 0, true, 0, false, 0},
  {"eyebrow_L", Servo(), 9, 52, 0, 100, 0, 100, 0, 0, true, 500, false, 0},
  {"eyebrow_R", Servo(), 12, 85, 0, 131, 0, 85, 0, 0, false, 500, false, 0},
  {"UD_L", Servo(), 10, 55, 0, 175, 0, 125, 0, 0, true, 900, false, 0},
  {"UD_R", Servo(), 13, 50, 0, 160, 0, 125, 0, 0, false, 900, false, 0},
  {"neck_U", Servo(), 44, 60, 0, 165, 0, 90, 0, 0, false, 1500, false, 0},
  {"neck_L", Servo(), 45, 40, 0, 120, 0, 90, 0, 0, false, 1200, false, 0},
  {"neck_LR", Servo(), 46, 25, 0, 125, 0, 75, 0, 0, false, 1500, false, 0},
  {"shoulder_L", Servo(), 5, 60, 0, 120, 0, 90, 0, 0, false, 1500, false, 0},
  {"shoulder_R", Servo(), 4, 60, 0, 120, 0, 90, 0, 0, false, 1500, false, 0},
  {"hand_L", Servo(), 7, 60, 0, 120, 0, 90, 0, 0, false, 1500, false, 0},
  {"hand_R", Servo(), 6, 60, 0, 120, 0, 90, 0, 0, false, 1500, false, 0}
};

String serie = "";

void lose(int nb);
void move(int nb, float angle);

void setup() {
  for (int i = 0; i < nb_servos; i++) {
    servos[i].servo.write(servos[i].initial_angle);
    servos[i].servo.attach(servos[i].pin);
    servos[i].current_angle=servos[i].servo.readMicroseconds();
    servos[i].aim_angle=servos[i].initial_angle;
    servos[i].angle_min_micro=map(servos[i].angle_min, 0, 180, micro_min, micro_max);
    servos[i].angle_max_micro=map(servos[i].angle_max, 0, 180, micro_min, micro_max);
  }
  pinMode(13, OUTPUT);
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}


void loop() {

  if (Serial.available() > 0) {
    serie = Serial.readStringUntil('\n');
    serie.trim();
    digitalWrite(13, HIGH);

    if (serie.indexOf('%') != -1) {
      String servoName = serie.substring(0, serie.indexOf('%'));
      float angle = serie.substring(serie.indexOf('%') + 1).toFloat();
      int servoIndex = getServoIndex(servoName);
      move(servoIndex, angle);
    }
    else if (serie.indexOf('=') != -1) {
      String Name = serie.substring(0, serie.indexOf('='));
      int angle = serie.substring(serie.indexOf('=') + 1).toInt();
      int servoIndex = getServoIndex(Name);
      Serial.println("Servo :" + String(servoIndex) + ", angle :"+ String(angle));
      servos[servoIndex].servo.write(angle);

    }
    digitalWrite(13, LOW);
  }
  update();
}

int getServoIndex(String name) {
  for (int i = 0; i < nb_servos; i++) {
    if (servos[i].name == name) {
      return i;
    }
  }
}


void move(int nb, float angle) {

  if (servos[nb].dir) angle = 1.0 - angle;

  servos[nb].aim_angle = map(angle*100, 0, 100, servos[nb].angle_min_micro, servos[nb].angle_max_micro);
  servos[nb].need_update = true;

  Serial.println("Servo: " + servos[nb].name + " | Current: " + String(servos[nb].servo.readMicroseconds()) + " | Aim: " + String(servos[nb].aim_angle));

}


void update(){
  long current_time=micros();
  for (int i = 0; i < nb_servos; i++) {
    if ((servos[i].need_update) && ((current_time-servos[i].last_update)>servos[i].speed)){
      servos[i].current_angle=servos[i].servo.readMicroseconds();
      if (servos[i].current_angle < servos[i].aim_angle) {
        servos[i].servo.writeMicroseconds(servos[i].current_angle+1);
      } 
      else if (servos[i].current_angle > servos[i].aim_angle) {
        servos[i].servo.writeMicroseconds(servos[i].current_angle-1);
      } 
      else {
        servos[i].need_update = false;
      }
      servos[i].last_update=current_time;
    }
  }
}

void avancer(int vitesse = 200) {
  analogWrite(ENA, vitesse);
  analogWrite(ENB, vitesse);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void reculer(int vitesse = 200) {
  analogWrite(ENA, vitesse);
  analogWrite(ENB, vitesse);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void tournerGauche(int vitesse = 200) {
  analogWrite(ENA, vitesse);
  analogWrite(ENB, vitesse);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void tournerDroite(int vitesse = 200) {
  analogWrite(ENA, vitesse);
  analogWrite(ENB, vitesse);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

/*
void lose(int nb) {
  Servo* servo = servos[nb];
  int angle = servo->read();
  delay(10);
  // Ajuster l'angle pour simuler une "perte" de position
  servo->write(angle + 5 * (servoConfigs[nb].dir ? 1 : -1));
  Serial.println("+ lose angle :" + String(angle + 5 * (servoConfigs[nb].dir ? 1 : -1)));
  delay(10);
  servo->write(angle);
}
*/