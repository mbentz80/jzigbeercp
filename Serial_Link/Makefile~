CFLAGS=-g -Wall 
maxstream: maxstream.c maxstream.c
	gcc -g -c -Wall maxstream.c -o maxstream.o
	gcc -g -c -Wall port.c -o port.o
	gcc -g -c -wall Zfunctions.c -o Zfunctions.o
	gcc -g port.o maxstream.o Zfunctions.o -o maxstream
