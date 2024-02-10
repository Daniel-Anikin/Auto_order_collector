#include "smotor.h"
#include "Servo.h"



SMotor::SMotor()
: _attached(false)
{
	set_reversed(false);
}

SMotor::SMotor(byte pin)
{
	attach(pin);
	set_reversed(false);
}

SMotor::SMotor(byte pin, bool reversed)
{
	attach(pin);
	set_reversed(reversed);
}

SMotor::~SMotor()
{
	
}

bool SMotor::is_attached(){
	return servo.attached();
}

void SMotor::set_speed(int speed)
{
	if (!is_attached())
		return;
	_speed = speed;
	speed = _reversed ? -speed : speed;
	byte new_speed = map(speed, -100, 100, 0, 180);
	new_speed = constrain(new_speed, 0, 180);
	servo.write(new_speed);
}

int SMotor::get_speed()
{
	return _speed;
}

void SMotor::set_reversed(bool reversed)
{
	_reversed = reversed;
}

bool SMotor::get_reversed()
{
	return _reversed;
}

void SMotor::stop()
{
	set_speed(0);
}

void SMotor::attach(byte pin)
{
	_pin = pin;
	servo.attach(_pin);
}

void SMotor::attach(byte pin, int min, int max)
{
	_pin = pin;
	servo.attach(_pin, min, max);
}

void SMotor::detach()
{
	stop();
	servo.detach();
}
