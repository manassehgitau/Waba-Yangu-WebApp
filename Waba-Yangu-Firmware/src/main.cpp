
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <MpesaSTK.h>

// get your credentials from;
// https://developer.safaricom.co.ke/user/me/apps
// https://developer.safaricom.co.ke/test_credentials
String consumer_key = "JdApLaok3X42Pr4FxDYGjU14WS2FdSIkdWDdhPT5RelxYgHT";
String consumer_secret = "PbGxGcpG5KRcaOJelSgfPA0txsqZGuKk8bPNucf1Thi1hnHEo9MUarXHvDOup7F4";
String pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919";

ESP8266WiFiMulti wifiMulti;

// MpesaSTK mpesa(consumer_key, consumer_secret, pass_key);	//defaults to SANDBOX environment
MpesaSTK mpesa(consumer_key, consumer_secret, pass_key, SANDBOX); // environment can be SANDBOX(default) or PRODUCTION

char *WIFI_SSID = "TUK-WIFI";
char *WIFI_PASS = "P@ssword@123";

void setup()
{
  Serial.begin(115200);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASS);

  Serial.print("Waiting for WiFi to connect...");
  while ((wifiMulti.run() != WL_CONNECTED))
  {
    Serial.print(".");
  }
  Serial.println(" connected");

  mpesa.begin(TEST_CODE, PAYBILL, "https://mycallbackurl.com/checkout.php", 0, false); // call this in setup after connected to the internet

  String result = mpesa.pay("254796921547", 20, "Arduino", "Test"); // STK request
  // you can also implement this in the loop but remember each call performs an STK Request
  Serial.println(result);
}

void loop()
{
  // nothing here
}
