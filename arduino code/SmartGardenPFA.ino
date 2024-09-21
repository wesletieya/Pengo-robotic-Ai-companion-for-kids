#define BLYNK_TEMPLATE_ID "TMPL2YCwH7OUu"
#define BLYNK_TEMPLATE_NAME "Plant Watering System"


#include <LiquidCrystal_I2C.h>
//Include the library files

#include <Wire.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

#define sensor 34
#define relay 13

//Initialize the LCD display
LiquidCrystal_I2C lcd(0x27, 16, 2);

BlynkTimer timer;

// Enter your Auth token
char auth[] = "PvViO8nF2UrTvLCf4xxk8qNS4h12DyGh";

//Enter your WIFI SSID and password
char ssid[] = "HUAWEI-4v6J";
char pass[] = "dNbq9yd6";
IPAddress serverIP(192, 168, 100, 9); // IP of your computer where Python script is running
const uint16_t serverPort = 5005;

WiFiClient client;

int value=0;
int wateringThreshold=30;
bool notified=false;
bool buttonenabled=false;

const int buttonPin = 19;     // Pin où le bouton poussoir est connecté
int buttonState = 0; 

void setup() {
  // Debug console
  pinMode(sensor,INPUT);
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
  lcd.init();
  lcd.backlight();
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);

  lcd.setCursor(1, 0);
  lcd.print("System Loading");
  for (int a = 0; a <= 15; a++) {
    lcd.setCursor(a, 1);
    lcd.print(".");
    delay(200);
  }
  lcd.clear();
  WiFi.begin(ssid, pass);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    
    Serial.println("Connected to WiFi");
    
    if (!client.connect(serverIP, serverPort)) {
        Serial.println("Connection to server failed");
    } else {
        Serial.println("Connected to server");
    }
  pinMode(buttonPin,INPUT);

}

//Get the ultrasonic sensor values
void soilMoisture() {
  
  value = analogRead(sensor);
  value = map(value, 0, 4095, 0, 100);
  value = (value - 100) * -1;
  
  Blynk.virtualWrite(V0, value);
  //Serial.println(value);
  lcd.setCursor(0, 0);
  lcd.print("Moisture :");
  lcd.print(value);
  lcd.print("%");
  
  
}

//Get the button value
BLYNK_WRITE(V1) {

  if(!buttonenabled){
    Serial.println("Button interaction is disabled.");
    return; // Ignorer l'événement du bouton si l'interaction est désactivée
  }

  bool RelayBol = param.asInt();
  if (RelayBol == 1) {
    digitalWrite(relay, HIGH);
    lcd.setCursor(0, 1);
    lcd.print("Motor is ON ");
  } else {
    digitalWrite(relay, LOW);
    lcd.setCursor(0, 1);
    lcd.print("Motor is OFF");
  }
}

void SEND_DATA_TO_PYTHON(String s){
  Serial.println(s);
  while(!client.connect(serverIP,serverPort)){
          Serial.println("Disconnected");
      }
  if (client.connected()) {
        Serial.println("Connected!");
        client.println(s);
        delay(2000); // Send data every 2 seconds
    }
}

void receivedDataFromPython() {
  
  while(!client.available());

  String receivedData = client.readStringUntil('\n');
  Serial.println("Received from Python: " + receivedData);
    // Process the received data as needed
  
}

void loop() {

  Blynk.run();
  Blynk.virtualWrite(V2, "Kiddo Must Complete His Tasks");
  int score=0;
  soilMoisture();
  //Serial.println(value);
  buttonState=digitalRead(buttonPin);
  Serial.println(buttonState);
  while(!buttonState){
    buttonState=digitalRead(buttonPin);
  }
  SEND_DATA_TO_PYTHON("FIRST_TASK");
  
  receivedDataFromPython();
  score+=100;
  soilMoisture();
  if (score==100){
    if(value <wateringThreshold){
      buttonenabled=true;
      Serial.println(buttonenabled);
      Blynk.run();
      
      while(value<wateringThreshold){
        soilMoisture(); 
        Blynk.run();
        Blynk.virtualWrite(V2, "Kiddo has completed his tasks Water your Plant!");
         delay(1000);
      }
     digitalWrite(relay, LOW);
     Blynk.run();
     Blynk.virtualWrite(V2, "Plant Watered!");
     delay(1000);
     buttonenabled=false;
    }
    else {
      Blynk.run();
      Blynk.virtualWrite(V2,"Kiddo has completed his tasks!");
      delay(1000);
    }

  }
}


 /* if (value < wateringThreshold)
  {
    buttonenabled=true;
     Blynk.virtualWrite(V2, "Arrosez votre Plante!");
     while(value<wateringThreshold){
       soilMoisture();
       Blynk.run();//Run the Blynk library
     }
     digitalWrite(relay, LOW);
    Blynk.virtualWrite(V2, "Plante Arrosée!");
    buttonenabled=false;
  }*/
  
