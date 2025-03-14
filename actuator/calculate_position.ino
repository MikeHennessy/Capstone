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
#define POTENTIOMETER_MAX  987   // PLEASE UPDATE THIS VALUE
#define POTENTIOMETER_MIN  13    // PLEASE UPDATE THIS VALUE

void setup() {
  Serial.begin(9600);
  // initialize digital pins as outputs.
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);

  digitalWrite(ENA_PIN, HIGH);
}

void loop() {
  // extend the actuator
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);

  int potentiometer_value = analogRead(POTENTIOMETER_PIN);
  int stroke_pos = map(potentiometer_value, POTENTIOMETER_MIN, POTENTIOMETER_MAX, 0, STROKE_LENGTH);
  Serial.print("The stroke's position = ");
  Serial.print(stroke_pos);
  Serial.println(" mm");
}
