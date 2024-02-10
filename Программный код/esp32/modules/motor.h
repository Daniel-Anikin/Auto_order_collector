#ifndef ___MOTOR_H___
#define ___MOTOR_H___


#include "IMotor.h"

class DC_Motor : public IMotor
{
public:
    DC_Motor();  // открытый конструктор
    DC_Motor(byte dirPin, byte speedPin);
	DC_Motor(byte dirPin, byte speedPin, bool reversed);
	~DC_Motor(); // открытый деструктор

    void set_speed(int speed) override;
	int get_speed() override;
	void set_reversed(bool reversed) override;
	bool get_reversed() override;
	void stop() override;
	void attach() override;
	void detach() override;

private:
	byte _dirPin;
	byte _speedPin
};



#endif