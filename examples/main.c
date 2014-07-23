

#include <stdio.h>
#include <string.h>
#include <stdbool.h>


size_t diff(size_t a, size_t b) {
	if(a > b) {
		return a - b;
	} else {
		return b -a;
	}
}

int main() {
	const size_t BUFFER_SIZE = 11;
	char buffer[BUFFER_SIZE];
	bool is_valid = false;
	//char input[] = "012";
	memset(buffer, ' ', BUFFER_SIZE);
	buffer[BUFFER_SIZE-1] = '\0';

	printf("&buffer: %p\n", &buffer);
	printf("&is_valid: %p\n", &is_valid);
	printf("diff: %u\n", diff((size_t)&buffer, (size_t)&is_valid));
	printf("%s\n", "");

	//printf("input: '%s', sizeof:%d, strlen:%d\n", input, sizeof(input), strlen(input));
	printf("buffer: '%s', sizeof:%d, strlen:%d\n", buffer, sizeof(buffer), strlen(buffer));
	printf("is_valid: '%d'\n", is_valid);
	printf("%s\n", "");

	fgets(buffer, 255, stdin);
	//strncpy(buffer, input, 11);

	//printf("input: '%s', sizeof:%d, strlen:%d\n", input, sizeof(input), strlen(input));
	printf("buffer: '%s', sizeof:%d, strlen:%d\n", buffer, sizeof(buffer), strlen(buffer));
	printf("is_valid: '%d'\n", is_valid);
	printf("%s\n", "");

	if(strcmp(buffer, "password") == 0) {
		is_valid = true;
	}

	if(is_valid) {
		printf("%s\n", "Welcome root!");
	} else {
		printf("%s\n", "Invalid password!");
	}

	return 0;
}

