
#include <Servo.h>
#include <HCSR04.h>

constexpr int triggerPin = 11, echoPin = 12, servo_pin = 10;

float distance;
uint8_t angle = 0;
String buffer;

UltraSonicDistanceSensor sensor(triggerPin, echoPin);
Servo radar_axis;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  radar_axis.attach(servo_pin);

  radar_axis.write(angle);
}

void loop() {
  static char c = {};

  while (Serial.available()){
    c = Serial.read();

    if(c == '\n'){

      switch(buffer[0]){
      case 'g':
        
        break;

      default:
        angle = buffer.toInt();
        break;
        
      }
      radar_axis.write(angle);

    
    
      distance = sensor.measureDistanceCm();

      Serial.print(angle);
      Serial.print(';'); 
      Serial.println(distance);

      buffer = "";
      angle = (angle + 1) % 181;

    }else{

      buffer += c;
    }
  }
  
}
