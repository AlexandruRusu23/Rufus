#define LIGHT_1_PIN A2
#define LIGHT_2_PIN A3
#define TEMPERATURE_PIN A4
#define HUMIDITY_PIN A5
#define MQ2_1_PIN A0
#define MQ2_2_PIN A1
#define TRIG_PIN 8
#define ECHO_PIN 7
#define RED_LED_PIN 2
#define GREEN_LED_PIN 3
#define BLUE_LED_PIN 4
#define YELLOW_LED_PIN 5
#define MOTION_PIN 6
#define RBG_LED_R_PIN 11
#define RGB_LED_G_PIN 10
#define RGB_LED_B_PIN 9

struct ScannerData
{
  int light_value[2];
  int mq2_value[2];
  float humidity_value;
  int motion_value;
  float temperature_value;
  float distance_value;
};

ScannerData scannerData;

float humi;
float prehum;
float humconst;
float truehum;
float pretruehum; 
long pretruehumconst; 
long valb;

unsigned long scanner_timer;
unsigned long controller_timer;

// Command Controller vars
unsigned long serialData;
int inByte;
int digitalState;
int pinNumber;
int analogRate;
int sensorVal;

void setup() {
  delay(100);
  Serial.begin(9600);
  
  // OUTPUT pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  //pinMode(BUZZER_1_PIN, OUTPUT);
  //pinMode(BUZZER_2_PIN, OUTPUT);
  pinMode(RBG_LED_R_PIN, OUTPUT);
  pinMode(RGB_LED_G_PIN, OUTPUT);
  pinMode(RGB_LED_B_PIN, OUTPUT);

  // INPUT pins
  pinMode(MOTION_PIN, INPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LIGHT_1_PIN, INPUT);
  pinMode(LIGHT_2_PIN, INPUT);
  pinMode(TEMPERATURE_PIN, INPUT);
  pinMode(HUMIDITY_PIN, INPUT);
  pinMode(MQ2_1_PIN, INPUT);
  pinMode(MQ2_2_PIN, INPUT);

  delay(1000);
}

void loop() {

  if(millis() - controller_timer > 100)
  {
    CommandManager();
    controller_timer = millis();
  }

  if(millis() - scanner_timer > 1000)
  {
  //// Light sensor
    scannerData.light_value[0] = analogRead(LIGHT_1_PIN);
    scannerData.light_value[1] = analogRead(LIGHT_2_PIN);
  
  //// Temperature sensor
    scannerData.temperature_value = ReadTemperature(10, TEMPERATURE_PIN);
  
  //// Humidity sensor
    valb = analogRead(HUMIDITY_PIN); // humidity calculation
    prehum = (valb/5);
    humconst = (0.16/0.0062);
    humi = prehum - humconst;
    pretruehumconst = 0.00216*scannerData.temperature_value;
    pretruehum = 1.0546-pretruehumconst;
    scannerData.humidity_value = humi/pretruehum;
  
  //// Distance sensor
    long duration;
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10); // Added this line
    digitalWrite(TRIG_PIN, LOW);
    duration = pulseIn(ECHO_PIN, HIGH);
    scannerData.distance_value = (duration/2) / 29.1;
    
  //// Gas sensor
    scannerData.mq2_value[0] = analogRead(MQ2_1_PIN);
    scannerData.mq2_value[1] = analogRead(MQ2_2_PIN);
  
  //// Motion sensor
    scannerData.motion_value = digitalRead(MOTION_PIN);
  
    PrintScannerData();

    scanner_timer = millis();
  }
}

float ReadTemperature(int count, int pin)
{
  float temperaturaMediata = 0;
  float sumaTemperatura = 0;
  for (int i = 0; i < count; i++) {
    int reading = analogRead(pin);
    float voltage = reading * 5.0;
    voltage /= 1024.0;
    float temperatureCelsius = (voltage - 0.5) * 100 ;
    sumaTemperatura = sumaTemperatura + temperatureCelsius;
  }
  return sumaTemperatura / (float)count;
}

int Humidity_Smooth(int data, float filterVal, float smoothedVal)
{
  if(filterVal > 1)
  {
    filterVal = 99;
  }
  else
    if (filterVal <= 0)
    {
      filterVal = 0;
    }
  smoothedVal = (data *(1 - filterVal)) + (smoothedVal * filterVal);

  return (int)smoothedVal;
}

void PrintScannerData()
{
  Serial.println("scanner_data");

  Serial.print("light: ");
  Serial.print(scannerData.light_value[0]);
  Serial.print("; ");
  Serial.println(scannerData.light_value[1]);

  Serial.print("temperature: ");
  Serial.println(scannerData.temperature_value);

  Serial.print("humidity: ");
  Serial.println(scannerData.humidity_value);

  Serial.print("distance: ");
  Serial.println(scannerData.distance_value);

  Serial.print("gas: ");
  Serial.print(scannerData.mq2_value[0]);
  Serial.print("; ");
  Serial.println(scannerData.mq2_value[1]);

  Serial.print("motion: ");
  Serial.println(scannerData.motion_value);
  
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

