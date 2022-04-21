#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include <WiFiManager.h>
#include <iostream>

#define API_HOST_URL "http://api.iot.hva-robots.nl/crypto"

//#define WEBSERVER_CRYPTO_URL "https://192.168.178.241:5000/api/crypto"
#define WEBSERVER_CRYPTO_URL "http://192.168.178.241:5000/api/crypto"
#define HOST "https://192.168.178.241:5000"

WiFiClientSecure client;
WiFiClient unsecureClient;

HTTPClient http;
HTTPClient http2;

// Fingerprint of the self-signed certificate to perform HTTPS requests
const char *fingerprint = "9cf528809965a62dec543f9df4f0428717f01594";
const int httpsPort = 443;

byte counter = 0;

// ESP2866 pin mappings
byte PIN_D0 = 16;
byte PIN_D1 = 5;
byte PIN_D2 = 4;
byte PIN_D3 = 0;
byte PIN_D4 = 2;
byte PIN_D5 = 14;
byte PIN_D6 = 12;
byte PIN_D7 = 13;
byte PIN_D8 = 15;

float getUserProfit(const char* email, const char* password) // Get the total amount of profit of a user
{

  String profitResponse;

  Serial.print("[HTTP] GET 2 begin...\n");

  //String userProfitUrl = String("https://192.168.178.241:5000/api/users/profit/") + userId;
  String userProfitUrl = String("http://192.168.178.241:5000/api/users/profit");

  http.setAuthorization(email, password);

  //  if (client.verify(fingerprint, HOST)) { // Verify if the fingerprint is the same as the webserver's fingerprint
  if (http.begin(unsecureClient, userProfitUrl))
  {

  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
  {
    profitResponse = http.getString();
  }
  else
  {
    Serial.printf("[HTTP] GET 2... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
  }

  return profitResponse.toFloat();
}

void put_crypto_info(String cryptoInfo) // Replace ("PUT") the crypto information to the webserver
{

  Serial.print("[HTTP] PUT begin...\n");

  // if (client.verify(fingerprint, HOST)) { // Verify if the fingerprint is the same as the webserver's fingerprint
  if (http2.begin(unsecureClient, WEBSERVER_CRYPTO_URL))
  {

  http.addHeader("Content-Type", "text/plain");

  int httpCode = http2.PUT(cryptoInfo);

  Serial.println(httpCode);
  if (httpCode > 0)
  {
    String response = http2.getString();
  }
  else
  {
    Serial.printf("[HTTP] PUT... failed, error: %s\n", http2.errorToString(httpCode).c_str());
  }

  http2.end();
  }
}

String get_crypto_info() // HTTP request to retreive the crypto information from the API
{

  String response;

  Serial.print("[HTTP] GET begin...\n");
  if (http.begin(unsecureClient, API_HOST_URL))
  {

    int httpCode = http.GET();

    if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
    {
      response = http.getString();
    }
    else
    {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }

  return response;
}

void setup()
{
  Serial.begin(9600);

  pinMode(PIN_D8, OUTPUT);
  pinMode(PIN_D7, OUTPUT);

  WiFiManager wifiManager;
  wifiManager.autoConnect("AutoConnectAP", AP_PASS);
  Serial.println("Connected.....");

  // Set fingerpint to connect to the server
  //client.setFingerprint(fingerprint);

  // If host is not responding, return
  //if (!client.connect(HOST, 5000))
  //{
    //Serial.println("Connection failed!!!!!");
    //return;
  //}

}

void loop()
{

  String cryptoInfo = get_crypto_info();
  Serial.println(cryptoInfo);

  put_crypto_info(cryptoInfo);

  const char* email = "p@gmail.com";
  const char* password = "penguin";
  float userProfit = getUserProfit(email, password);

  Serial.println(userProfit);

  // if (userProfit > 500)
  // {
  //   if (counter <= 4) {
  //   digitalWrite(PIN_D8, HIGH);
  //   digitalWrite(PIN_D7, HIGH); // LED on
  //   delay(1000);
  //   digitalWrite(PIN_D8, LOW);
  //   digitalWrite(PIN_D7, LOW); // LED off
  //   delay(3000);
  //   counter++;
  //   } else {
  //   delay(60000);
  //   counter = 0;
  //   }
  // }

  // if (userProfit < -300)
  // {
  //   if (counter <= 4) {
  //   digitalWrite(PIN_D8, HIGH);
  //   digitalWrite(PIN_D7, HIGH); // LED on
  //   delay(500);
  //   digitalWrite(PIN_D8, LOW);
  //   digitalWrite(PIN_D7, LOW); // LED off
  //   delay(500);
  //   counter++;
  //   } else {
  //   delay(60000);
  //   counter = 0;
  //   }
  // }

  delay(30000);
}
