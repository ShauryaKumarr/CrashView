/*
  LSM6DSO_raw_fast.ino
  Read accel + gyro from LSM6DSO @ 0x6B via I²C, no extra libraries,
  printing ~10×/s instead of 2×/s.
*/

#include <Wire.h>

#define LSM6DSO_ADDR   0x6B
#define WHO_AM_I_REG   0x0F
#define CTRL1_XL       0x10
#define CTRL2_G        0x11
#define OUTX_L_XL      0x28
#define OUTX_L_G       0x22

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  Wire.begin();

  // Check WHO_AM_I
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(WHO_AM_I_REG);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 1);
  if (Wire.available()) {
    uint8_t who = Wire.read();
    if (who != 0x6C) {
      Serial.println("Unexpected device, halting.");
      while (1) delay(10);
    }
  } else {
    Serial.println("No response, check wiring.");
    while (1) delay(10);
  }

  // Configure accel (1.66 kHz, ±2g) and gyro (1.66 kHz, 250 dps)
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(CTRL1_XL);
  Wire.write(0b10000010);
  Wire.endTransmission();

  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(CTRL2_G);
  Wire.write(0b10001000);
  Wire.endTransmission();
}

void loop() {
  uint8_t buf[12];
  int16_t ax, ay, az, gx, gy, gz;

  // Read accel
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(OUTX_L_XL);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 6);
  for (int i = 0; i < 6; i++) buf[i] = Wire.read();

  // Read gyro
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(OUTX_L_G);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 6);
  for (int i = 0; i < 6; i++) buf[6 + i] = Wire.read();

  // Combine bytes
  ax = (int16_t)(buf[1] << 8 | buf[0]);
  ay = (int16_t)(buf[3] << 8 | buf[2]);
  az = (int16_t)(buf[5] << 8 | buf[4]);
  gx = (int16_t)(buf[7] << 8 | buf[6]);
  gy = (int16_t)(buf[9] << 8 | buf[8]);
  gz = (int16_t)(buf[11] << 8 | buf[10]);

  // Convert
  const float accel_sens = 0.061e-3 * 9.80665;
  const float gyro_sens  = 8.75e-3;

  // Example: Only display ax, ay, az every second
  Serial.print("{");
  Serial.print("ax:"); Serial.print(ax * accel_sens, 2);
  Serial.print(",ay:"); Serial.print(ay * accel_sens, 2);
  Serial.print(",az:"); Serial.print(az * accel_sens, 2);
  Serial.print(",gx:"); Serial.print(gx * gyro_sens, 2);
  Serial.print(",gy:"); Serial.print(gy * gyro_sens, 2);
  Serial.print(",gz:"); Serial.print(gz * gyro_sens, 2);
  Serial.println("}");

  delay(1000);  // 1 reading per second
}
