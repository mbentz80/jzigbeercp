#include <stdio.h>
#include <stdlib.h>
#include <string.h>   
#include <unistd.h>    
#include <errno.h>  
#include <sys/types.h>         
#include <sys/ipc.h> 
#include <sys/shm.h>  
//#include "port.h"       
#include "Zfunctions.h"  
  
#define SHM_SIZE = 1024    


     
int main(int argc, char *argv[]) 
{
  

  
	key_t key;    
	int shmid;  
	char *data;     
	int mode;    

    key = ftok("/home/Zeno/serial/Maxstream.c", 'R');
    shmid = shmget(key, 1024, 0644 | IPC_CREAT);
    data = shmat(shmid, (void *)0, 0);  
  
	int dataFlag; 
	char sCmd[254];   
	char sResult[254];  
	
	if (argc < 2 || argc > 2)
	{
		printf("Serial needs one parameter for the serial port\n");
		printf(" For Linux use 'adrserial 0' to connect to /dev/ttyS0\n");
		printf(" For Cygwin, use 'adrserial 0' to connect to COM1\n");
		return 0;
	} // end if
	printf("Type q to quit.\n\n");
	if (OpenPort(argv[1]) < 0) return 0;

   pid_t pid = fork();

 
   if (pid == 0)
   {  
      // Child process:     
	  // int j = 0;
	  //while (1){ 
		//ReadPort(sResult,254) > 0;
		//if (sResult[0]!='N' && j<254 && sResult[0]!=0x0d){
		//data[j] = sResult[0];
		//j++;    
		//}  
		//if (sResult[0]==0x0d){       
		//	j=0;
		//	printf("%s\n",data);    
		//}    

	 // }  
   }
   else if (pid > 0)
   {    
      // Parent process:
	   while (1) {  
		printf("?:");
		gets(sCmd);
		printf("");//Do not remove this line or the system crashes

		
		ATCommand(1,sCmd);//sCmd);
		//printf("Say goodbye to her for me \n\r");
		//printf("your mom\r\n");
	   }  
   }
 

   else
   {     
      // Error:
      fprintf(stderr, "can't fork, error %d\n", errno);
      exit(1);
   }
}














