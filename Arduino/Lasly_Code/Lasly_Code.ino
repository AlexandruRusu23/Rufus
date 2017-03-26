/*
 * Lasly is the code name for the Arduino Nano reponsible to manage the digital sensors and modules
 * but also it has to take care of two analog sensors (two MQ2)
 */

// PINS Distribution
#define   MQ2_1_PIN             A0
#define   MQ2_2_PIN             A1
#define   RED_LED_PIN           2
#define   GREEN_LED_PIN         3
#define   BLUE_LED_PIN          4
#define   YELLOW_LED_PIN        5
#define   MOTION_PIN            6
#define   ECHO_PIN              7
#define   TRIG_PIN              8
#define   RGB_LED_B_PIN         9
#define   RGB_LED_G_PIN         10
#define   RBG_LED_R_PIN         11

#define   GAS                   20
#define   MOTION                21
#define   DISTANCE              22

struct ScannerData
{
  int                 mq2_value[2];
  int                 motion_value;
  float               distance_value;
};

ScannerData           scannerData;

// timers
unsigned long         distance_scanner_timer;
unsigned long         motion_scanner_timer;
unsigned long         gas_scanner_timer;
unsigned long         controller_timer;

bool isMoving;

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
  pinMode(TRIG_PIN,         OUTPUT);
  pinMode(RED_LED_PIN,      OUTPUT);
  pinMode(GREEN_LED_PIN,    OUTPUT);
  pinMode(BLUE_LED_PIN,     OUTPUT);
  pinMode(YELLOW_LED_PIN,   OUTPUT);
  pinMode(RBG_LED_R_PIN,    OUTPUT);
  pinMode(RGB_LED_G_PIN,    OUTPUT);
  pinMode(RGB_LED_B_PIN,    OUTPUT);

  // INPUT pins
  pinMode(MOTION_PIN,       INPUT);
  pinMode(ECHO_PIN,         INPUT);
  pinMode(MQ2_1_PIN,        INPUT);
  pinMode(MQ2_2_PIN,        INPUT);

  isMoving = false;

  delay(500);
}

void loop() {

  if(millis() - controller_timer > 100)
  {
    CommandManager();
    controller_timer = millis();
  }

  if(millis() - distance_scanner_timer > 1000)
  {
  //// Distance sensor
    long duration;
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10); // Added this line
    digitalWrite(TRIG_PIN, LOW);
    duration = pulseIn(ECHO_PIN, HIGH);

    
    int auxValue = (duration/2) / 29.1;
    if (abs(auxValue - scannerData.distance_value) > 2)
    { 
      scannerData.distance_value = (duration/2) / 29.1;
      PrintScannerData(DISTANCE);
    }
    distance_scanner_timer = millis();
  }
  
  if(millis() - gas_scanner_timer > 3000)
  {
  //// Gas sensor
    int auxValue1 = analogRead(MQ2_1_PIN);
    int auxValue2 = analogRead(MQ2_2_PIN);
    if (abs(scannerData.mq2_value[0] - auxValue1) > 25 || abs(scannerData.mq2_value[0] - auxValue2) > 25)
    {  
      scannerData.mq2_value[0] = analogRead(MQ2_1_PIN);
      scannerData.mq2_value[1] = analogRead(MQ2_2_PIN);
      PrintScannerData(GAS);
    }
    gas_scanner_timer = millis();
  }
  
  if(millis() - motion_scanner_timer > 100)
  {
  //// Motion sensor
    scannerData.motion_value = digitalRead(MOTION_PIN);

    if(scannerData.motion_value == 1)
    {
      if (isMoving == false)
      {
        PrintScannerData(MOTION);
        isMoving = true;
      }
    }
    else
    {
      if (isMoving == true)
      {
        PrintScannerData(MOTION);
        isMoving = false; 
      }
    }
    
    motion_scanner_timer = millis();
  }
}

void PrintScannerData(int type)
{
  Serial.println("scanner_data");

  switch(type)
  {
    case DISTANCE:
    {
      Serial.print("distance: ");
      Serial.println(scannerData.distance_value);
      break;
    }
    case GAS:
    { 
      Serial.print("gas: ");
      Serial.println((scannerData.mq2_value[0] + scannerData.mq2_value[1]) / 2);
      break;
    }
    case MOTION:
    {
      Serial.print("motion: ");
      Serial.println(scannerData.motion_value);
      break;
    }
  }
  Serial.println("end_scanner_data");
  Serial.println("");
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

