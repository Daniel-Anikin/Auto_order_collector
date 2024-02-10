#ifndef ___ENDER_H___
#define ___ENDER_H___


#define DEFAULT_PIN_MODE 2 //INPUT_PULLUP

class Ender{
	public:
		Ender();
		Ender(byte pin);
		Ender(byte pin, int mode, bool is_reversed);
		~Ender();
		void attach(byte pin);
		void detach();
		bool get_raw();
		bool check();
		void set_mode(bool mode);
		void set_reversed(bool is_reversed);
		bool is_attached();
	private:
		byte _pin;
		int _mode;
		bool _reversed;
		bool _attached;
};


#endif
