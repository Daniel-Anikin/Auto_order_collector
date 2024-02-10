#include <GCodeParser.h>

#define UART_SPEED 115200

void setup(){
	Serial.begin(UART_SPEED);
}


bool logs_on = true;

bool get_logSt(){
	return logs_on;
}

void set_logsSt(bool st){
	logs_on = st;
}

void log(String msg){
	if (get_logSt()){
		//Serial.print(millis());
		//Serial.print(" ");
		Serial.print(msg);
	}
}



GCodeParser GCode = GCodeParser();


void g0(){
	log("> g0()");
}

void g1(){
	log("> g1()");
	
}

void g4(){
	log("> g4()");
}

void g28(){
	log("> g28()");
}

void m15(){
	log("> m15() - Enable logs");
	set_logsSt(true);
}

void m16(){
	log("> m16() - disable logs");
	set_logsSt(false);
}

void m17(){
	log("> m17()");
}

void m18(){
	log("> m18()");
}

void m112(){
	log("> m112()");
}

void m114(){
	log("> m114()");
}

void m115(){
	log("> m115()");
}

void m119(){
	log("> m119()");
}



use gcode_func_t = void (*)();

typedef struct{
	int name;
	gcode_func_t handler;
	//void (*func)();
} gcode_func_t;


#define	G_FAST_MOVE_CMD 	0
#define G_SLOW_MOVE_CMD 	1
#define G_WAIT				4	 
#define G_HOME_CMD 			28

#define M_LOG_ON_CMD			15
#define M_LOG_OFF_CMD			16
#define M_MOTORS_ON_CMD			17
#define M_MOTORS_OFF_CMD		18
#define M_EMERGENCY_STOP_CMD	112
#define M_GET_POSITION_CMD		114
#define M_GET_VERSION_CMD		115
#define M_GET_ENDERS_ST_CMD		119

#define G_CMD_NUM 4
#define M_CMD_NUM 8

gcode_func_t g_functions[] = {
	{G_FAST_MOVE_CMD, g0},
	{G_SLOW_MOVE_CMD, g1},
	{G_WAIT, g4},
	{G_HOME_CMD, g28}
};

gcode_func_t m_functions[] = {
	{M_LOG_ON_CMD, m15},
	{M_LOG_OFF_CMD, m16},
	{M_MOTORS_ON_CMD, m17},
	{M_MOTORS_OFF_CMD, m18},
	{M_EMERGENCY_STOP_CMD, m112},
	{M_GET_POSITION_CMD, m114},
	{M_GET_VERSION_CMD, m115},
	{M_GET_ENDERS_ST_CMD, m119}
};





bool collect_gcode_cmd(){
	while (Serial.available() > 0){
		if (GCode.AddCharToLine(Serial.read())){
			return 1;
		}
	}
	return 0;
}


void G(int g_cmd_code){
	log((String)"G" + String(g_cmd_code) + '\n');
	
	int index = -1;
	for (int i=0; i < G_CMD_NUM; i++){
		if (g_cmd_code == g_functions[i].name){
			log(String("Launch G") + String(g_cmd_code));
			index = i;
			break;
		}
	}
	if (index == -1){
		log("Unknown G command");
		return;
	}
	g_functions[index].func();
}


void M(int m_cmd_code){
	log("M" + String(m_cmd_code) + '\n');
	
	int index = -1;
	for (int i=0; i < M_CMD_NUM; i++){
		if (m_cmd_code == m_functions[i].name){
			log(String("Launch M") + String(m_cmd_code));
			index = i;
			break;
		}
	}
	if (index == -1){
		log("Unknown M command");
		return;
	}
	m_functions[index].func();
}


void parse_gcode_task(){
	if (collect_gcode_cmd()){
		log("Line was received: ");
		GCode.ParseLine();
		log(GCode.line); log("\n");
		GCode.RemoveCommentSeparators();
		log("Comment(s): ");
		log(GCode.comments); log("\n");
	
		if (GCode.HasWord('G')){
			log("Process cmd: ");
			int val = (int)GCode.GetWordValue('G');
			G(val);
		}
		else if (GCode.HasWord('M')){
			log("Process cmd: ");
			int val = (int)GCode.GetWordValue('M');
			M(val);
		}
		else{
			log("Unknown gcode command!");
		}
	}
	else{
		log("No data");
	}
}



void loop(){ 
  parse_gcode_task();
  delay(50);
}