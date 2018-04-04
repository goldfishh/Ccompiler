#include <stdio.h>
int main(){
	int *A[10], B[10];
	int i;
	for(i = 1; i <= 5; ++i ){
		B[i] = i;
	}
	*A = B;
	printf("%d",*A+1);
	return 0;
} 
