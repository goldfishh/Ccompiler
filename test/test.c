#include<stdio.h>

int main(int a,int b)
{
	int i,k;
	int j;
	int a;
	int *p;
	int **q;
	int a[2];
	char c;
	a[0]=0;
	a[1]=1;
	c='c';
	p=&a;
	q=&p;
	j=*p;
	i=**q;
	i = 1+(j-i)+a[1];
	j=2;
	if((i+1)/2==(j+1)/2)
	{
		j=3;
	}

	for(a=1;a<10;a++)
	{
		j=i;
	}
	while(a<10)
	{
		j=1;
		continue;
	}
	do
	{
		j=1;
	}
	while(a<10);
	
	
	scanf("%d %d",&i,&j);
	printf("i=%d,j=%d",i,i);
	return 0;
}