#define R_EN 2
#define L_EN 3
#define RPWM 4
#define LPWM 5
#define HALL_EXTEND A0
#define HALL_RETRACT A1
#define ACTUATOR_ENABLE 11

const float PULSES_PER_MM = 15.0; // Conversion factor

float targetDistanceMM = 0;
int targetPulses = 0;
int currentPulses = 0;
float currentDistanceMM = 0; // Current position in millimeters
bool moving = false;
int lastHallExtendState = LOW;
int lastHallRetractState = LOW;

void setup() {
  Serial.begin(2000000);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(HALL_EXTEND, INPUT);
  pinMode(HALL_RETRACT, INPUT);
  pinMode(ACTUATOR_ENABLE, OUTPUT);

  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);
  digitalWrite(ACTUATOR_ENABLE, HIGH);
}

void moveActuator(int direction, int speed) {
  if (direction > 0) { // Extend
    digitalWrite(R_EN, HIGH);
    digitalWrite(L_EN, HIGH);
    analogWrite(RPWM, speed);
    analogWrite(LPWM, 0);
  } else if (direction < 0) { // Retract
    digitalWrite(R_EN, HIGH);
    digitalWrite(L_EN, HIGH);
    analogWrite(RPWM, 0);
    analogWrite(LPWM, speed);
  } else { // Stop
    digitalWrite(R_EN, HIGH);
    digitalWrite(L_EN, HIGH);
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 0);
  }
}

void loop() {
  if (Serial.available() > 0) {
    targetDistanceMM = Serial.parseFloat(); // Read target distance in mm
    while (Serial.available()) Serial.read();
    targetPulses = int(abs(targetDistanceMM) * PULSES_PER_MM); // Convert mm to pulses
    currentPulses = 0;
    currentDistanceMM = 0; // Reset current position
    moving = true;
    Serial.print("Moving to target distance (mm): ");
    Serial.println(targetDistanceMM);
  }

  if (moving) {
    digitalWrite(ACTUATOR_ENABLE, HIGH);

    if (currentPulses < targetPulses) {
      if (targetDistanceMM * PULSES_PER_MM > 0) {
        moveActuator(1, 255); // Lower speed
      } else {
        moveActuator(-1, 255); // Lower speed
      }
    } else {
      moveActuator(0, 0);
      delay(500); // Add a 500ms delay before stopping.
      digitalWrite(ACTUATOR_ENABLE, LOW);
      moving = false;
      Serial.println("Target reached");
    }
  }

  int hallExtend = digitalRead(HALL_EXTEND);
  int hallRetract = digitalRead(HALL_RETRACT);

  //Serial.print("Hall Extend: "); Serial.print(hallExtend);
  //Serial.print(" | Hall Retract: "); Serial.println(hallRetract);

  if (hallExtend == HIGH && lastHallExtendState == LOW && targetPulses > 0) {
    currentPulses++;
    currentDistanceMM = currentPulses / PULSES_PER_MM; // Update current position
    Serial.print("Pulse Count: "); Serial.println(currentPulses);
    Serial.print("Current Distance (mm): "); Serial.println(currentDistanceMM);
  }
  lastHallExtendState = hallExtend;

  if (hallRetract == HIGH && lastHallRetractState == LOW && targetPulses < 0) {
    currentPulses--;
    currentDistanceMM = currentPulses / PULSES_PER_MM; // Update current position
    Serial.print("Pulse Count: "); Serial.println(currentPulses);
    Serial.print("Current Distance (mm): "); Serial.println(currentDistanceMM);
  }
  lastHallRetractState = hallRetract;

  delay(10);
}