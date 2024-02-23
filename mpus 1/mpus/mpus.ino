#include "ThingSpeak.h"
#include <ESP8266WiFi.h>
#include <time.h>
unsigned long ch_no = 2440195;//ThingSpeak Channel number
const char * write_api = "JNYLPKU933J3HLFD";// API
char ssid[] = "project01";
char pass[] = "project01";
WiFiClient  client;
const char *str;

#include<LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;
float temp_sense;

String mode_status=" ";

#define gas D5
int gas_sense;
String gas_status=" ";

#define sw D7    // for wet detection
int sw_sense;
String sw_status=" ";

#define mode_sw D6
int mode_sense;

#define buzzer D3

float sensor_value;
float signal;

#define SAMPLE_RATE 125
#define INPUT_PIN A0

void setup()
{
  Serial.begin(9600);
  configTime(11 * 1800, 0, "pool.ntp.org", "time.nist.gov");

  pinMode(INPUT_PIN,INPUT);
  pinMode(gas,INPUT);
  pinMode(sw,INPUT);
  pinMode(mode_sw,INPUT);

  pinMode(buzzer,OUTPUT);
  digitalWrite(buzzer,LOW);

  pinMode(D0,OUTPUT);
  digitalWrite(D0,LOW);
  
  lcd.init();
  lcd.backlight();

  lcd.clear();
  lcd.print("MPU CHECKING");
  delay(1000);
  
  if (!mpu.begin()) 
  {
    Serial.println("Failed to find MPU6050 chip");
    lcd.clear();
    lcd.print("   MPU FAILED   ");
    delay(100);
    while (1) 
    {
      delay(10);
    }
  }
  
  Serial.println("MPU6050 Found!");
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);//accelerometer range +-8G
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);//gyro range +- 500 deg/s
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);//filter bandwidth 21 Hz
  delay(100);

  lcd.clear();
  lcd.print("CONNECTING TO...");
  lcd.setCursor(0,1);
  lcd.print(ssid);
  delay(1000);

  WiFi.begin(ssid, pass);
  Serial.print("Connecting to WiFi ..");
  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(500);
  }
  
  Serial.println("READY");

  lcd.clear();
  lcd.print(" WIFI CONNECTED ");
  delay(1000);

  ThingSpeak.begin(client);
}
void beep()
{
  digitalWrite(buzzer,HIGH);delay(300);digitalWrite(buzzer,LOW);delay(200);
  digitalWrite(buzzer,HIGH);delay(300);digitalWrite(buzzer,LOW);delay(200);
}
void loop()
{ 
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  temp_sense=(temp.temperature*1.8)+32;
  
  sw_sense=digitalRead(sw);

  gas_sense=digitalRead(gas);
  gas_sense=1-gas_sense;
  
  mode_sense=digitalRead(mode_sw);
  mode_sense=1-mode_sense;

  ECG_EEG();

  if(gas_sense == 1)
  {
    gas_status="ALERT";
  }
  else
  {
    gas_status="NORMAL";
  }
  
  if(sw_sense==1)
  {
    sw_status="ALERT";
  }
  else
  {
    sw_status="NORMAL";
  }
  
  if(mode_sense==1)
  {
    mode_status="MORNING";
    alert_mode();
  }
  else
  {
   mode_status="SLEEPY";
    sleepy_mode();
  }

  Serial.print("X : ");Serial.println(a.acceleration.x);
  Serial.print("TEMP : ");Serial.println(temp.temperature);

  lcd.clear();
  lcd.print("SWEAT : ");lcd.print(sw_status);
  lcd.setCursor(0,1);
  lcd.print("TEMPERATURE : ");lcd.print(temp_sense);
  digitalWrite(D0,LOW);delay(500);digitalWrite(D0,HIGH);delay(500);
  lcd.clear();
  lcd.print("SMOKE : ");lcd.print(gas_sense);
  lcd.setCursor(0,1);
  lcd.print("MODE : ");lcd.print(mode_status);
  digitalWrite(D0,LOW);delay(500);digitalWrite(D0,HIGH);delay(500);

  ThingSpeak.setField(1, temp_sense);
  ThingSpeak.setField(2, signal);
  ThingSpeak.setField(3, a.acceleration.x);
  ThingSpeak.setField(4, sw_sense);
  ThingSpeak.setField(5, gas_sense);
  ThingSpeak.writeFields(ch_no, write_api);
  digitalWrite(D0,LOW);delay(500);digitalWrite(D0,HIGH);delay(500);
}
void ECG_EEG() {
  // elapsed time
  static unsigned long past = 0;
  unsigned long present = micros();
  unsigned long interval = present - past;
  past = present;

  // Run timer
  static long timer = 0;
  timer -= interval;
  if(timer < 0){
    timer += 1000000 / SAMPLE_RATE;
    sensor_value = analogRead(INPUT_PIN);
    signal = ECGFilter(sensor_value);
    Serial.println(signal);
  }
}

float ECGFilter(float input)
{
  float output = input;
  {
    static float z1, z2; // filter
    float x = output - 0.70682283*z1 - 0.15621030*z2;
    output = 0.28064917*x + 0.56129834*z1 + 0.28064917*z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2;
    float x = output - 0.95028224*z1 - 0.54073140*z2;
    output = 1.00000000*x + 2.00000000*z1 + 1.00000000*z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2; 
    float x = output - -1.95360385*z1 - 0.95423412*z2;
    output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2; 
    float x = output - -1.98048558*z1 - 0.98111344*z2;
    output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
    z2 = z1;
    z1 = x;
  }
  return output;
}
void sleepy_mode()
{
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  temp_sense=(temp.temperature*1.8)+32;

  if(sw_sense==1 && temp_sense<=30)
  {
    beep();
  }
  else
  {
    digitalWrite(buzzer,LOW);
  }
}
void alert_mode()
{
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  temp_sense=(temp.temperature*1.8)+32;
  
  if((sw_sense==1 && temp.temperature <= 96)|| (a.acceleration.x<=-8.0 || a.acceleration.x>=8.0))  //in *C
  {
    beep();
  }
  else
  {
    digitalWrite(buzzer,LOW);
  }
}
