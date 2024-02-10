#include "dc_motor.h"


DC_Motor::DC_Motor() 
: _attached(false)
{
	set_reversed(false);
}

DC_Motor::DC_Motor(byte dirPin, byte speedPin)
{
	attach(dirPin, speedPin);
	set_reversed(false);
}

DC_Motor::DC_Motor(byte dirPin, byte speedPin, bool reversed)
{
	attach(dirPin, speedPin);
	set_reversed(reversed);
}

DC_Motor::~DC_Motor(){

}

bool DC_Motor::is_attached(){
	return _attached;
}

void DC_Motor::set_speed(int speed){
	if (!is_attached())
		return;
	bool dir = (speed >= 0) xor _reversed;
	int pwm_speed = map(fabs(speed), 0, 100, 0, 255);
	pwm_speed = constain(pwm_speed, 0, 255);
	
	digitalWrite(_dirPin, dir);
	analogWrite(_speedPin, pwm_speed);
	_speed = speed;
}

int DC_Motor::get_speed(){
	return _speed;
}


void DC_Motor::set_reversed(bool reversed){
	_reversed = reversed;
}
	
bool DC_Motor::get_reversed(){
	return _reversed;
}
	
	

void DC_Motor::stop(){
	set_speed(0);
}

void DC_Motor::attach(byte dirPin, byte speedPin){
	_dirPin = dirPin;
	_speedPin = speedPin;
	pinMode(_dirPin, OUTPUT);
	pinMode(_speedPin, OUTPUT);
	_attached = true;
}

void DC_Motor::detach(){
	stop();
	pinMode(_dirPin, INPUT);
	pinMode(_speedPin, INPUT);
	_attached = false;
}