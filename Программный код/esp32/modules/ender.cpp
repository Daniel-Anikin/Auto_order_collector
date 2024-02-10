#include "ender.h"


Ender::Ender()
	: _attached(false)
	, _mode(DEFAULT_PIN_MODE)
	, _reversed(true)
{
	
}
		
Ender::Ender(byte pin)
	: _mode(DEFAULT_PIN_MODE)
	, _reversed(true)
{
	attach(pin);
}
		
Ender::Ender(byte pin, int mode, bool is_reversed)
	: _mode(mode);
	, _reversed(is_reversed)
{
	attach(pin);
}
		
void Ender::attach(byte pin){
	_pin = pin;
	pinMode(_pin, _mode);
}
		
void Ender::detach(){
	_attached = false;
}	
		`
bool Ender::get_raw(){
	return _attached ? digitalRead(_pin) : 0;
}
		
bool Ender::check(){
	return _attached ? (get_raw() xor _reversed) : 0;
}
		
void Ender::set_mode(bool mode){
	_mode = mode;
	attach(_pin);
}
		
void Ender::set_reversed(bool is_reversed){
	_reversed = is_reversed;
}
		
bool Ender::is_attached(){
	return _attached;
}
