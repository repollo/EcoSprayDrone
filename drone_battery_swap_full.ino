#include <ezButton.h>
//to save pins I'm putting all direction pins together on breadboard and controlling via pin 2. since motors are "off" except for 1 place in code running it's ok. Means I can use ardu uno instead of mega
// initialize pins
int generic_dir = 2;
int motor2_dir = 4;
int dronepush_pwm = 3;
//int batPush_dir = 7; 
int batPush_pwm = 6;
//int batRetrieve_dir = 8;
int batRetrieve_pwm = 9;
//int upDown_dir = 4;
int upDown_pwm = 5;
//int landing2_dir = 12;
int landing2_pwm = 10;
ezButton landing2_limit(13);
int landing1a_pwm = 11;
int landing1b_pwm = A0;
//int pump_pwm = A1;
ezButton landing1b_limit = 12;
ezButton landing1a_limit = 8;

// the setup function runs once when you press reset or power the board
void setup() 
{
  pinMode(generic_dir, OUTPUT); 
  pinMode(dronepush_pwm, OUTPUT);
  //pinMode(batPush_dir, OUTPUT); 
  pinMode(batPush_pwm, OUTPUT);
  //pinMode(batRetrieve_dir, OUTPUT); 
  pinMode(batRetrieve_pwm, OUTPUT);
  //pinMode(upDown_dir, OUTPUT); 
  pinMode(upDown_pwm, OUTPUT);
  //pinMode(landing2_dir, OUTPUT); 
  pinMode(landing2_pwm, OUTPUT);
  landing2_limit.setDebounceTime(10);
  landing1b_limit.setDebounceTime(10);
  landing1a_limit.setDebounceTime(10);
}

// the loop function runs over and over again forever
void loop() 
{ 
  landing2_limit.loop(); // start watching the limit switches
  landing1b_limit.loop();
  landing1a_limit.loop();
  //To do: get 100rpm lander 1a/b and halve times.
  moveMotorLimit2(motor2_dir, landing1a_pwm, 250, landing1b_pwm, 255, 1200000, 0, landing1a_limit, landing1b_limit); //pull in drone lander1 retrieve arm.  0 = pull in.  1 = push back
  moveMotorLimit(generic_dir, landing2_pwm, 650000, 0, landing2_limit); //pull in drone lander2 retrieve arm
  //make push out of arm 1 happen during the rest of the battery swap (saves lots of time).   565000 (exclude arm 1) + 600000 arm1 = 1165000 which is perfect! Just divide moveMotor2 into 2 (start/stop)
  moveMotor2Start(motor2_dir, landing1a_pwm, 250, landing1b_pwm, 255, 1150000, 1); //push out big drone lander arm 
  moveMotor(generic_dir, batRetrieve_pwm, 68500, 1); //push out battery retrieve arm 
  moveMotor(generic_dir, batPush_pwm, 76000, 1); //push out battery from drone
  moveMotor(generic_dir, batPush_pwm, 78000, 0); //pull back in battery pusher arm to neutral
  moveMotor(generic_dir, batRetrieve_pwm, 30000, 0); //pull battery retrieve arm back in a bit to center battery on charge port
  //TO DO: fill up tank
  moveMotor(generic_dir, upDown_pwm, 21000, 1); //push up battery cage
  moveMotor(generic_dir, batPush_pwm, 39000, 1); //install battery in drone
  moveMotor(generic_dir, batPush_pwm, 40000, 0); //pull back battery pusher arm to neutral  
  moveMotor(generic_dir, upDown_pwm, 21000, 0); //let down battery cage 
  moveMotor(generic_dir, batRetrieve_pwm, 37000, 0); //pull battery retrieve arm back in to retrieve spent battery
  moveMotor(generic_dir, batRetrieve_pwm, 500, 1); //push arm out a bit so as not to lift battery during charge
  moveMotor(generic_dir, landing2_pwm, 600000, 1); //push out drone lander2 retrieve arm
  moveMotor(generic_dir, dronepush_pwm, 76000, 1); //push out drone for takeoff
  moveMotor(generic_dir, dronepush_pwm, 78000, 0); //retrieve drone pusher arm
  moveMotor2Stop(landing1a_pwm, landing1b_pwm); // stop motor 1 arm moving, should be nearly done
  exit(0);
}


int moveMotor(int dir_pin, int pwm_pin, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm_pin, 255); //start motor movin
  delay(milliseconds); //delay for duration desired
  analogWrite(pwm_pin, 0); //stop motor movin
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  delay(milliseconds); //delay for duration desired
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2Start(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2Stop(int pwm1_pin, int pwm2_pin){
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotorLimit(int dir_pin, int pwm_pin, long milliseconds, int dir, ezButton limitSwitch){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  long startMillis = millis(); //get initial time
  long currentMillis = millis();
  limitSwitch.loop();
  int initState = limitSwitch.getState(); //get initial state
  int curState = limitSwitch.getState(); 
  analogWrite(pwm_pin, 255); //start motor moving
  //turn on motor until the milliseconds are pass OR the limit switch is hit
  while((currentMillis - startMillis <= milliseconds) && (initState == curState)) {
    limitSwitch.loop();
    curState = limitSwitch.getState();
    currentMillis = millis();
  }
  analogWrite(pwm_pin, 0); //stop motor moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotorLimit2(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir, ezButton limitSwitch1, ezButton limitSwitch2){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  long startMillis = millis(); //get initial time
  long currentMillis = millis();
  limitSwitch1.loop();
  limitSwitch2.loop();
  int initState1 = limitSwitch1.getState(); //get initial state 1
  int curState1 = limitSwitch1.getState(); //get cur state 1
  int initState2 = limitSwitch2.getState(); //get initial state 2
  int curState2 = limitSwitch2.getState(); //get cur state 2
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  //turn on motors until the milliseconds are passed OR the limit switches are hit
  int counterLimit1 = 0;
  int counterLimit2 = 0;
  while((currentMillis - startMillis <= milliseconds) && ((counterLimit1 == 0) || (counterLimit2 == 0))) {
    limitSwitch1.loop();
    limitSwitch2.loop();
    curState1 = limitSwitch1.getState();
    curState2 = limitSwitch2.getState();
    if(initState1 != curState1){
      analogWrite(pwm1_pin, 0); //limit reached, stop motor1 moving
      counterLimit1 = 1;
    }
    if(initState2 != curState2){
      analogWrite(pwm2_pin, 0); //limit reached, stop motor2 moving
      counterLimit2 = 1;
    }
    currentMillis = millis();
  }
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}#include <ezButton.h>
//to save pins I'm putting all direction pins together on breadboard and controlling via pin 2. since motors are "off" except for 1 place in code running it's ok. Means I can use ardu uno instead of mega
// initialize pins
int generic_dir = 2;
int motor2_dir = 4;
int dronepush_pwm = 3;
//int batPush_dir = 7; 
int batPush_pwm = 6;
//int batRetrieve_dir = 8;
int batRetrieve_pwm = 9;
//int upDown_dir = 4;
int upDown_pwm = 5;
//int landing2_dir = 12;
int landing2_pwm = 10;
ezButton landing2_limit(13);
int landing1a_pwm = 11;
int landing1b_pwm = A0;
//int pump_pwm = A1;
ezButton landing1b_limit = 12;
ezButton landing1a_limit = 8;

// the setup function runs once when you press reset or power the board
void setup() 
{
  pinMode(generic_dir, OUTPUT); 
  pinMode(dronepush_pwm, OUTPUT);
  //pinMode(batPush_dir, OUTPUT); 
  pinMode(batPush_pwm, OUTPUT);
  //pinMode(batRetrieve_dir, OUTPUT); 
  pinMode(batRetrieve_pwm, OUTPUT);
  //pinMode(upDown_dir, OUTPUT); 
  pinMode(upDown_pwm, OUTPUT);
  //pinMode(landing2_dir, OUTPUT); 
  pinMode(landing2_pwm, OUTPUT);
  landing2_limit.setDebounceTime(10);
  landing1b_limit.setDebounceTime(10);
  landing1a_limit.setDebounceTime(10);
}

// the loop function runs over and over again forever
void loop() 
{ 
  landing2_limit.loop(); // start watching the limit switches
  landing1b_limit.loop();
  landing1a_limit.loop();
  //To do: get 100rpm lander 1a/b and halve times.
  moveMotorLimit2(motor2_dir, landing1a_pwm, 250, landing1b_pwm, 255, 1200000, 0, landing1a_limit, landing1b_limit); //pull in drone lander1 retrieve arm.  0 = pull in.  1 = push back
  moveMotorLimit(generic_dir, landing2_pwm, 650000, 0, landing2_limit); //pull in drone lander2 retrieve arm
  //make push out of arm 1 happen during the rest of the battery swap (saves lots of time).   565000 (exclude arm 1) + 600000 arm1 = 1165000 which is perfect! Just divide moveMotor2 into 2 (start/stop)
  moveMotor2Start(motor2_dir, landing1a_pwm, 250, landing1b_pwm, 255, 1150000, 1); //push out big drone lander arm 
  moveMotor(generic_dir, batRetrieve_pwm, 68500, 1); //push out battery retrieve arm 
  moveMotor(generic_dir, batPush_pwm, 76000, 1); //push out battery from drone
  moveMotor(generic_dir, batPush_pwm, 78000, 0); //pull back in battery pusher arm to neutral
  moveMotor(generic_dir, batRetrieve_pwm, 30000, 0); //pull battery retrieve arm back in a bit to center battery on charge port
  //TO DO: fill up tank
  moveMotor(generic_dir, upDown_pwm, 21000, 1); //push up battery cage
  moveMotor(generic_dir, batPush_pwm, 39000, 1); //install battery in drone
  moveMotor(generic_dir, batPush_pwm, 40000, 0); //pull back battery pusher arm to neutral  
  moveMotor(generic_dir, upDown_pwm, 21000, 0); //let down battery cage 
  moveMotor(generic_dir, batRetrieve_pwm, 37000, 0); //pull battery retrieve arm back in to retrieve spent battery
  moveMotor(generic_dir, batRetrieve_pwm, 500, 1); //push arm out a bit so as not to lift battery during charge
  moveMotor(generic_dir, landing2_pwm, 600000, 1); //push out drone lander2 retrieve arm
  moveMotor(generic_dir, dronepush_pwm, 76000, 1); //push out drone for takeoff
  moveMotor(generic_dir, dronepush_pwm, 78000, 0); //retrieve drone pusher arm
  moveMotor2Stop(landing1a_pwm, landing1b_pwm); // stop motor 1 arm moving, should be nearly done
  exit(0);
}


int moveMotor(int dir_pin, int pwm_pin, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm_pin, 255); //start motor movin
  delay(milliseconds); //delay for duration desired
  analogWrite(pwm_pin, 0); //stop motor movin
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  delay(milliseconds); //delay for duration desired
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2Start(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotor2Stop(int pwm1_pin, int pwm2_pin){
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotorLimit(int dir_pin, int pwm_pin, long milliseconds, int dir, ezButton limitSwitch){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  long startMillis = millis(); //get initial time
  long currentMillis = millis();
  limitSwitch.loop();
  int initState = limitSwitch.getState(); //get initial state
  int curState = limitSwitch.getState(); 
  analogWrite(pwm_pin, 255); //start motor moving
  //turn on motor until the milliseconds are pass OR the limit switch is hit
  while((currentMillis - startMillis <= milliseconds) && (initState == curState)) {
    limitSwitch.loop();
    curState = limitSwitch.getState();
    currentMillis = millis();
  }
  analogWrite(pwm_pin, 0); //stop motor moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}

int moveMotorLimit2(int dir_pin, int pwm1_pin, int pwm1_speed, int pwm2_pin, int pwm2_speed, long milliseconds, int dir, ezButton limitSwitch1, ezButton limitSwitch2){
  //set motor direction
  if (dir == 1) {
    digitalWrite(dir_pin, HIGH);
  }
  else {
    digitalWrite(dir_pin, LOW);
  }
  long startMillis = millis(); //get initial time
  long currentMillis = millis();
  limitSwitch1.loop();
  limitSwitch2.loop();
  int initState1 = limitSwitch1.getState(); //get initial state 1
  int curState1 = limitSwitch1.getState(); //get cur state 1
  int initState2 = limitSwitch2.getState(); //get initial state 2
  int curState2 = limitSwitch2.getState(); //get cur state 2
  analogWrite(pwm1_pin, pwm1_speed); //start motor1 moving
  analogWrite(pwm2_pin, pwm2_speed); //start motor2 moving
  //turn on motors until the milliseconds are passed OR the limit switches are hit
  int counterLimit1 = 0;
  int counterLimit2 = 0;
  while((currentMillis - startMillis <= milliseconds) && ((counterLimit1 == 0) || (counterLimit2 == 0))) {
    limitSwitch1.loop();
    limitSwitch2.loop();
    curState1 = limitSwitch1.getState();
    curState2 = limitSwitch2.getState();
    if(initState1 != curState1){
      analogWrite(pwm1_pin, 0); //limit reached, stop motor1 moving
      counterLimit1 = 1;
    }
    if(initState2 != curState2){
      analogWrite(pwm2_pin, 0); //limit reached, stop motor2 moving
      counterLimit2 = 1;
    }
    currentMillis = millis();
  }
  analogWrite(pwm1_pin, 0); //stop motor1 moving
  analogWrite(pwm2_pin, 0); //stop motor2 moving
  delay(1000); // let the power supply and motors sit idle for a moment
  return 1;
}