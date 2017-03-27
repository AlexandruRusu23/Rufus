/*
 * Bryan is the code name for the Arduino Uno R3 responsible to manage the digital and analog sensors
 */

#include <DHT.h>

// PIN DISTRIBUTION
#define   MQ2_1_PIN             A0
#define   MQ2_2_PIN             A1
#define   LIGHT_1_PIN           A2
#define   LIGHT_2_PIN           A3
#define   DHT11_PIN             7
#define   MOTION_PIN            6
#define   ECHO_PIN              5
#define   TRIG_PIN              4

// CODE NAMES FOR PRINTING THE SPECIFIC DATA
#define   LIGHT                 20
#define   TEMPERATURE           21
#define   HUMIDITY              22
#define   GAS                   23
#define   MOTION                24
#define   DISTANCE              25

struct ScannerData
{
  int                   light_value[2];
  float                 humidity_value;
  float                 temperature_value;
  int                   mq2_value[2];
  int                   motion_value;
  float                 distance_value;
};

ScannerData             scannerData;

DHT dht(DHT11_PIN, DHT11);

bool isMoving;

unsigned long           light_scanner_timer;
unsigned long           temperature_scanner_timer;
unsigned long           humidity_scanner_timer;
unsigned long           distance_scanner_timer;
unsigned long           motion_scanner_timer;
unsigned long           gas_scanner_timer;

void setup() {
  delay(500);
  Serial.begin(9600);

  // OUTPUT pins
  pinMode(TRIG_PIN,             OUTPUT);

  // INPUT pins
  pinMode(LIGHT_1_PIN,          INPUT);
  pinMode(LIGHT_2_PIN,          INPUT);
  pinMode(MOTION_PIN,           INPUT);
  pinMode(ECHO_PIN,             INPUT);
  pinMode(MQ2_1_PIN,            INPUT);
  pinMode(MQ2_2_PIN,            INPUT);

  isMoving = false;

  delay(500);
}

void loop() {
  
  if (millis() - light_scanner_timer > 1000)
  {
  //// Light sensor
    int auxValue1 = analogRead(LIGHT_1_PIN);
    int auxValue2 = analogRead(LIGHT_2_PIN);
    if(abs(auxValue1 - scannerData.light_value[0]) > 50 || abs(auxValue2 - scannerData.light_value[1]) > 50)
    {
      scannerData.light_value[0] = analogRead(LIGHT_1_PIN);
      scannerData.light_value[1] = analogRead(LIGHT_2_PIN);
      PrintScannerData(LIGHT);
    }
    light_scanner_timer = millis();
  }

  if (millis() - temperature_scanner_timer > 1000)
  {
  //// Temperature sensor
    float auxValue = dht.readTemperature();
    if (abs(auxValue - scannerData.temperature_value) > 0.5)
    {
      scannerData.temperature_value = dht.readTemperature();
      PrintScannerData(TEMPERATURE);
    }
    temperature_scanner_timer = millis();
  }

  if (millis() - humidity_scanner_timer > 1000)
  {
  //// Humidity sensor
    float auxValue = dht.readHumidity();
    if (abs(auxValue - scannerData.humidity_value) > 10)
    {
      scannerData.humidity_value = dht.readHumidity();
      PrintScannerData(HUMIDITY);
    }
    humidity_scanner_timer = millis();
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
    if (abs(scannerData.mq2_value[0] - auxValue1) > 25 || abs(scannerData.mq2_value[1] - auxValue2) > 25)
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
    case LIGHT:
    {
      Serial.print("light: ");
      Serial.println((scannerData.light_value[0] + scannerData.light_value[1]) / 2);
      break;
    }
    case TEMPERATURE:
    {
      Serial.print("temperature: ");
      Serial.println(scannerData.temperature_value);
      break;
    }
    case HUMIDITY:
    {
      Serial.print("humidity: ");
      Serial.println(scannerData.humidity_value);
      break;
    }
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
