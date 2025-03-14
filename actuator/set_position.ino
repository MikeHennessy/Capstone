/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-actuator-with-feedback
 */

#define ENA_PIN   9 // the Arduino pin connected to the EN1 pin L298N
#define IN1_PIN   6 // the Arduino pin connected to the IN1 pin L298N
#define IN2_PIN   5 // the Arduino pin connected to the IN2 pin L298N
#define POTENTIOMETER_PIN   A0 // the Arduino pin connected to the potentiometer of the actuator

#define STROKE_LENGTH      102 // PLEASE UPDATE THIS VALUE (in millimeter)
#define POTENTIOMETER_MAX  987 // PLEASE UPDATE THIS VALUE
#define POTENTIOMETER_MIN  13  // PLEASE UPDATE THIS VALUE
#define TOLERANCE  5 // in millimeter

int targetPosition_mm = 50; // in millimeter

void setup() {
  Serial.begin(9600);
  // initialize digital pins as outputs.
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);

  digitalWrite(ENA_PIN, HIGH);
}

void loop() {

  int potentiometer_value = analogRead(POTENTIOMETER_PIN);
  int stroke_pos = map(potentiometer_value, POTENTIOMETER_MIN, POTENTIOMETER_MAX, 0, STROKE_LENGTH);
  Serial.print("The stroke's position = ");
  Serial.print(stroke_pos);
  Serial.println(" mm");

  if (stroke_pos < (targetPosition_mm - TOLERANCE))
    ACTUATOR_extend();
  else if (stroke_pos > (targetPosition_mm + TOLERANCE))
    ACTUATOR_retract();
  else
    ACTUATOR_stop();
}

void ACTUATOR_extend() {
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}
void ACTUATOR_retract() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
}

void ACTUATOR_stop() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}
