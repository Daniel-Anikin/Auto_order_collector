#ifndef ___IMOTOR_H___
#define ___IMOTOR_H___


class IMotor
{
protected:
    virtual ~IMotor() = default; // защищенный деструктор
    IMotor& operator=(const IMotor&) = default; // запрет присваивания

public:
    virtual void set_speed(int speed) = 0;
	virtual int get_speed() = 0;
	virtual void set_reversed(bool reversed) = 0;
	virtual bool get_reversed() = 0;
	virtual void stop() = 0;

private:
	bool _reversed;
	int  _speed;
};


#endif