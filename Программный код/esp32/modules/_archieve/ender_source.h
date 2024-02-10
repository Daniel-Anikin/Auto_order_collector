#ifndef ___ENDER___
#define ___ENDER___


#define DEFAULT_PIN_MODE 2 //INPUT_PULLUP

class Ender(){
	public:
		Ender(){
			this->_attached = false;
			this->_mode = DEFAULT_PIN_MODE;
			this->_reversed = true;
		}
		
		Ender(byte pin){
			this->_mode = DEFAULT_PIN_MODE;
			this->_reversed = true;
			this->attach(pin);
		}
		
		Ender(byte pin, int mode, bool reversed){
			this->_mode = mode;
			this->_reversed = reversed;
			this->attach(pin);
		}
		
		~Ender(){}
		
		void attach(byte pin){
			this->_pin = pin;
			pinMode(this->_pin, this->_mode);
		}
		
		void detach(){
			this->_attached = false;
		}	
		
		bool get_raw(){
			return this->_attached ? digitalRead(this->_pin) : 0;
		}
		
		bool check(){
			return this->_attached ? (this->get_raw() xor this->_reversed) : 0;
		}
		
		void set_mode(bool mode){
			this->_mode = mode;
			this->attach(this->_pin);
		}
		
		void set_reversed(bool reversed){
			this->_reversed = reversed;
		}
		
		bool is_attached(){
			return this->_attached;
		}
	private:
		byte _pin;
		int _mode;
		bool _reversed;
		bool _attached;
};


#endif
