// control pins output table in array form
// see truth table on page 2 of TI 74HC4067 data sheet
// connect 74HC4067 S0~S3 to Arduino D7~D4 respectively
// connect 74HC4067 pin 1 to Arduino A0
byte controlPins[] = {B00000000, 
                  B10000000,
                  B01000000,
                  B11000000,
                  B00100000,
                  B10100000,
                  B01100000,
                  B11100000,
                  B00010000,
                  B10010000,
                  B01010000,
                  B11010000,
                  B00110000,
                  B10110000,
                  B01110000,
                  B11110000 }; 

// holds incoming values from 74HC4067                  
int muxValues[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

int chess_to_mux[64];
int chess_to_pin[64];

void setup()
{
  Serial.begin(9600);
  DDRD = B11111111; // set PORTD (digital 7~0) to outputs

  //////////mux 0////////////////

for(int i=0;i<16;i++){
chess_to_mux[i] = 0;
}
int k = 0;
for(int i=7;i>=0;i--){
  chess_to_pin[k] = i;
  k++;
}
for(int i=15;i>=8;i--){
  chess_to_pin[k] = i;
  k++;
}

//////////mux 1////////////////

for(int i=16;i<32;i++){
chess_to_mux[i] = 1;
}
k = 16;
for(int i=7;i>=0;i--){
  chess_to_pin[k] = i;
  k++;
}
for(int i=15;i>=8;i--){
  chess_to_pin[k] = i;
  k++;
}

//////////mux 2////////////////

for(int i=32;i<48;i++){
chess_to_mux[i] = 2;
}
k = 32;
for(int i=7;i>=0;i--){
  chess_to_pin[k] = i;
  k++;
}
for(int i=15;i>=8;i--){
  chess_to_pin[k] = i;
  k++;
}

//////////mux 3////////////////

for(int i=48;i<64;i++){
chess_to_mux[i] = 3;
}
k = 48;
for(int i=7;i>=0;i--){
  chess_to_pin[k] = i;
  k++;
}
for(int i=15;i>=8;i--){
  chess_to_pin[k] = i;
  k++;
}
}

void setPin(int outputPin)
// function to select pin on 74HC4067
{
  PORTD = controlPins[outputPin];
}

char EMPTY = 0;
char OCCUPIED = 1;


void displayDataBoard()
{
  for (int i = 0; i < 16; i++)
  {
    Serial.print(muxValues[i]);
    Serial.print(" , "); 
    if (i==7)
    {
      Serial.println();
      }
  }
  Serial.println();
}


void loop()
{
//    Serial.write('S');
//    for (int i = 0; i < 4; i++){
//      for (int j = 15; j >= 0; j--)
//      { 
//        setPin(j); // choose an input pin on the 74HC4067
//        muxValues[j]=analogRead(i); // read the vlaue on that pin and store in array
//       
//        if (muxValues[j] >= 400)
//        {
//          Serial.write(EMPTY);
//        }
//        else
//        {
//          Serial.write(OCCUPIED);
//          }
//      }
//    }
//     Serial.write('E');



Serial.write('S');
    for (int i = 0; i < 64; i++){
      int mux = chess_to_mux[i];
      int pin = chess_to_pin[i];
      
        setPin(pin); // choose an input pin on the 74HC4067
        int val = analogRead(mux); // read the vlaue on that pin and store in array
       
        if (val >= 200)
        {
          Serial.write(EMPTY);
        }
        else
        {
          Serial.write(OCCUPIED);
          }
      }
    
     Serial.write('E');
     
  // display captured data
  /*displayDataBoard();*/
  delay(5000); 
  /*
  // serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      char c = Serial.read();  //gets one byte from serial buffer
      if (c = "x")
      {
        
      }
      }
    }
  }*/
}
