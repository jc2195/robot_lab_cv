
#define irPickUpPin1  A4
#define irDropOffPin1 A3

#define irPickUpPin2  A5
#define irDropOffPin2 A10

#define irPickUpPin3  A14
#define irDropOffPin3 A13

#define irPickUpPin4  A12
#define irDropOffPin4 A11

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

byte stepPins[] = {stepPin1, stepPin2, stepPin3, stepPin4};
byte dirPins[] = {dirPin1, dirPin2, dirPin3, dirPin4};
byte enPins[] = {enPin1, enPin2, enPin3, enPin4};

byte irPickUpPins[] = {irPickUpPin1, irPickUpPin2, irPickUpPin3, irPickUpPin4};
byte irDropOffPins[] = {irDropOffPin1, irDropOffPin2, irDropOffPin3, irDropOffPin4};

int irPickUpThreshold[] = {0, 0, 0, 0};
int irDropOffThreshold[] = {0, 0, 0, 0};

bool irPickUpPrev[] = {true, true, true, true};
bool irPickUp[] = {true, true, true, true};
bool irDropOffPrev[] = {true, true, true, true};
bool irDropOff[] = {true, true, true, true};

int stepsPerRevolution = 200;
int motorDist[] = {199, 199, 60, 36};
int motorOffsetDist[] = {15, 15, 60, 167};

void turnMotor(int stepPin, int dirPin, int enPin,
               int delaySpeed, int dist, int dir) {
  digitalWrite(enPin, LOW);
  if (dir == 1) {
    digitalWrite(dirPin, HIGH);
  }
  if (dir == -1) {
    digitalWrite(dirPin, LOW);
  }
  for(int d = 0; d < dist; d++)
  {
    for(int x = 0; x < stepsPerRevolution; x++)
    {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(delaySpeed);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(delaySpeed);
    }
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

    digitalWrite(enPins[i], HIGH);
  }

  for(int i = 0; i < 4; i++) {
    for(int j = 0; j < 10; j++) {
      irPickUpThreshold[i] += analogRead(irPickUpPins[i]);
    }
    irPickUpThreshold[i] /= 10;
    irPickUpThreshold[i] += 1;
    if (irPickUpThreshold[i] < 100) {
      irPickUpThreshold[i] = 85; 
    }
    else {
      irPickUpThreshold[i] *= 1.15;
    }

    irDropOffThreshold[i] = irPickUpThreshold[i];
      
    Serial.print("irThresholds: ");
    Serial.print(i);
    Serial.print(",");
    Serial.print(irPickUpThreshold[i]);
    Serial.print(",");
    Serial.println(irDropOffThreshold[i]);
  }

  delay(500);

  for(int i = 0; i < 4; i++) {
    irPickUp[i] = analogRead(irPickUpPins[i]) < irPickUpThreshold[i];
    irDropOff[i] = analogRead(irDropOffPins[i]) < irDropOffThreshold[i];
  }
}


void loop()
{
  Serial.print(analogRead(irPickUpPins[0]));
  Serial.print(",");
  Serial.print(analogRead(irPickUpPins[1]));
  Serial.print(",");
  Serial.print(analogRead(irPickUpPins[2]));
  Serial.print(",");
  Serial.println(analogRead(irPickUpPins[3]));
  for(int i = 0; i < 4; i++) {
    irPickUp[i] = analogRead(irPickUpPins[i]) < irPickUpThreshold[i];
    irDropOff[i] = analogRead(irDropOffPins[i]) < irDropOffThreshold[i];

    // PickUp goes from full to empty -- new gear was picked up
    if (irPickUpPrev[i] && !irPickUp[i]) {
      numParts[i]--;
      Serial.print("Buffer is ");
      Serial.print(i);
      Serial.print(" with ");
      Serial.println(numParts[i]);
      Serial.println("New gear picked up");
      
      if (numParts[i] <= 0) {
        Serial.println("NO MORE PARTS IN BUFFER");
      } else if (numParts[i] > 4) {
        Serial.println("TOO MANY PARTS IN BUFFER, ASSUMING ERROR");
      } else {
        delay(2500);
        turnMotor(stepPins[i], dirPins[i], enPins[i], 100, motorOffsetDist[i] + (4-numParts[i])*motorDist[i], 1);
        turnMotor(stepPins[i], dirPins[i], enPins[i], 50,  motorOffsetDist[i] + (4-numParts[i])*motorDist[i], -1);
      }  
    }

    if (!irDropOffPrev[i] && irDropOff[i]) {
      numParts[i]++;
      Serial.print("Buffer is ");
      Serial.print(i);
      Serial.print(" with ");
      Serial.println(numParts[i]);
      Serial.println("New gear dropped off");
      
      // ADD MASSIVE DELAY FOR INTEGRATION TESTING
      if (numParts[i] <= 0) {
        Serial.println("ZERO/NEGATIVE PARTS IN BUFFER AFTER REPLENISHMENT, ASSUMING ERROR"); 
      } else if (numParts[i] <= 4) {
        delay(2500);
        turnMotor(stepPins[i], dirPins[i], enPins[i], 100, motorOffsetDist[i] + (4-numParts[i])*motorDist[i], 1);
        turnMotor(stepPins[i], dirPins[i], enPins[i], 50,  motorOffsetDist[i] + (4-numParts[i])*motorDist[i], -1);
      } /*else if (numParts[i] == 4) {
        if(i >= 2) { // more shove for gears
          turnMotor(stepPins[i], dirPins[i], enPins[i], 100, motorOffsetDist[i]-2, 1);
        } else {
          turnMotor(stepPins[i], dirPins[i], enPins[i], 100, motorOffsetDist[i]-10, 1);
        }
        Serial.println("full!");
      } */else {
        Serial.println("TOO MANY PARTS IN BUFFER, ASSUMING ERROR");
      }
    }
  
    irPickUpPrev[i] = irPickUp[i];
    irDropOffPrev[i] = irDropOff[i];
  }

  delay(500);
}
