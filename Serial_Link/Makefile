CFLAGS=-g -Wall 
maxstream: Maxstream.c Maxstream.c
	gcc -g -c -Wall Maxstream.c -o Maxstream.o
	gcc -g -c -Wall port.c -o port.o
	gcc -g -c -wall Zfunctions.c -o Zfunctions.o
	gcc -g port.o Maxstream.o Zfunctions.o -o Maxstream
