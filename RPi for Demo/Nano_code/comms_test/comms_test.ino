const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables for parsed data
char command_type_str[numChars] = {0};
char command_type = 0;
signed int newSpeeds[4];

boolean newData = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Format: <A,0,0,0,0>");
}

//===========

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        
        // change motor speeds here
        if (command_type == 'D'){
          Serial.println(newSpeeds[0]);
          Serial.println(newSpeeds[1]);
          Serial.println(newSpeeds[2]);
          Serial.println(newSpeeds[3]);
        } else if (command_type == 'H') {
          Serial.println(newSpeeds[0]);
        } else if (command_type == 'W') {
          Serial.println("wall");
        }
//        showParsedData();

        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(command_type_str, strtokIndx); // copy to string
    command_type = command_type_str[0];  
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    newSpeeds[0] = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[1] = atoi(strtokIndx);    

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[2] = atoi(strtokIndx);    

    strtokIndx = strtok(NULL, ","); 
    newSpeeds[3] = atoi(strtokIndx);     
}

//============

void showParsedData() {
    Serial.println(command_type);
    Serial.println(newSpeeds[0]);
    Serial.println(newSpeeds[1]);
    Serial.println(newSpeeds[2]);
    Serial.println(newSpeeds[3]);
}

