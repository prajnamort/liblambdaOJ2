#include <stdio.h>
#include <stdlib.h>

int b[1024*1024*10];

int main()
{
	srand(0);
	int *a;
	int n = 1024* 1024* 10;
	a = (int*)malloc(n+1);

	int i;
	int best = -1;
	for (i = 0; i < n; i++) {
		a[i] = i;
		b[i] = rand();
		if (b[i] % 2) best = a[i];
		else best = i;
	}
	
	return best;
}
