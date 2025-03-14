/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-actuator-with-feedback
 */

// the code for getting the feedback when the actuator fully extended and retracted

#define ENA_PIN   9 // the Arduino pin connected to the EN1 pin L298N
#define IN1_PIN   6 // the Arduino pin connected to the IN1 pin L298N
#define IN2_PIN   5 // the Arduino pin connected to the IN2 pin L298N
#define POTENTIOMETER_PIN   A0 // the Arduino pin connected to the potentiometer of the actuator

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
  delay(20000); // wait for actuator fully extends. It will stop extending automatically when reaching the limit
  // read the analog in value:
  int POTENTIOMETER_MAX = analogRead(POTENTIOMETER_PIN);
  Serial.print("POTENTIOMETER_MAX = ");
  Serial.println(POTENTIOMETER_MAX);

  // retracts the actuator
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  delay(20000); // wait for actuator fully extends. It will stop retracting automatically when reaching the limit
  int POTENTIOMETER_MIN = analogRead(POTENTIOMETER_PIN);
  Serial.print("POTENTIOMETER_MIN = ");
  Serial.println(POTENTIOMETER_MIN);
}
