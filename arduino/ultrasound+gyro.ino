#include <Wire.h>

// ————— Ultrasonic sensor pins —————
const int trigPin = 9;
const int echoPin = 10;

// ————— LSM6DSO I²C settings —————
#define LSM6DSO_ADDR   0x6B
#define WHO_AM_I_REG   0x0F
#define CTRL1_XL       0x10
#define CTRL2_G        0x11
#define OUTX_L_XL      0x28
#define OUTX_L_G       0x22

void setup() {
  // Serial at 115200 for both sensors
  Serial.begin(115200);
  while (!Serial) { delay(5); }

  // Ultrasonic pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // I²C bus
  Wire.begin();

  // Check WHO_AM_I
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(WHO_AM_I_REG);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 1);
  if (!Wire.available() || Wire.read() != 0x6C) {
    Serial.println("LSM6DSO not found!");
    while (1) delay(100);
  }

  // Configure accel (1.66 kHz, ±2 g)
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(CTRL1_XL);
  Wire.write(0b10000010);
  Wire.endTransmission();

  // Configure gyro (1.66 kHz, 250 dps)
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(CTRL2_G);
  Wire.write(0b10001000);
  Wire.endTransmission();
}

void loop() {
  // --- 1) Read ultrasonic distance ---
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  float distanceCm = (duration > 0) ? (duration * 0.0343 / 2.0) : -1;

  // --- 2) Read accel + gyro from LSM6DSO ---
  uint8_t buf[12];
  int16_t ax, ay, az, gx, gy, gz;

  // accel
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(OUTX_L_XL);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 6);
  for (int i = 0; i < 6; i++) buf[i] = Wire.read();

  // gyro
  Wire.beginTransmission(LSM6DSO_ADDR);
  Wire.write(OUTX_L_G);
  Wire.endTransmission(false);
  Wire.requestFrom(LSM6DSO_ADDR, 6);
  for (int i = 0; i < 6; i++) buf[6 + i] = Wire.read();

  ax = (int16_t)(buf[1] << 8 | buf[0]);
  ay = (int16_t)(buf[3] << 8 | buf[2]);
  az = (int16_t)(buf[5] << 8 | buf[4]);
  gx = (int16_t)(buf[7] << 8 | buf[6]);
  gy = (int16_t)(buf[9] << 8 | buf[8]);
  gz = (int16_t)(buf[11] << 8 | buf[10]);

  // convert to physical units
  const float accel_sens = 0.061e-3 * 9.80665;  // g‑to‑m/s²
  const float gyro_sens  = 8.75e-3;             // dps

  float ax_g = ax * accel_sens;
  float ay_g = ay * accel_sens;
  float az_g = az * accel_sens;
  float gx_d = gx * gyro_sens;
  float gy_d = gy * gyro_sens;
  float gz_d = gz * gyro_sens;

  // --- 3) Print everything ---
  Serial.print("Dist(cm): ");
  if (distanceCm < 0) {
    Serial.print("Out of range");
  } else {
    Serial.print(distanceCm, 1);
  }

  Serial.print("  |  Acc(m/s2): ");
  Serial.print(ax_g, 2); Serial.print(", ");
  Serial.print(ay_g, 2); Serial.print(", ");
  Serial.print(az_g, 2);

  Serial.print("  |  Gyro(dps): ");
  Serial.print(gx_d, 1); Serial.print(", ");
  Serial.print(gy_d, 1); Serial.print(", ");
  Serial.println(gz_d, 1);

  // adjust delay as needed
  delay(200);
}
