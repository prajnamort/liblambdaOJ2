#include <stdio.h>

int a[999999];

int main()
{
	int i;
	for(i = 0; i < 999999; i++)
		a[i] = i;
	return 0;
}
