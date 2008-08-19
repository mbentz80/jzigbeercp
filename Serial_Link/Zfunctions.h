
void char2Hex(char message);
void hex2Ascii(int message);
void strn2Hex(char* data);
void hex2Strn(char* data, int length);
void modemStatus(int status);
void ATCommand(int frameID, char* command);
void ATCommandQ(int frameID, char* command);
void RemoteATCommand(int frameID, char* destAddr, char* netAddr, char* comOp, char* command);
void Transmit(int frameID, char* destAddr, char* netAddr, char* hops,char* mCast, char* data);