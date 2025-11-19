#include <SoftwareSerial.h>
SoftwareSerial sensorSerial(2, 3);  // RX (to TXD), TX (to RXD)

const int GSR = A0;
const int LED = 13;
int threshold = 0;
int sensorValue;
byte startCommand[1] = {0x24};  // Start command

unsigned long lastCommandTime = 0;
unsigned long lastOutputTime = 0;
bool hrvStarted = false;

void setup() {
  Serial.begin(9600);
  sensorSerial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  // Initialize GSR threshold
  long sum = 0;
  for (int i = 0; i < 500; i++) {
    sensorValue = analogRead(GSR);
    sum += sensorValue;
    delay(5);
  }
  threshold = sum / 500;
  Serial.print("{\"GSR_threshold\": ");
  Serial.print(threshold);
  Serial.println("}");
}

void loop() {
  // ⏱ Resend start command every 3 seconds until the module starts sending data.
  if (!hrvStarted && millis() - lastCommandTime > 3000) {
    sensorSerial.write(startCommand, 1);
    Serial.println("📤 重发 HRV 启动指令 (0x24)");
    lastCommandTime = millis();
  }

  // 📈 GSR data reading
  sensorValue = analogRead(GSR);
  bool emotionDetected = false;
  int delta = threshold - sensorValue;

  if (abs(delta) > 60) {
    delay(20);
    int confirm = analogRead(GSR);
    if (abs(threshold - confirm) > 60) {
      emotionDetected = true;
      digitalWrite(LED, HIGH);
      delay(300);
      digitalWrite(LED, LOW);
    }
  }

  // 📦 HRV data reading (non-blocking mode)
  if (sensorSerial.available() >= 24) {
    byte buffer[24];
    for (int i = 0; i < 24; i++) {
      buffer[i] = sensorSerial.read();
    }

    // Check if packet header and footer are valid.
    if (buffer[0] == 0xFF && buffer[23] == 0xF1) {
      hrvStarted = true;  // Module has started working.
      // Extract data
      int heartRate = buffer[2];
      int bloodOxygen = buffer[3];
      int circulation = buffer[4];
      int highPressure = buffer[5];
      int lowPressure = buffer[6];
      int breathRate = buffer[7];
      int fatigue = buffer[8];
      int rrInterval = buffer[9];
      int hrvSdnn = buffer[10];
      int hrvRmssd = buffer[11];
      float bodyTemp = buffer[12] + buffer[13] / 100.0;

      // Output JSON data once per second
      if (millis() - lastOutputTime >= 1000) {
        Serial.print("{");
        Serial.print("\"GSR\": "); Serial.print(sensorValue); Serial.print(", ");
        Serial.print("\"EmotionDetected\": "); Serial.print(emotionDetected ? "true" : "false"); Serial.print(", ");
        Serial.print("\"HeartRate\": "); Serial.print(heartRate); Serial.print(", ");
        Serial.print("\"BloodOxygen\": "); Serial.print(bloodOxygen); Serial.print(", ");
        Serial.print("\"Circulation\": "); Serial.print(circulation); Serial.print(", ");
        Serial.print("\"BP_High\": "); Serial.print(highPressure); Serial.print(", ");
        Serial.print("\"BP_Low\": "); Serial.print(lowPressure); Serial.print(", ");
        Serial.print("\"BreathRate\": "); Serial.print(breathRate); Serial.print(", ");
        Serial.print("\"Fatigue\": "); Serial.print(fatigue); Serial.print(", ");
        Serial.print("\"RRInterval\": "); Serial.print(rrInterval); Serial.print(", ");
        Serial.print("\"HRV_SDNN\": "); Serial.print(hrvSdnn); Serial.print(", ");
        Serial.print("\"HRV_RMSSD\": "); Serial.print(hrvRmssd); Serial.print(", ");
        Serial.print("\"BodyTemp\": "); Serial.print(bodyTemp, 2);
        Serial.println("}");
        lastOutputTime = millis();
      }
    }
  }

  delay(20);  // Add slight delay to avoid blocking
}