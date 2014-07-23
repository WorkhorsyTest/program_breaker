
#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>
#include "main.h"

int main() {
	int x = 88;
	int y = 77;
	int z = x + y;
	printf("z: %d\n", z);

	char a = 2;
	signed char b = 2;
	unsigned char c = 2;

	short d = -4;
	unsigned short e = 4;

	int f = -5;
	unsigned int g = 5;

	long h = -6;
	unsigned long i = 6;

	long long j = -7;
	unsigned long long int k = 8;

	bool l = false;

	float m = 2.5;
	double n = 3.5;
	long double o = 4.5;

	size_t p = 4;
	ptrdiff_t q = 3;

	int r[] = {1, 2, 3};
	char name[] = "example name";

	blah();

	return 0;
}

