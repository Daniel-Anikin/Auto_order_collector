#ifndef ___MSERVO_H___
#define ___MSERVO_H___


#include "imotor.h"
#include "Servo.h"

class SMotor : public IMotor
{
public:
    SMotor();  // открытый конструктор
    SMotor(byte pin);
	SMotor(byte pin, bool reversed);
	~SMotor();

    void set_speed(int speed) override;
	int get_speed() override;
	void set_reversed(bool reversed) override;
	bool get_reversed() override;
	void stop() override;
	void attach(byte pin);
	void attach(byte pin, int min, in max);
	void detach();
	bool is_attached();
	
private:
	byte _pin;
	Servo servo;
};



#endif