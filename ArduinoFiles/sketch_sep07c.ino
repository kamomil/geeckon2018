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

void setup()
{
  Serial.begin(9600);
  DDRD = B11111111; // set PORTD (digital 7~0) to outputs
}

void setPin(int outputPin)
// function to select pin on 74HC4067
{
  PORTD = controlPins[outputPin];
}

char EMPTY = 0;
char OCCUPIED = 1;

void loop()
{
    Serial.write('S');
    for (int i = 0; i < 4; i++){
      for (int j = 0; j < 4; j++)
      { 
        setPin(j); // choose an input pin on the 74HC4067
        muxValues[i,j]=analogRead(i); // read the vlaue on that pin and store in array
       
        if (muxValues[i] >= 400)
        {
          Serial.write(EMPTY);
        }
        else if (muxValues[i] < 400)
        {
          Serial.write(OCCUPIED);
          }
      }
    }
     Serial.write('E');

  /*// display captured data
  displayData();*/
  delay(1000); 
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
