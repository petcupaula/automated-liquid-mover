/* 
 *  Simple example for moving a DC motor (or a peristaltic pump, which would be dispensing water or some other liquid)
 *  for 1000 ms, waiting for 1000 ms, and then doing it over again.
 *
 *  Setup based on: https://mechatrofice.com/arduino/relay-module-interface
 */

#define motor 2

void setup() {
  pinMode(motor, OUTPUT);
}

void loop() {
  digitalWrite(motor, HIGH);
  delay(1000);
  digitalWrite(motor, LOW);
  delay(1000);
}
