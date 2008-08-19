CFLAGS=-g -Wall 
maxstream: Maxstream.c Maxstream.c
	gcc -lm -g -c -Wall Maxstream.c -o Maxstream.o
	gcc -lm -g -c -Wall port.c -o port.o
	gcc -lm -g -c -Wall Zfunctions.c -o Zfunctions.o
	gcc -lm -g port.o Maxstream.o Zfunctions.o -o Maxstream
