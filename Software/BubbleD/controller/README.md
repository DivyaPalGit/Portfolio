# Connecting to the external controller

To connect the BubbleD software to the external controller the `StandardFrimata.ino` should be uploaded to the Teensy 4.1 microcontroller board.

## Dependencies
ArduinoIDE with Teensyduino (for installation see https://www.pjrc.com/teensy/tutorial.html) is needed to upload the `StandardFrimata.ino` to the Teensy 4.1 microcontroller board. After installation of ArduinoIDE, the `StandardFrimata.ino` can be found in `Arduino/libraries/Firmata/examples/StandardFirmata` and for it to work with Teensy 4.1 the following additions are required in the `Boards.h` stored in `Arduino/libraries/Firmata`.

```
// Teensy 4.0 & 4.1
#elif defined(__IMXRT1062__)
#define TOTAL_ANALOG_PINS       NUM_ANALOG_INPUTS
#define TOTAL_PINS              NUM_DIGITAL_PINS
#define VERSION_BLINK_PIN       13
#define PIN_SERIAL1_RX          0
#define PIN_SERIAL1_TX          1
#define PIN_SERIAL2_RX          7
#define PIN_SERIAL2_TX          8
#define PIN_SERIAL3_RX          15
#define PIN_SERIAL3_TX          14
#define PIN_SERIAL4_RX          16
#define PIN_SERIAL4_TX          17
#define PIN_SERIAL5_RX          21
#define PIN_SERIAL5_TX          20
#define PIN_SERIAL6_RX          25
#define PIN_SERIAL6_TX          24
#define PIN_SERIAL7_RX          28
#define PIN_SERIAL7_TX          29
#define IS_PIN_DIGITAL(p)       ((p) >= 0 && (p) < NUM_DIGITAL_PINS)
#ifdef ARDUINO_TEENSY40
  #define IS_PIN_ANALOG(p)        ((p) >= 14 && (p) <= 27)
  #define PIN_TO_ANALOG(p)        ((p) - 14)
#endif
#ifdef ARDUINO_TEENSY41
  #define IS_PIN_ANALOG(p)        (((p) >= 14 && (p) <= 27) || ((p) >= 38 && (p) <= 41))
  #define PIN_TO_ANALOG(p)        (((p) <= 27) ? (p) - 14 : (p) - 24)
#endif
#define IS_PIN_PWM(p)           digitalPinHasPWM(p)
#define IS_PIN_SERVO(p)         ((p) >= 0 && (p) < MAX_SERVOS)
#define IS_PIN_I2C(p)           ((p) == PIN_WIRE_SDA || (p) == PIN_WIRE_SCL)
#define IS_PIN_SERIAL(p)        (((p) >= 0 && (p) <= 1) || ((p) >= 7 && (p) <= 8) || ((p) >= 14 && (p) <= 17) || ((p) >= 20 && (p) <= 21) || ((p) >= 24 && (p) <= 25) || ((p) >= 28 && (p) <= 29))
#define PIN_TO_DIGITAL(p)       (p)
#define PIN_TO_PWM(p)           (p)
#define PIN_TO_SERVO(p)         (p)

```
