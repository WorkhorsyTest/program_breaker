

import std.stdio;

void print_stats(ref int[] nums) {
	writefln("sizeof: %d", nums.sizeof);
}

size_t sizeb(int[] array) {
	return array[0].sizeof * array.length;
}

int main() {
	int[] nums1 = [1, 2, 3, 4, 5, 6, 7];
	int[7] nums2 = [1, 2, 3, 4, 5, 6, 7];
	int[0] nums3;

	writefln("sizeof: %d", nums1.sizeb);
	writefln("sizeof: %d", nums2.sizeb);
	writefln("sizeof: %d, %d", nums3.sizeb, nums3.sizeof);

	return 0;
}

