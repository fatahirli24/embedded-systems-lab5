The aim of this task was to read the X and Y axis values of a joystick using Arduino analog 
inputs and use these values to determine movement direction. Four LEDs were used to indicate 
up, down, left, and right motion. The joystick button was also read as a digital input. In addition, 
the X and Y values and button state were sent to the Serial Monitor in real time for observation 
and testing. 
Hardware Configuration 
 Arduino Uno 
 Joystick module 
 4 LEDs 
 4 resistors 
 Breadboard 
 Jumper wires 
Component 
Joystick X output         
Joystick Y output        
Joystick button         
Up LED        
Down LED         
Left LED        
Right LED         
Arduino Pin Purpose 
A0 
A1 
2 
10 
9 
11 
6 
Reads horizontal position 
Reads vertical position 
Reads push-button state 
Indicates upward movement 
Indicates downward movement 
Indicates left movement 
Indicates right movement 
The joystick module provides two analog outputs representing the X and Y positions and one 
digital button output. The analog outputs were connected to pins A0 and A1, while the push
button output was connected to pin 2 using the internal pull-up resistor. Four LEDs were 
connected to separate output pins to indicate movement direction. 
Code Implementation 
The setup() function initializes Serial communication and configures the joystick and LED pins. 
The button pin uses INPUT_PULLUP, so it reads HIGH when released and LOW when pressed. 
The joystick X and Y axis values are read from the analog pins, while the push-button state is 
read digitally. 
The map() function converts joystick position values into PWM brightness levels from 0 to 255. 
This allows the LED brightness to increase as the joystick is pushed more far away from its 
center position. 
These conditions determine which LED should respond based on joystick position. Vertical 
motion controls the up and down LEDs, while horizontal motion controls the left and right 
LEDs. 
Function in code 
analogRead(A0) 
analogRead(A1) 
pinMode(buttonPin, 
INPUT_PULLUP) 
digitalRead(buttonPin) 
analogWrite(upLed, ...) 
analogWrite(downLed, 
...) 
Register/peripheral Bit(s) / role Function in 
this lab 
Reads 
ADC 
ADC 
DDRD / PORTD 
PIND 
Timer/PWM output 
Timer/PWM output 
analogWrite(leftLed, ...) Timer/PWM output 
ADMUX, 
ADCSRA 
ADMUX, 
ADCSRA 
DDD2, 
PORTD2 
PIND2 
PWM 
hardware on 
pin 10 
PWM 
hardware on 
pin 9 
PWM-related 
output 
behavior 
joystick X 
axis 
Reads 
joystick Y 
axis 
Sets button as 
input with 
pull-up 
Reads 
joystick 
button state 
Controls LED 
brightness 
Controls LED 
brightness 
Controls LED 
brightness 
Evidence 
X values change 
in Serial Monitor 
Y values change 
in Serial Monitor 
Button reads 
LOW when 
pressed 
Serial shows 
button state 
change 
LED brightness 
changes with 
joystick 
movement 
Down LED 
brightens when 
joystick moves 
down 
Left LED 
brightens when 
joystick moves 
left 
Register/peripheral Bit(s) / role Function in 
Function in code 
analogWrite(rightLed, ...) Timer/PWM output 
this lab 
PWM 
hardware on 
pin 6 
Controls LED 
brightness 
Evidence 
Right LED 
brightens when 
joystick moves 
right 
The joystick X and Y values are read through the ADC subsystem, where channel selection and 
conversion are controlled by ADC registers such as ADMUX and ADCSRA. The button input 
uses the digital I/O registers, and the internal pull-up resistor is enabled through the port control 
logic. The LED brightness control is achieved using PWM output pins. These functions are 
supported by the changing Serial Monitor values and by the visible LED brightness changes 
when the joystick is moved. 
Circuit Diagram 
<img width="312" height="177" alt="image" src="https://github.com/user-attachments/assets/87bbdd6d-48ea-4523-86ef-238e290ee363" />

Discussion 
The joystick center position was approximately near the midpoint of the ADC range, which is 
why threshold values around 509 to 512 were used in the program. These values are supported 
by observing the Serial monitor. Because the joystick outputs analog voltages, the measured 
values vary smoothly rather than switching instantly. 
