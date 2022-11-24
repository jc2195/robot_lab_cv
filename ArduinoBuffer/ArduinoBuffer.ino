
#define irPickUpPin A0
bool irPickUp = false;
bool irPickUpPrev = false;

#define irDropOffPin A1
bool irDropOff = false;
bool irDropOffPrev = false;

int irThreshold = 200;

int numGears = 4;
bool eatingMode = true;

// Define pin connections & motor's steps per revolution
const int dirPin = 8;
const int stepPin = 9;
const int stepsPerRevolution = 200;

void turnMotor(int delaySpeed, int dist, int dir) {
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
}

void setup()
{
  Serial.begin(9600);
  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop()
{
  irPickUp = analogRead(irPickUpPin) < irThreshold;
  irDropOff = analogRead(irDropOffPin) < irThreshold;
  
  if (eatingMode) {
    // PickUp goes from full to empty -- new gear was picked up
    if (irPickUpPrev && !irPickUp) {
      Serial.println("EATING MODE");
      Serial.println(numGears);
      Serial.println("New gear picked up");
      numGears--;
      if (numGears == 0) {
        turnMotor(1000, 4, -1);
        eatingMode = false;
      } else {
        turnMotor(1000, 1, 1); // push forward by 1
      }  
    }
  } else {
    // in feeding mode
    if (!irDropOffPrev && irDropOff) {
      Serial.println("FEEDING MODE");
      Serial.println(numGears);
      Serial.println("New gear dropped off");
      numGears++;
      if (numGears < 4) {
        turnMotor(1000, 1, 1);
        turnMotor(1000, 1, -1); // push forward and pull back
      } else {
        Serial.println("full!");
        eatingMode = true;
      }
    }
  }

  irPickUpPrev = irPickUp;
  irDropOffPrev = irDropOff;

  delay(500);
}
