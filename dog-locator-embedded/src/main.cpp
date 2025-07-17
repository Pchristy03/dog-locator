#include <Arduino.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

HardwareSerial gpsSerial(2); // TX = 26, RX = 25
HardwareSerial loraSerial(1);
TinyGPSPlus gps;
float lattitude, longitude;

void handleLoraResponse();
void sendInfoMessage(String infoData);
void sendGpsData();

// vcc gnd tx rx pps
// great youtube video showing how to use the lora module https://www.youtube.com/watch?v=LiWlPERp1ec
// blue is TX
// white is RX

unsigned long lastSend = 0;

void sendInfoMessage(String infoData)
{
  String payload = "AT+SEND=2,24,{\"info\": \"" + infoData + "\"}";
  Serial.println(payload);
  loraSerial.println(payload);
}

void handleLoraResponse()
{
  String loraLine = "";

  while (loraSerial.available())
  {
    char c = loraSerial.read();
    if (c == '\n' || c == '\r')
    {
      if (loraLine.length() > 0)
      {
        Serial.println("LoRa: " + loraLine);
        loraLine = "";
      }
    }
    else
    {
      loraLine += c;
    }
  }
}

void sendGpsData()
{
  while (gpsSerial.available())
  {
    if (gps.encode(gpsSerial.read()) && gps.location.isUpdated())
    {
      if ((millis() - lastSend) > 10000)
      {
        String lng = String(gps.location.lng(), 6);
        String lat = String(gps.location.lat(), 6);
        String latAndLonPayload = String("{\"lon\": \"" + lng + "\", \"lat\": \"" + lat + "\"}");
        String payload = "AT+SEND=2," + String(latAndLonPayload.length()) + "," + latAndLonPayload;

        Serial.println(payload);
        loraSerial.println(payload);

        loraSerial.flush();
        lastSend = millis();
      }
    }
  }
}

void setup()
{
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, 25, 26);
  loraSerial.begin(115200, SERIAL_8N1, 22, 21);

  delay(3000);

  Serial.println("Serial Created... Starting Location Capture");
  sendInfoMessage("Sending Data");

  delay(2000);
}

void loop()
{
  handleLoraResponse();
  sendGpsData();
}