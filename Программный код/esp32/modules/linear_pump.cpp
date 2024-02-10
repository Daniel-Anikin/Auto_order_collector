#include "linear_pump.h"
#include "ender.h"
#include "motor.h"

LinearPump::LinearPump(Motor mot, Ender upEnder, Ender downEnder)
: _motor(mot)
, _upEnder(upEnder)
, _downEnder(downEnder)
{

}

void LinearPump::pumpIn()
{
	_motor.set_dir(RIGHT);
	_motor.run();
	while (!_upEnder.check());
	_motor.stop();
	_state = STOPPED;
}


void LinearPump::pumpOut()
{
	
}

void LinearPump::pump(bool dir)
{
	
}


void LinearPump::stPump(bool dir)
{
	_motor.set_dir(dir);
	_motor.run();
	_state = dir;
}

void LinearPump::stPumpIn()
{
	_motor.set_dir(RIGHT);
	_motor.run();
}

void LinearPump::stPumpOut()
{
	_motor.set_dir(LEFT);
	_motor.run();
}



void LinearPump::stop()
{
	_motor.stop();
	_state = STOPPED;
}



bool LinearPump::get_upEnderSt()
{
	return _upEnder.check();
}

bool LinearPump::get_downEnderSt()
{
	return _downEnder.check();
}



void LinearPump::set_speed(int speed)
{
	_motor.set_speed(speed);
}



bool LinearPump::tick()
{
	if (_state == IN){
		if (_upEnder.check()){
			_motor.stop();
			_state = STOPPED;
		}
	}
	else if (_state == OUT){
		if (_downEnder.check()){
			_motor.stop();
			_state = STOPPED;
		}
	}
	return _state == STOPPED ? 1 : 0;
}



		Ender _upEnder;
		Ender _downEnder;
		Servo _motor;
