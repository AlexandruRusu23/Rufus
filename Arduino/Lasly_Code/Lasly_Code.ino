/*
 * Lasly is the code name for the Arduino Nano reponsible to manage the digital sensors and modules
 * and got the role of Animator
 */

// PINS DISTRIBUTION
#define   BLUE_LED_PIN          2
#define   RED_LED_PIN           3
#define   YELLOW_LED_PIN        4
#define   GREEN_LED_PIN         5
#define   RGB_LED_B_PIN         9
#define   RGB_LED_G_PIN         10
#define   RBG_LED_R_PIN         11

// timers
unsigned long         controller_timer;

// Command Controller vars
unsigned long         serialData;
int                   inByte;
int                   digitalState;
int                   pinNumber;
int                   analogRate;
int                   sensorVal;

void setup() {
  // wait for Arduino to warm up
  delay(500);
  Serial.begin(9600);
  
  // OUTPUT pins
  pinMode(RED_LED_PIN,      OUTPUT);
  pinMode(GREEN_LED_PIN,    OUTPUT);
  pinMode(BLUE_LED_PIN,     OUTPUT);
  pinMode(YELLOW_LED_PIN,   OUTPUT);
  pinMode(RBG_LED_R_PIN,    OUTPUT);
  pinMode(RGB_LED_G_PIN,    OUTPUT);
  pinMode(RGB_LED_B_PIN,    OUTPUT);

  delay(500);
}

void loop() {

  if(millis() - controller_timer > 50)
  {
    CommandManager();
    controller_timer = millis();
  }
}

long getSerial()
{
  serialData = 0;
  if (Serial.available() > 0) {
    while(inByte != '/')
    {
      inByte = Serial.read();
      if(inByte > 0 && inByte != '/')
      {
        serialData = serialData * 10 + inByte - '0';
      }
    }
  
    inByte = 0;
  }
  return serialData;
}

void CommandManager()
{
  getSerial();
  switch(serialData)
  {
    case 1:
    {
      // Analog / Digital write
      getSerial();
      switch(serialData)
      {
        case 1:
        {
          AnalogWrite();
          break;
        }
        case 2:
        {
          DigitalWrite();
          break;
        }
      }
      break;
    }
    case 2:
    {
      // Analog / Digital read
      getSerial();
      switch (serialData)
      {
      case 1:
        {
          AnalogRead();
          break;
        } 
      case 2:
        {
          DigitalRead();
          break;
        }
      }
      break;
    }
  }
}

void AnalogRead()
{
  getSerial();
  pinNumber = serialData;
  pinMode(pinNumber, INPUT);
  sensorVal = analogRead(pinNumber);
  Serial.println("analog_read");
  Serial.println(sensorVal);
  Serial.println("end_analog_read");
  sensorVal = 0;
  pinNumber = 0;
}

void AnalogWrite()
{
  getSerial();
  pinNumber = serialData;
  getSerial();
  analogRate = serialData;
  pinMode(pinNumber, OUTPUT);
  analogWrite(pinNumber, analogRate);
  pinNumber = 0;
}

void DigitalRead()
{
  getSerial();
  pinNumber = serialData;
  pinMode(pinNumber, INPUT);
  sensorVal = digitalRead(pinNumber);
  Serial.println("digital_read");
  Serial.println(sensorVal);
  Serial.println("end_digital_read");
  sensorVal = 0;
  pinNumber = 0;
}

void DigitalWrite()
{      
  getSerial();
  pinNumber = serialData;
  getSerial();
  digitalState = serialData;
  pinMode(pinNumber, OUTPUT);
  if (digitalState == 0)
  {
    digitalWrite(pinNumber, LOW);
  }
  if (digitalState >= 1)
  {
    digitalWrite(pinNumber, HIGH);
  }
  pinNumber = 0;
}

