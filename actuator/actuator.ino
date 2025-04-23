#include <Wire.h>

// Pin definitions for actuators
#define R_EN_ACT1 7
#define L_EN_ACT1 6
#define RPWM_ACT1 8
#define LPWM_ACT1 9
#define ACTUATOR_ENABLE_ACT1 10
#define R_EN_ACT2 2
#define L_EN_ACT2 3
#define RPWM_ACT2 4
#define LPWM_ACT2 5
#define ACTUATOR_ENABLE_ACT2 11

// Constants
const float SPEED_INCHES_PER_SEC = 0.51;
const float MM_PER_INCH = 25.4;

// Global variables for actuator state
int currentActuator = 0;       // 0: none, 1: actuator 1, 2: actuator 2
int currentDirection = 0;    // 0: stopped, 1: forward, -1: backward
unsigned long moveStartTime = 0; // Time when movement started
unsigned long moveDuration = 0;  // Duration of current movement
bool isMoving = false;

void setup() {
  Wire.begin(8); // Join I2C bus as slave with address 8
  Serial.begin(9600); // For debugging

  // pinMode declarations
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

  // Initial state of actuators
  digitalWrite(R_EN_ACT1, HIGH);
  digitalWrite(L_EN_ACT1, HIGH);
  digitalWrite(ACTUATOR_ENABLE_ACT1, HIGH); // Enable Actuator 1
  digitalWrite(R_EN_ACT2, HIGH);
  digitalWrite(L_EN_ACT2, HIGH);
  digitalWrite(ACTUATOR_ENABLE_ACT2, HIGH); // Enable Actuator 2
  Serial.println("Arduino ready.");
}

void loop() {
  Wire.onReceive(receiveEvent); // Register event handler
  manageActuators();           // Handle actuator movement
}

void moveActuator(int actuatorNum, int direction, unsigned long duration) {
  // Only start movement if not already moving
  if (!isMoving) {
    isMoving = true;
    currentActuator = actuatorNum;
    currentDirection = direction;
    moveStartTime = millis();
    moveDuration = duration;

    Serial.print("moveActuator: Actuator = ");
    Serial.print(actuatorNum);
    Serial.print(", Direction = ");
    Serial.print(direction);
    Serial.print(", Duration = ");
    Serial.println(duration);

    if (actuatorNum == 1) {
      if (direction > 0) {
        analogWrite(RPWM_ACT1, 255);
        analogWrite(LPWM_ACT1, 0);
      } else {
        analogWrite(RPWM_ACT1, 0);
        analogWrite(LPWM_ACT1, 255);
      }
    } else if (actuatorNum == 2) {
      if (direction > 0) {
        analogWrite(RPWM_ACT2, 255);
        analogWrite(LPWM_ACT2, 0);
      } else {
        analogWrite(RPWM_ACT2, 0);
        analogWrite(LPWM_ACT2, 255);
      }
    }
  } else {
    Serial.println("moveActuator: Already moving");
  }
}

void manageActuators() {
  if (isMoving) {
    if (millis() - moveStartTime >= moveDuration) {
      // Stop the actuator
      if (currentActuator == 1) {
        analogWrite(RPWM_ACT1, 0);
        analogWrite(LPWM_ACT1, 0);
        digitalWrite(R_EN_ACT1, HIGH); // Stop Actuator 1
        digitalWrite(L_EN_ACT1, HIGH);
      } else if (currentActuator == 2) {
        analogWrite(RPWM_ACT2, 0);
        analogWrite(LPWM_ACT2, 0);
        digitalWrite(R_EN_ACT2, HIGH); // Stop Actuator 2
        digitalWrite(L_EN_ACT2, HIGH);
      }
      isMoving = false;
      currentActuator = 0;
      currentDirection = 0;
      Serial.println("Target reached");
      Wire.write("OK"); // Respond to the Raspberry Pi
    }
  }
}

void receiveEvent(int howMany) {
  Serial.print("receiveEvent called.  Received ");
  Serial.print(howMany);
  Serial.println(" bytes.");

  if (howMany == 9) { // Expecting  9 bytes
    byte data[9];
    // Read the  9 bytes
    for (int i = 0; i < 9; i++) {
      data[i] = Wire.read();
      Serial.print("data[");
      Serial.print(i);
      Serial.print("] = ");
      Serial.print(data[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    // Extract data from the received bytes (Big Endian)
    int actuatorNum = data[4];
    union {
      float f;
      byte b[4];
    } u;
    u.b[3] = data[5];
    u.b[2] = data[6];
    u.b[1] = data[7];
    u.b[0] = data[8];
    float targetDistanceMM = u.f;

    Serial.print("Received: Actuator = ");
    Serial.print(actuatorNum);
    Serial.print(", MM = ");
    Serial.println(targetDistanceMM, 4);

    // Calculate the duration
    unsigned long targetTimeMS = abs(long(targetDistanceMM / MM_PER_INCH / SPEED_INCHES_PER_SEC * 1000));

    // Move the actuator
    moveActuator(actuatorNum, targetDistanceMM > 0 ? 1 : -1, targetTimeMS);
  } else {
    Serial.print("Received ");
    Serial.print(howMany);
    Serial.println(" bytes. Expected 9.");
    while (Wire.available()) {
      Wire.read();
    }
  }
}