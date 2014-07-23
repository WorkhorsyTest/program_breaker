

all: clean
	gcc -g -O0 -std=c99 main.c -omain

clean:
	rm -f main

