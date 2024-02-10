#ifndef ___RELAY_H___
#define ___RELAY_H___

#define ON 1
#define OFF 0 

class Relay{
	public:
		Relay();
		Relay(byte pin);
		Relay(byte pin, bool is_reversed);
		~Relay();
		
		void attach(byte pin);
		void detach();
		bool is_attached();
		
		void turn(bool state);
		void on();
		void off();
		bool get_state();
		
		bool get_reversed();	
		void set_reversed(bool is_reversed);
		
	private:
		byte _pin;
		bool _reversed;
		bool _attached;
};


#endif
