#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "port.h"  




void sendFrames(char* Data,int length) {
	char *charPtr0;
	char *charPtr1;
	char *charPtr2;
	char *charPtr3;
	char checkSum = 0xFF;
	
	char *frameData;//[length];
	
	
	
/*Parses data into transmission string frameData*/
	
	//Set Length Pointer
	char* lengthPtr = (char*) (& length);
	//lengthPtr= (char*) (& length);  
	char data[length+4];
	
	frameData = & data;
	// Read headers into frameData
	frameData[0] =  0x7E;
	frameData[2] = (char) (lengthPtr[0]);
	frameData[1] = (char) (lengthPtr[1]); 

	
	//Read Data into frameData
	int w=0;  
	for(w=0;w<length;w++) {
	frameData[3+w] = (char) Data[w];
	checkSum = checkSum - frameData[2+w];
	}

	//Read checksum into frameData
	frameData[3+length] =  (char) checkSum;

	//Read null into frameData
	frameData[4+length] = 0x00;

/*Transmits string*/
WritePort(frameData,length+4);
//printf("Your father as well\n\r");
//memset(frameData, 0, length +5);
}


int char2Hex(char message){
char j;
int value;

	value = (int) message;
	printf("before edit%i\n",value);
	if ((value > 47) & (value < 58)){
	
		value = value - 0x30;
	
	}
	else if ((value > 64) & (value < 91)) {
		value = value - 0x37;
	}
	printf("after edit:%i\n",value);
	return  (char) value;
}

char hex2Ascii(int message){
int value;
	value = (int) message;
	if ((value >= 0) & (value < 10)){
		value = value + 0x30;
	}
	else if ((value > 9) & (value < 17)) {
		value = value + 0x36;
	}
	else //error
	
	return (char) value;
	}
  
char* strn2Hex(char* data) {
int j;
char* output;
int temp;
int length = strlen(data);
char tempData[length/2];
output = (char*) & tempData;


for (j=0+2;j<=length/2+2;j=j+2){
	temp = (char2Hex(data[j])*16 + char2Hex(data[j+1]));
	output[j/2] = (char) temp;
	}
	return output;
}

char* hex2Strn(char* data, int length){
int j;
char* output;
int temp;
for (j=0;j<length*2;j=j+2){
	output[j] =  (hex2Ascii(floor(((int) data[j/2])/16)));
	output[j+1] =  (hex2Ascii(data[j/2] -output[j]*16));
	}
}



	

 
 
 
 

// *
 //0x8A://Modem Status
void modemStatus(int status){
	char *messageData;
	char data[2];
	messageData = &data;
	messageData[0] = 0x8A;
	messageData[1] = (char) status;
	sendFrames(messageData,2);    
}

//0x08://AT Command
void ATCommand(int frameID, char* command){
	char *messageData;
	
	char *tempString = strn2Hex(command);
	int dataLength = strlen(command)/2-1;
	char data[dataLength + 4];
	messageData = & (data);
	
	messageData[0] = 0x08;
	messageData[1] = (char) frameID;
	
	messageData[2] = (char) command[0];
	messageData[3] = (char) command[1];
	
	int j;
	for (j=0;j<dataLength;j++){
	messageData[j+4] = tempString[j+1];
	}
	
	//runs frame packing function
	sendFrames(messageData,dataLength+4); 
}

//0x09://AT Queue Parameter Value
void ATCommandQ(int frameID, char* command){
	char *messageData;
	char *tempString = strn2Hex(command);
	int dataLength = strlen(command)/2-1;
	
	messageData[0] = 0x08;
	messageData[1] = (char) frameID;
	
	messageData[2] = (char) command[0];
	messageData[3] = (char) command[1];
	
	
	
	int j;
	for (j=0;j<dataLength;j++){
	messageData[j+4] = tempString[j+1];
	}
	
	sendFrames(messageData,dataLength+4);
}


//0x17://Remote Command Request
void RemoteATCommand(int frameID, char* destAddr, char* netAddr, char* comOp, char* command){
	char *messageData;
	char *tempString1 = strn2Hex(destAddr);
	char *tempString2 = strn2Hex(netAddr);
	char *tempString3 = strn2Hex(comOp);
	char *tempString4 = strn2Hex(command);
	int length = strlen(command)/2-1;
	int j;
	
	messageData[0] = 0x17;
	messageData[1] = (char) frameID;

	

		
	for (j=2;j<10;j++){
		messageData[j] = tempString1[j-2];
	}
	
	for (j=10;j<12;j++){
		messageData[j] = tempString2[j-10];
	}	
	

	messageData[12] = tempString3[0];
	messageData[13] = (char) command[0];
	messageData[14] = (char) command[1];
	
	for (j=0;j<length;j++){
	messageData[j+15] = tempString4[j+1];
	}

	sendFrames(messageData,length+15);
} 
  
 //0x10://ZigBee Transmit Request
void Transmit(int frameID, char* destAddr, char* netAddr, char* hops,char* mCast, char* data){
	char *messageData;
	char *feedback;	
	char *tempString1 = strn2Hex(destAddr);
	char *tempString2 = strn2Hex(netAddr);
	char *tempString3 = strn2Hex(hops);
	char *tempString4 = strn2Hex(mCast);
	char *tempString5 = strn2Hex(data);
	int dataLength = strlen(data)/2;
	int j;
	
	messageData[0] = 0x10;
	messageData[1] = (char) frameID;
	
	for (j=2;j<10;j++){
		messageData[j] = tempString1[j-2];
	}
	
	for (j=10;j<12;j++){
		messageData[j] = tempString2[j-10];
	}	
	

	messageData[12] = tempString3[0];
	messageData[13] = tempString4[0];
	
	for (j=0;j<dataLength;j++){
	messageData[j+14] = tempString1[j];
	}

	sendFrames(messageData,dataLength+14);
}





















 
  

  
  
  
