#include "relay.h"


Relay::Relay()
	: _attached(false)
	, _reversed(false)
{
	
}
		
Relay::Relay(byte pin)
	, _reversed(false)
{
	attach(pin);
}
		
Relay::Relay(byte pin, bool is_reversed)
	: _reversed(is_reversed)
{
	attach(pin);
}
		
		
		
void Relay::attach(byte pin){
	_pin = pin;
	pinMode(_pin, OUTPUT);
}
		
void Relay::detach(){
	_attached = false;
}	
				
bool Relay::is_attached(){
	return _attached;
}


void Relay::turn(bool state){
	digitalWrite(_pin, state);
}

void Relay::on(){
	turn(1);
}

void Relay::off(){
	turn(0);
}

bool Relay::get_state(){
	return digitalRead(_pin);
}


		
bool Relay::get_reversed(){
	return _reversed;
}
		
		
void Relay::set_reversed(bool is_reversed){
	_reversed = is_reversed;
}
