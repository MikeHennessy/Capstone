#define R_EN_ACT1 2
#define L_EN_ACT1 3
#define RPWM_ACT1 4
#define LPWM_ACT1 5
#define ACTUATOR_ENABLE_ACT1 11

#define R_EN_ACT2 7
#define L_EN_ACT2 6
#define RPWM_ACT2 8
#define LPWM_ACT2 9
#define ACTUATOR_ENABLE_ACT2 10

const float SPEED_INCHES_PER_SEC = 0.51;
const float MM_PER_INCH = 25.4;

void setup() {
  Serial.begin(9600);
  pinMode(R_EN_ACT1, OUTPUT);
  pinMode(L_EN_ACT1, OUTPUT);
  pinMode(RPWM_ACT1, OUTPUT);
  pinMode(LPWM_ACT1, OUTPUT);
  pinMode(ACTUATOR_ENABLE_ACT1, OUTPUT);

  pinMode(R_EN_ACT2, OUTPUT);
  pinMode(L_EN_ACT2, OUTPUT);
  pinMode(RPWM_ACT2, OUTPUT);
  pinMode(LPWM_ACT2, OUTPUT);
  pinMode(ACTUATOR_ENABLE_ACT2, OUTPUT);

  digitalWrite(R_EN_ACT1, HIGH);
  digitalWrite(L_EN_ACT1, HIGH);
  digitalWrite(ACTUATOR_ENABLE_ACT1, HIGH);

  digitalWrite(R_EN_ACT2, HIGH);
  digitalWrite(L_EN_ACT2, HIGH);
  digitalWrite(ACTUATOR_ENABLE_ACT2, HIGH);
}

void moveActuator(int actuatorNum, int direction, unsigned long duration) {
  if (actuatorNum == 1) {
    if (direction > 0) {
      analogWrite(RPWM_ACT1, 255);
      analogWrite(LPWM_ACT1, 0);
    } else if (direction < 0) {
      analogWrite(RPWM_ACT1, 0);
      analogWrite(LPWM_ACT1, 255);
    } else {
      analogWrite(RPWM_ACT1, 0);
      analogWrite(LPWM_ACT1, 0);
    }
  } else if (actuatorNum == 2) {
    if (direction > 0) {
      analogWrite(RPWM_ACT2, 255);
      analogWrite(LPWM_ACT2, 0);
    } else if (direction < 0) {
      analogWrite(RPWM_ACT2, 0);
      analogWrite(LPWM_ACT2, 255);
    } else {
      analogWrite(RPWM_ACT2, 0);
      analogWrite(LPWM_ACT2, 0);
    }
  }
  delay(duration); // Move for the specified duration
  if (actuatorNum == 1) {
    analogWrite(RPWM_ACT1, 0);
    analogWrite(LPWM_ACT1, 0);
  } else if (actuatorNum == 2) {
    analogWrite(RPWM_ACT2, 0);
    analogWrite(LPWM_ACT2, 0);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    int actuatorNum = inputString.substring(inputString.indexOf('[') + 1, inputString.indexOf(',')).toInt();
    float targetDistanceMM = inputString.substring(inputString.indexOf(',') + 1, inputString.indexOf(']')).toFloat();

    unsigned long targetTimeMS = abs(int(targetDistanceMM / MM_PER_INCH / SPEED_INCHES_PER_SEC * 1000));

    Serial.print("Moving Actuator ");
    Serial.print(actuatorNum);
    Serial.print(" for (ms): ");
    Serial.println(targetTimeMS);

    digitalWrite(actuatorNum == 1 ? ACTUATOR_ENABLE_ACT1 : ACTUATOR_ENABLE_ACT2, HIGH);

    moveActuator(actuatorNum, targetDistanceMM > 0 ? 1 : -1, targetTimeMS);

    delay(500);
    digitalWrite(actuatorNum == 1 ? ACTUATOR_ENABLE_ACT1 : ACTUATOR_ENABLE_ACT2, LOW);
    Serial.println("Target reached");
  }
  delay(10);
}