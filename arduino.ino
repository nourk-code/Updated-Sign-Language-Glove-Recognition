#include <ADXL345.h>  // ADXL345 Accelerometer Library
#include <ITG3200.h>  // ITG3200 Gyroscope Library

ADXL345 acc; // Instance of the ADXL345 accelerometer library
ITG3200 gyro = ITG3200();
float gx, gy, gz;
float gx_rate, gy_rate, gz_rate;
int ix, iy, iz;
float anglegx=0.0, anglegy=0.0, anglegz=0.0;
int ax, ay, az;  
int rawX, rawY, rawZ;
float X, Y, Z;
float rollrad, pitchrad;
float rolldeg, pitchdeg;
int error = 0; 
float aoffsetX, aoffsetY, aoffsetZ;
float goffsetX, goffsetY, goffsetZ;
unsigned long time, looptime;
// Define pins for the flex sensors
const int flexPins[] = {A0, A1, A2, A3, A4}; // Pins connected to voltage divider outputs
const int numSensors = 5; // Number of sensors

// Constants
const float VCC = 5;           // Voltage at Arduino 5V line
const float R_DIV = 47000.0;   // Resistor used to create a voltage divider
const float flatResistance = 25000.0; // Resistance when flat
const float bendResistance = 100000.0; // Resistance at 90 degrees
float alpha = 0.5; // Smoothing factor
float filteredX = 0, filteredY = 0, filteredZ = 0;



void filterAccelData(int rawX, int rawY, int rawZ) {
  filteredX = alpha * filteredX + (1 - alpha) * (rawX / 256.00);
  filteredY = alpha * filteredY + (1 - alpha) * (rawY / 256.00);
  filteredZ = alpha * filteredZ + (1 - alpha) * (rawZ / 256.00);
}


void setup(){
  Serial.begin(9600);
  acc.powerOn();
  gyro.init(ITG3200_ADDR_AD0_LOW);
  // calibrateSensors();  // Call the enhanced calibration function

  for (int i = 0; i < numSensors; i++) {
    pinMode(flexPins[i], INPUT);
    // pinMode(flexPins[i], INPUT);
  }
  acc.powerOn();
  // Calibrate accelerometer
  for (int i = 0; i <= 200; i++) {
    acc.readAccel(&ax, &ay, &az);
    if (i == 0) {
      aoffsetX = ax;
      aoffsetY = ay;
      aoffsetZ = az;
    }
    if (i > 1) {
      aoffsetX = (ax + aoffsetX) / 2;
      aoffsetY = (ay + aoffsetY) / 2;
      aoffsetZ = (az + aoffsetZ) / 2;
    }
  }
  // Calibrate gyroscope
  for (int i = 0; i <= 200; i++) {
    gyro.readGyro(&gx,&gy,&gz);
    if (i == 0) {
      goffsetX = gx;
      goffsetY = gy;
      goffsetZ = gz;
    }
    if (i > 1) {
      goffsetX = (gx + goffsetX) / 2;
      goffsetY = (gy + goffsetY) / 2;
      goffsetZ = (gz + goffsetZ) / 2;
    }
  }
  delay(1000);
  gyro.init(ITG3200_ADDR_AD0_LOW);
  time = millis();  // Initialize 'time' at the end of setup

}

void loop() {
  static unsigned long lastMeasurement = 0;
  unsigned long currentMillis = millis();

  if (currentMillis - lastMeasurement >= 10) {  // Data capture every 10 milliseconds
    lastMeasurement = currentMillis;

    acc.readAccel(&ax, &ay, &az);
    rawX = ax - aoffsetX;
    rawY = ay - aoffsetY;
    rawZ = az - aoffsetZ;
    filterAccelData(rawX, rawY, rawZ);

    rollrad = atan2(filteredY, sqrt(filteredX * filteredX + filteredZ * filteredZ));
    pitchrad = atan2(filteredX, sqrt(filteredY * filteredY + filteredZ * filteredZ));
    rolldeg = 180 * rollrad / PI;
    pitchdeg = 180 * pitchrad / PI;

    // Gyroscope readings
    gyro.readGyro(&gx, &gy, &gz);
    gx_rate = (gx - goffsetX) / 14.375;
    gy_rate = (gy - goffsetY) / 14.375;
    gz_rate = (gz - goffsetZ) / 14.375;

    float deltaTime = (currentMillis - time) / 1000.0;
    anglegx += gx_rate * deltaTime;
    anglegy += gy_rate * deltaTime;
    anglegz += gz_rate * deltaTime;

    for (int i = 0; i < numSensors; i++) {
      int ADCflex = analogRead(flexPins[i]);
      float Vflex = ADCflex * VCC / 1023.0;
      float Rflex = R_DIV * (VCC / Vflex - 1.0);
      float angle = map(Rflex, flatResistance, bendResistance, 0, 90.0);

      Serial.print(angle);
      Serial.print(",");
    }

    

    // Print angles
    Serial.print(rolldeg);
    Serial.print(",");
    Serial.println(pitchdeg);
    // Serial.print(",");
    // Serial.print(anglegx);
    // Serial.print(",");
    // Serial.print(anglegy);
    // Serial.print(",");
    // Serial.println(anglegz);

    time = currentMillis;  // Update the last measurement time
  }
}
