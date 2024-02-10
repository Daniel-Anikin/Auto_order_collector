#ifndef ___DC_MOTOR_H___
#define ___DC_MOTOR_H___


#include "imotor.h"

class DC_Motor : public IMotor
{
public:
    DC_Motor();
    DC_Motor(byte dirPin, byte speedPin);
	DC_Motor(byte dirPin, byte speedPin, bool reversed);
	~DC_Motor();

    void set_speed(int speed) override;
	int get_speed() override;
	void set_reversed(bool reversed) override;
	bool get_reversed() override;
	void stop() override;
	void attach(byte dirPin, byte speedPin);
	void detach();
	bool is_attached();

private:
	byte _dirPin;
	byte _speedPin;
	bool _attached;
};



#endif