#ifndef ___LINEARPUMP_H___
#define ___LINEAR_PUMP_H___

#include "ender.h"
#include "motor.h"

#define IN 			0
#define OUT 		1
#define STOPPED 	2

class LinearPump
{
	public:
		LinearPump(Motor mot, Ender upEnder, Ender downEnder);
		void stPump(bool dir);
		void stPumpIn();
		void stPumpOut();
		
		void pump(bool dir);
		void pumpIn();
		void pumpOut();
		
		void stop();
		bool get_EnderSt(bool dir);
		bool get_upEnderSt();
		bool get_downEnderSt();
		void set_speed(int speed);
		bool tick();
	private:
		byte _state;
		Ender _upEnder;
		Ender _downEnder;
		Motor _motor;
};


#endif