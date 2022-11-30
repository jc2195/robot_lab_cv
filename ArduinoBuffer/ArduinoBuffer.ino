
#define irPickUpPin1  A3
#define irDropOffPin1 A4

#define irPickUpPin2  A5
#define irDropOffPin2 A10

#define irPickUpPin3  A11
#define irDropOffPin3 A12

#define irPickUpPin4  A13
#define irDropOffPin4 A14

// Define pin connections & motor's steps per revolution
#define stepPin1  54
#define dirPin1   55
#define enPin1    38

#define stepPin2  60
#define dirPin2   61
#define enPin2    56

#define stepPin3  46
#define dirPin3   48
#define enPin3    62

#define stepPin4  26
#define dirPin4   28
#define enPin4    24

int numParts[] = {4, 4, 4, 4};
bool eatingMode[] = {true, true, true, true};

byte stepPins[] = {stepPin1, stepPin2, stepPin3, stepPin4};
byte dirPins[] = {dirPin1, dirPin2, dirPin3, dirPin4};
byte enPins[] = {enPin1, enPin2, enPin3, enPin4};

byte irPickUpPins[] = {irPickUpPin1, irPickUpPin2, irPickUpPin3, irPickUpPin4};
byte irDropOffPins[] = {irDropOffPin1, irDropOffPin2, irDropOffPin3, irDropOffPin4};

int irPickUpThreshold[] = {0, 0, 0, 0};
int irDropOffThreshold[] = {0, 0, 0, 0};

bool irPickUpPrev[] = {false, false, false, false};
bool irPickUp[] = {false, false, false, false};
bool irDropOffPrev[] = {false, false, false, false};
bool irDropOff[] = {false, false, false, false};

int stepsPerRevolution = 200;

void turnMotor(int stepPin, int dirPin, int enPin,
               int delaySpeed, int dist, int dir) {
  digitalWrite(enPin, LOW);
  if (dir == 1) {
    digitalWrite(dirPin, HIGH);
  }
  if (dir == -1) {
    digitalWrite(dirPin, LOW);
  }
  for(int x = 0; x < stepsPerRevolution*dist; x++)
  {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(delaySpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(delaySpeed);
  }
  digitalWrite(enPin, HIGH);
}

void setup()
{
  Serial.begin(9600);
  // Declare pins as Outputs
  for(int i = 0; i < 4; i++) {
    pinMode(stepPins[i], OUTPUT);
    pinMode(dirPins[i], OUTPUT);
    pinMode(enPins[i], OUTPUT);
  }

  for(int i = 0; i < 4; i++) {
    for(int j = 0; j < 100; j++) {
      irPickUpThreshold[i] += analogRead(irPickUpPins[i]);
      irDropOffThreshold[i] += analogRead(irDropOffPins[i]);
    }
    irPickUpThreshold[i] /= 100*2;
    irDropOffThreshold[i] /= 100*2;
      
    Serial.print("irThresholds: ");
    Serial.print(i);
    Serial.print(",");
    Serial.println(irPickUpThreshold[i]);
  }
}

void loop()
{
  for(int i = 0; i < 4; i++) {
    irPickUp[i] = analogRead(irPickUpPins[i]) < irPickUpThreshold[i];
    irDropOff[i] = analogRead(irDropOffPins[i]) < irDropOffThreshold[i];
    
    if (eatingMode[i]) {
      // PickUp goes from full to empty -- new gear was picked up
      if (irPickUpPrev[i] && !irPickUp[i]) {
        Serial.println(i);
        Serial.println("EATING MODE");
        Serial.println(numParts[i]);
        Serial.println("New gear picked up");
        numParts[i]--;
        if (numParts[i] == 0) {
          turnMotor(stepPins[i], dirPins[i], enPins[i], 1000, 4, -1);
          eatingMode[i] = false;
        } else {
          turnMotor(stepPins[i], dirPins[i], enPins[i], 1000, 1, 1); // push forward by 1
        }  
      }
    } else {
      // in feeding mode
      if (!irDropOffPrev[i] && irDropOff[i]) {
        Serial.println(i);
        Serial.println("FEEDING MODE");
        Serial.println(numParts[i]);
        Serial.println("New gear dropped off");
        numParts[i]++;
        if (numParts[i] < 4) {
          turnMotor(stepPins[i], dirPins[i], enPins[i], 1000, 1, 1);
          turnMotor(stepPins[i], dirPins[i], enPins[i], 1000, 1, -1); // push forward and pull back
        } else {
          Serial.println("full!");
          eatingMode[i] = true;
        }
      }
    }
  
    irPickUpPrev[i] = irPickUp[i];
    irDropOffPrev[i] = irDropOff[i];
  }

  delay(500);
}
