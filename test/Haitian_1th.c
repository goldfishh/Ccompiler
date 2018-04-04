// test for struct and enum
#include <stdio.h>
enum Color {red, blue, green, black, purple, pink, grey};
struct Haitian{
	double height, width;
	double weight;
	double price;
	enum Color s;
	int stock;
};
int A;
double C;
void play(int A, double C){
	++A;
	C = C + A;
	printf("int: %d, double: %lf\n",A, C);
	return ;
}
int main(){
	struct Haitian HT_1th;
	HT_1th.height = 100.0;
	HT_1th.width = 50.0;
	HT_1th.weight = 10000000.0;
	HT_1th.s = 0;
	//HT_1th.s = pink;
	printf("%d\n",0);
	printf("OK!\n");
	A = 10;
	C = 8.88;
	play(A, C);
	
	return 0;
}
