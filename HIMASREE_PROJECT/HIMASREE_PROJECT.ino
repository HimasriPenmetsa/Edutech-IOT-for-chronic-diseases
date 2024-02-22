#define BLYNK_TEMPLATE_ID "TMPL3T7mxvUqv"
#define BLYNK_TEMPLATE_NAME "HIMASRI"
#define BLYNK_AUTH_TOKEN "KQfMcmAPMpyc36vUjr5UmWK0lF61iaf7"

#ifdef ESP32
  #include <WiFi.h>
  #include <BlynkSimpleEsp32.h>
#else
  #include <ESP8266WiFi.h>
  #include <BlynkSimpleEsp8266.h>
#endif

#define BLYNK_PRINT Serial
 
char auth[] = "KQfMcmAPMpyc36vUjr5UmWK0lF61iaf7";    // authuntifaction id
char ssid[] = "project01";   //wifi name
char pass[] = "project01";   //wifi password

#include<LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000
PulseOximeter pox;
uint32_t tsLastReport = 0;

void onBeatDetected() {
    Serial.println("Beat!");
}

void setup() {
    Serial.begin(9600);

    lcd.init();
    lcd.backlight();

  lcd.clear();
  lcd.print("   ***READY***   ");
  delay(2000);
  lcd.clear();

  lcd.clear();
  lcd.print("CONNECTING TO...");
  lcd.setCursor(0,1);
  lcd.print(ssid);
  
  WiFi.begin(ssid, pass);
  Serial.print("Connectinh to WiFi");
  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(500);
  }
  
  Blynk.config(auth);
  Serial.println("READY");
  
  lcd.clear();
  lcd.print(" WIFI CONNECTED ");
  lcd.setCursor(0,1);
  lcd.print(WiFi.localIP());
  delay(1000);
  lcd.clear();
  
  lcd.clear();
  lcd.print("***  READY  ***");
  delay(1000);
  lcd.clear();


    Serial.print("Initializing pulse oximeter..");

    // Initialize sensor
    if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
    }

  // Configure sensor to use 7.6mA for LED drive
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);

    // Register a callback routine
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
    // Read from the sensor
    pox.update();

    // Grab the updated heart rate and SpO2 levels
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.print("Heart rate:");
        Serial.print(pox.getHeartRate());
        Serial.print("bpm / SpO2:");
        Serial.print(pox.getSpO2());
        Serial.println("%");

        lcd.clear();
        lcd.print("PULSE : ");lcd.print(pox.getHeartRate());
        lcd.setCursor(0,1);
        lcd.print("SPO2 : ");lcd.print(pox.getSpO2());

        Blynk.virtualWrite(V2, pox.getHeartRate());
        Blynk.virtualWrite(V3, pox.getSpO2());

        Blynk.run();

        tsLastReport = millis();
    }
}