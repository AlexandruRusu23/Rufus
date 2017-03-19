#define LIGHT_1_PIN         A2
#define LIGHT_2_PIN         A3
#define TEMPERATURE_PIN     A4
#define HUMIDITY_PIN        A5

struct ScannerData
{
  int                   light_value[2];
  float                 humidity_value;
  float                 temperature_value;
};

ScannerData             scannerData;

float                   humi;
float                   prehum;
float                   humconst;
float                   truehum;
float                   pretruehum; 
long                    pretruehumconst; 
long                    valb;

unsigned long           scanner_timer;

void setup() {
  delay(500);
  Serial.begin(9600);

  // INPUT pins
  pinMode(LIGHT_1_PIN,          INPUT);
  pinMode(LIGHT_2_PIN,          INPUT);
  pinMode(TEMPERATURE_PIN,      INPUT);
  pinMode(HUMIDITY_PIN,         INPUT);

  delay(500);
}

void loop() {
  if(millis() - scanner_timer > 5000)
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
  
  Serial.println("end_scanner_data");
  Serial.println("");
}
