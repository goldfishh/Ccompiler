helloworldfile = \
"""#include <stdio.h>
int main(){
	printf("Hello World!");
	return false;
}
"""
mergesortfile = \
"""#include <stdio.h>
#include <stdlib.h>
#define NUM 100
typedef int ElementType;
int False;
/* L = 左边起始位置, R = 右边起始位置, RightEnd = 右边终点位置*/
void Merge( ElementType A[], ElementType TmpA[], int L, int R, int RightEnd )
{ /* 将有序的A[L]~A[R-1]和A[R]~A[RightEnd]归并成一个有序序列 */
     int LeftEnd, NumElements, Tmp;
     int i;
      
     LeftEnd = R - 1; /* 左边终点位置 */
     Tmp = L;         /* 有序序列的起始位置 */
     NumElements = RightEnd - L + 1;
      
     while( L <= LeftEnd && R <= RightEnd ) {
         if ( A[L] <= A[R] ){
            TmpA[Tmp++] = A[L++]; /* 将左边元素复制到TmpA */
         }
         else{
            TmpA[Tmp++] = A[R++]; /* 将右边元素复制到TmpA */
         }
     }
 
     while( L <= LeftEnd ){
        TmpA[Tmp++] = A[L++]; /* 直接复制左边剩下的 */
     }
     while( R <= RightEnd ){
        TmpA[Tmp++] = A[R++]; /* 直接复制右边剩下的 */
     }

     for( i = 0; i < NumElements; i++, RightEnd -- ){
        A[RightEnd] = TmpA[RightEnd]; /* 将有序的TmpA[]复制回A[] */
     }
}

/* length = 当前有序子列的长度*/
void Merge_pass( ElementType A[], ElementType TmpA[], int N, int length )
{ /* 两两归并相邻有序子列 */
     int i, j;
       
     for ( i=0; i <= N-2*length; i = i+2*length ){
        Merge( A, TmpA, i, i+length, i+2*length-1 );
     }
     if ( i+length < N ){ /* 归并最后2个子列*/
        Merge( A, TmpA, i, i+length, N-1);
     }
     else{ /* 最后只剩1个子列*/
        for ( j = i; j < N; j++ ){
            TmpA[j] = A[j];
        }
     }
}
 
void Merge_Sort( ElementType A[], int N )
{ 
     int length; 
     ElementType *TmpA;
      
     length = 1; /* 初始化子序列长度*/
     TmpA = malloc( N * 4 );
     if ( TmpA != NULL ) {
          while( length < N ) {
              Merge_pass( A, TmpA, N, length );
              length = length * 2;
              Merge_pass( TmpA, A, N, length );
              length = length * 2;
          }
          free( TmpA );
     }
     else{
        printf( "空间不足" );
     }
}
//void initialization(int A, int B, int C, int D, int E, int F, int G, int H, int I, int J)
int main(){
	ElementType A[NUM]/* = {10,120,320,0,-5,42,-56,80,-81,7,100,1000,-1} */;
	Merge_Sort(A, 13);
	int i;
	for(i = 0; i < 13; i++){
		if(i == 0){
		    printf("%d", A[i]);
		}
		else{
		    printf(" %d", A[i]);
		}
	}
	return 0;
}
"""
tetrisfile = \
"""// 俄罗斯方块.cpp : 定义控制台应用程序的入口点。
//所有头文件以及定义
#include "stdio.h"
#include "time.h"
#include "windows.h"
#include "stdlib.h"
#include "conio.h"
void initialization();   //初始化函数
void round();            //定义回合函数，用于初始化一回合生成随机数等
void show();             //定义显示函数
void control();          //定义操控函数
void drop();             //定义掉落函数（控制掉落，消去等）
void del();              //定义去除函数，用于消去
void check();            //定义检查函数，用于检查当前横向移动是否合理
void jturn();            //定义左旋转函数
void kturn();            //定义右旋转函数
void scan();             //定义扫描函数，扫描当前旋转中心以及其他方块坐标
void current();          //定义直降函数
void losecheck();        //定义游戏总判断函数
char step;               //定义控制变量，暂定ad左右,s加速，j左转，k右转,l直降
int amovecheck;          //定义左移动检查变量，用于检测当前控制是否成立
int dmovecheck;          //定义右移动检查变量，用于检测当前控制是否成立
int smovecheck;          //定义下移动检查变量，用于检测当前控制是否成立
int count;               //定义计时变量，暂定每100us计数一次，每到100掉落
int roundcount;          //定义回合计数变量
int score;               //定义分数计数变量
int mode;                //定义游戏难度，暂定简单1s，普通0.6s，困难0.2s
int modetime;            //定义难度对应时间间隔
int board[20][10];       //定义棋盘20*10，右侧用于显示其他项（此变量仅用于判断）
int gamejudge;           //定义游戏判断变量，用于判断游戏结束等
int firstblock;          //定义第一个方块种类
int block;               //定义方块种类，7种（利用█或■堆叠）
int nextblock;           //定义下一方块种类，7种
int dropjudge;           //定义掉落判断变量，用于判断是否能够顺利掉落
int o[2];                //定义旋转中心，即值为3的坐标
int point[3][2];         //定义其他方块，即值为2的坐标
int turncheck;           //定义旋转检查变量
int temp;                //定义旋转临时变量
int min;                 //定义直降临时变量，用于记录降落最小距离
int mintemp;             //定义直降临时计算变量，用于临时记录降落距离
int currentflag;         //定义直降判断变量，判断最底层是否有方块
int conti;               //定义重开变量

						 //主函数
int main()
{
	initialization();
	Sleep(1000);
	round();
	return 0;
}

//初始化模块
void initialization()
{
	int i;
	int j;
	printf("俄罗斯方块\\\n");
	printf("请输入游戏难度\\\n1 简单   2 普通   3困难   4地狱\\\n");
	scanf("%d", &mode);
	if (mode == 1)
	{
		modetime = 100;
	}
	if (mode == 2)
	{
		modetime = 60;
	}
	if (mode == 3)
	{
		modetime = 20;
	}
	if (mode == 4)
	{
		modetime = 1;
	}
	for (i = 0; i < 20; ++i)
	{
		for (j = 0; j < 10; ++j)
		{
			board[i][j] = 0;
		}
	}
	srand(time(0));
	firstblock = rand() % 7 + 1;
	block = 0;
	nextblock = 0;
	gamejudge = 1;
	roundcount = 0;
	count = 0;
	dropjudge = 0;
	show();
}

//操作模块
void control()
{
	int i, j;
	Sleep(10);
	if (!kbhit())
	{
	}
	else
	{
		step = getch();
		if (step == 'a')
		{
			if (amovecheck != 0)
			{
				for (i = 19; i > -1; i--)
				{
					for (j = 1; j <10; ++j)
					{
						if (board[i][j] == 2)
						{
							board[i][j] = 0;
							board[i][j - 1] = 2;
						}
						if (board[i][j] == 3)
						{
							board[i][j] = 0;
							board[i][j - 1] = 3;
						}
					}
				}
			}
		}
		if (step == 'd')
		{
			if (dmovecheck != 0){
				for (i = 19; i > -1; i--)
				{
					for (j = 8; j > -1; j--)
					{
						if (board[i][j] == 2)
						{
							board[i][j] = 0;
							board[i][j + 1] = 2;
						}
						if (board[i][j] == 3)
						{
							board[i][j] = 0;
							board[i][j + 1] = 3;
						}
					}
				}				
			}
		}
		if (step == 's')
		{
			smovecheck = 1;
			for (i = 19; i > -1; i--)
			{
				for (j = 9; j > -1; j--)
				{
					if (board[i][j] == 2)
					{
						if (i == 19)
						{
							smovecheck = 0;
						}
					}
					if (board[i][j] == 3)
					{
						if (i == 19)
						{
							smovecheck = 0;
						}
					}
				}
			}
			if (smovecheck == 1)
			{
				for (i = 19; i > -1; i--)
				{
					for (j = 9; j > -1; j--)
					{
						if (board[i][j] == 2)
						{
							board[i + 1][j] = 2;
							board[i][j] = 0;
						}
						if (board[i][j] == 3)
						{
							board[i + 1][j] = 3;
							board[i][j] = 0;
						}
					}
				}
			}
		}
		if (step == 'j')
		{
			jturn();
		}
		if (step == 'k')
		{
			kturn();
		}
		if (step == 'l')
		{
			current();
			count = modetime;
		}
		show();
	}
}

//显示模块
void show()
{
	int i ,j;
	system("cls");
	for (i = 0; i < 20; ++i)
	{
		printf("|");
		for (j = 0; j < 10; ++j)
		{
			if (board[i][j] == 0)
			{
				printf("  ");
			}
			else
			{
				printf("█");
			}
		}
		printf("|");
		if (i == 0)
		{
			printf("          Round");
		}
		if (i == 1)
		{
			printf("          %d", roundcount);
		}
		if (i == 3)
		{
			printf("          Next Block");
		}
		if (i == 4)
		{
			if (nextblock == 1)
			{
				printf("          ██");
			}
			if (nextblock == 2)
			{
				printf("          ██");
			}
			if (nextblock == 3)
			{
				printf("            ██");
			}
			if (nextblock == 4)
			{
				printf("          █");
			}
			if (nextblock == 5)
			{
				printf("              █");
			}
			if (nextblock == 6)
			{
				printf("          ████");
			}
			if (nextblock == 7)
			{
				printf("            █");
			}
		}
		if (i == 5)
		{
			if (nextblock == 1)
			{
				printf("          ██");
			}
			if (nextblock == 2)
			{
				printf("            ██");
			}
			if (nextblock == 3)
			{
				printf("          ██");
			}
			if (nextblock == 4)
			{
				printf("          ███");
			}
			if (nextblock == 5)
			{
				printf("          ███");
			}
			if (nextblock == 6)
			{
				printf("");
			}
			if (nextblock == 7)
			{
				printf("          ███");
			}
		}
		if (i == 7)
		{
			printf("          Score");
		}
		if (i == 8)
		{
			printf("          %d", score);
		}
		if (i == 10)
		{
			printf("          游戏操作");
		}
		if (i == 11)
		{
			printf("          A左移，D右移，S加速下降，J左转，K右转，L直降");
		}
		if (i == 12)
		{
			printf("          游戏愉快");
		}
		if (i == 14)
		{
			printf("          Made By 陆海天");
		}
		printf("\\\n");
	}
	printf("----------------------");
}

//回合模块
void round()
{
	int i;
	if (dropjudge == 0)
	{
		if (roundcount == 0)
		{
			block = firstblock;
		}
		else
		{
			block = nextblock;
		}
		losecheck();
		roundcount++;
		srand(time(0));
		nextblock = rand() % 7 + 1;
		if (block == 1)
		{
			board[0][4] = 3;
			board[0][5] = 2;
			board[1][4] = 2;
			board[1][5] = 2;
		}
		if (block == 2)
		{
			board[0][4] = 2;
			board[0][5] = 3;
			board[1][5] = 2;
			board[1][6] = 2;
		}
		if (block == 3)
		{
			board[0][5] = 3;
			board[0][6] = 2;
			board[1][4] = 2;
			board[1][5] = 2;
		}
		if (block == 4)
		{
			board[0][4] = 2;
			board[1][4] = 3;
			board[1][5] = 2;
			board[1][6] = 2;
		}
		if (block == 5)
		{
			board[0][6] = 2;
			board[1][4] = 2;
			board[1][5] = 2;
			board[1][6] = 3;
		}
		if (block == 6)
		{
			board[0][4] = 2;
			board[0][5] = 3;
			board[0][6] = 2;
			board[0][7] = 2;
		}
		if (block == 7)
		{
			board[0][5] = 2;
			board[1][4] = 2;
			board[1][5] = 3;
			board[1][6] = 2;
		}
		show();
		for (i = 0; i <10; count++)
		{
			check();
			control();
			if (count == 10)
			{
				count = 0;
				drop();
			}
		}
	}
	else
	{
		
		for (i = 0; i <10; count++)
		{
			check();
			control();
			if (count == modetime)
			{
				count = 0;
				drop();
			}
		}
	}
}

//掉落模块
void drop()
{
	int i, j, k;
	dropjudge = 1;
	for (j = 9; j > -1; j--)
	{
		if (board[19][j] == 2 || board[19][j] == 3)
		{
			for (i = 19; i > -1; i--)
			{
				for (k = 9; k > -1; k--)
				{
					if (board[i][k] == 2)
					{
						board[i][k] = 1;
					}
					if (board[i][k] == 3)
					{
						board[i][k] = 1;
					}
				}
			}
			del();
			dropjudge = 0;
			round();
		}
	}
	for (i = 18; i > -1; i--)
	{
		for (j = 9; j > -1; j--)
		{
			if (board[i][j] == 2 || board[i][j] == 3)
			{
				if (board[i + 1][j] == 1)
				{
					dropjudge = 0;
				}
			}
		}
	}
	if (dropjudge == 0)
	{
		for (i = 19; i > -1; i--)
		{
			for (j = 9; j > -1; j--)
			{
				if (board[i][j] == 2 || board[i][j] == 3)
				{
					board[i][j] = 1;
				}
			}
		}
		del();
		show();
		round();
	}
	else
	{
		for (i = 19; i > -1; i--)
		{
			for (j = 9; j > -1; j--)
			{
				if (board[i][j] == 2)
				{
					board[i][j] = 0;
					board[i + 1][j] = 2;
				}
				if (board[i][j] == 3)
				{
					board[i][j] = 0;
					board[i + 1][j] = 3;
				}
			}
		}
		del();
		show();
		round();
	}
}

//去除模块
void del()
{
	int i, j, k, l;
	for (k = 19; k > -1; k--)
	{
		if ((board[k][0] != 0) &&
			(board[k][1] != 0) &&
			(board[k][2] != 0) &&
			(board[k][3] != 0) &&
			(board[k][4] != 0) &&
			(board[k][5] != 0) &&
			(board[k][6] != 0) &&
			(board[k][7] != 0) &&
			(board[k][8] != 0) &&
			(board[k][9] != 0))
		{
			score = score + 100;
			for (j = 9; j > -1; j--)
			{
				board[k][j] = 0;
			}
			for (i = 9; i > -1; i--)
			{
				for (l = k; l > 0; l--)
				{
					board[l][i] = board[l - 1][i];
					board[l - 1][i] = 0;
				}
			}
		}
	}
}

//横向移动检查模块
void check()
{
	int i, j;
	amovecheck = 1;
	dmovecheck = 1;
	for (i = 19; i > -1; i--)
	{
		for (j = 1; j < 10; ++j)
		{
			if (board[i][j] == 2 || board[i][j] == 3)
			{
				if (board[i][j - 1] == 1)
				{
					amovecheck = 0;
					break;
				}
			}
		}
	}
	for (i = 19; i > -1; i--)
	{
		if (board[i][0] == 2 || board[i][0] == 3)
		{
			amovecheck = 0;
		}
	}
	for (i = 19; i > -1; i--)
	{
		for (j = 8; j >-1; j--)
		{
			if (board[i][j] == 2 || board[i][j] == 3)
			{
				if (board[i][j - 1] == 1)
				{
					dmovecheck = 0;
					break;
				}
			}
		}
	}
	for (i = 19; i > -1; i--)
	{
		if (board[i][9] == 2 || board[i][9] == 3)
		{
			dmovecheck = 0;
		}
	}
}

//左旋转模块
void jturn()
{
	int t;
	scan();
	for (t = 0; t < 3; ++t)
	{
		if (board[o[0] - point[t][1] + o[1]][o[1] + point[t][0] - o[0]] == 1 ||
			(o[0] - point[t][1] + o[1]) < 0 ||
			(o[0] - point[t][1] + o[1]) > 19 ||
			(o[1] + point[t][0] - o[0]) < 0 ||
			(o[1] + point[t][0] - o[0]) > 9)
		{
			turncheck = 0;
		}
	}
	if (turncheck == 1)
	{
		for (t = 0; t < 3; ++t)
		{
			board[point[t][0]][point[t][1]] = 0;
		}
		for (t = 0; t < 3; ++t)
		{
			board[o[0] - point[t][1] + o[1]][o[1] + point[t][0] - o[0]] = 2;
		}
	}
}

//右旋转模块
void kturn()
{
	int t;
	scan();
	for (t = 0; t < 3; ++t)
	{
		if (board[o[0] + point[t][1] - o[1]][o[1] - point[t][0] + o[0]] == 1 ||
			(o[0] + point[t][1] - o[1]) < 0 ||
			(o[0] + point[t][1] - o[1]) > 19 ||
			(o[1] - point[t][0] + o[0]) < 0 ||
			(o[1] - point[t][0] + o[0]) > 9)
		{
			turncheck = 0;
		}
	}
	if (turncheck == 1)
	{
		for (t = 0; t < 3; ++t)
		{
			board[point[t][0]][point[t][1]] = 0;
		}
		for (t = 0; t < 3; ++t)
		{
			board[o[0] + point[t][1] - o[1]][o[1] - point[t][0] + o[0]] = 2;
		}
	}
}

//旋转扫描模块
void scan()
{
	int i , j;
	turncheck = 1;
	temp = 0;
	for (i = 0; i < 20; ++i)
	{
		for (j = 0; j < 10; ++j)
		{
			if (board[i][j] == 3)
			{
				o[0] = i;
				o[1] = j;
			}
			if (board[i][j] == 2)
			{
				point[temp][0] = i;
				point[temp][1] = j;
				temp = temp + 1;
			}
		}
	}
}

//定义直降模块
void current()
{
	int i, j, k;
	min = 20;
	currentflag = 0;
	for (j = 0; j < 10; ++j)
	{
		currentflag = 0;
		for (i = 0; i < 20; ++i)
		{
			if (board[i][j] == 2 || board[i][j] == 3)
			{
				for (k = 0; k < 20; ++k)
				{
					if (board[k][j] == 1)
					{
						currentflag = 1;
						if (k - i - 1 < min)
						{
							min = k - i - 1;
						}
					}
				}
				if (currentflag == 0)
				{
					if (19 - i < min)
					{
						min = 19 - i;
					}
				}
			}
		}
	}
	for (i = 19; i > -1; i--)
	{
		for (j = 9; j > -1; j--)
		{
			if (board[i][j] == 2)
			{
				board[i][j] = 0;
				board[i + min][j] = 2;
			}
			if (board[i][j] == 3)
			{
				board[i][j] = 0;
				board[i + min][j] = 3;
			}
		}
	}
}

//结束判断模块
void losecheck()
{
	if (block == 1)
	{
		if (board[0][4] != 0 ||
			board[0][5] != 0 ||
			board[1][4] != 0 ||
			board[1][5] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 2)
	{
		if (board[0][4] != 0 ||
			board[0][5] != 0 ||
			board[1][5] != 0 ||
			board[1][6] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 3)
	{
		if (board[0][5] != 0 ||
			board[0][6] != 0 ||
			board[1][4] != 0 ||
			board[1][5] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 4)
	{
		if (board[0][4] != 0 ||
			board[1][4] != 0 ||
			board[1][5] != 0 ||
			board[1][6] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 5)
	{
		if (board[0][6] != 0 ||
			board[1][4] != 0 ||
			board[1][5] != 0 ||
			board[1][6] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 6)
	{
		if (board[0][4] != 0 ||
			board[0][5] != 0 ||
			board[0][6] != 0 ||
			board[0][7] != 0)
		{
			gamejudge = 0;
		}
	}
	if (block == 7)
	{
		if (board[0][5] != 0 ||
			board[1][4] != 0 ||
			board[1][5] != 0 ||
			board[1][6] != 0)
		{
			gamejudge = 0;
		}
	}
	if (gamejudge == 0)
	{
		system("cls");
		printf("                            Game Over\\\n\\\n                             Score:%d\\\n\\\n                   输入0结束游戏，输入1重新开始\\\n", score);
		scanf("%d", &conti);
		if (conti == 0)
		{
			exit(0);
		}
		if (conti == 1)
		{
			system("cls");
			main();
		}
	}
}
"""
cftext = \
"""0.词法分析两次扫描
(1). #define、 goto标签定位、 enum声明、 typedef
(2). 正常词法分析步骤

1.注释与忽略:
(1).  //
(2).  /*   */  不允许嵌套
省略: ' ' '\t' '\n' '\r' '\v'

2.关于#语句
大部分# .... 省略
#define XX NUM保留

3.标识符: return (IDENTIFIER, {{标识符名字}} )
大小写敏感
开头不能数字
[A-Za-z_][A-Za-z0-9_]*

4.保留字:  (KEYWORD, {{具体保留字}} )
(大小写敏感)
double int char struct void enum string √
if else for continue break do while √
goto return √
sizeof √
typedef √
true, false √

5.常量:  return (CONSTANT ,{{具体常量}} )
int-constant ?????
[0-9]+
char-constant
'单字符'(返回单引号')
string-constant
"......"(返回双引号")
floating-constant
[0-9]+\.*[0-9]+

6.符号:  return ( SYMBOL, {{具体符号}} )
# 贪心匹配
{
}
(
)
[
]
. ->
,
;
+ - * / %
<< >> & | ~ ^
! && ||
++ --
? :
=
== !=
> < >= <=

7.贪心匹配例子:

11111     return INT_CONST
11111.000 return FLOATING_CONST

char      return 关键字
charB     return 标识符

-> return "->"
- > return "-" andthen return ">" 
-- return "--"

= return "="
== return "=="

!
!=

&
&&

|
||

+
++

>
>=
>>

<
<=
<<

8.词法分析抛错(打印输出错误发生行, 以及错误信息)
 (0.字符串超限
 (1.字符串遇到非转义换行符
  exp:  "haha, 
				"
 (2. "    EOF(end of file) 
 (3. /*   EOF
 (4. 直接遇到   */
 (5. 标识符数字开头
 (6, 其他无法识别字符
"""

yftext = \
"""program ::= {global_declaration}+
 
global_declaration ::= enum_decl | variable_decl | function_decl | struct_decl

enum_decl ::= 'enum' varName '{' identifyName ['=' INT_CONST] {',' identifyName ['=' INT_CONST] }+ '}' ';'

variable_decl ::= type {'*'}* varName {'[' expression ']'}* { ',' {'*’}* varName {'[' expression ']'}* }* ';'

function_decl ::=  type {'*'}* routineName '(' parameterList ')' ';' 
				 | type {'*'}* routineName '(' parameterList ')' body_decl 

parameterList ::= type {'*'} varName ['[' [INT_CONST] ']']  {',' type {'*'} varName ['[' [INT_CONST] ']'] }*
				 
struct_decl ::= 'struct' varName '{' { variable_decl }+ '}' ';'

routineName = IDENTIFIER

varName ::= IDENTIFIER varNameTail
varNameTail ::= "." IDENTIFIER | "->" IDENTIFIER | ε

label ::= IDENTIFIER

type ::= singletype | doubletype
singletype ::= 'int' |'double' |'char' |'string' |'void'
doubletype ::= 'struct' varName | 'enum' varName

body_decl ::= '{' {variable_decl}* {statement}* '}'

statement ::=  ifStatement
			 | whileStatement
			 | returnStatement
			 | forStatement
			 | blockStatement
			 | gotoStatement
			 | label ':' statement 
			 | letStatement 
			 | doStatement
			 
ifStatement ::= 'if' '(' expression ')' '{' statements '}'
				[ 'else'  '{' statements '}' ]
	
whileStatement ::= 'while' '(' expression ')' '{' statements '}'
                 | 'do' '{' statements '}' 'while' '(' expression ')' ';'

returnStatement ::= 'return' [expression] ';'

forStatement ::= 'for' '(' [letStatement] ';' [expression] ';' [letStatement] ';' ')' '{' statements '}'

blockStatement ::= '{' body_decl '}'
				 
gotoStatement ::= 'goto' label ';'				 
				 
letStatement ::= {'*'}* varName {'['expression']'}* '=' expression ';'
			   | ["++"|"--"] varName ';'
	           | varName ["++"|"--"] ';'

doStatement ::= RoutineCall ';'

expression ::= term [op term]*

term ::=  INT_CONST                             
		| FLOAT_CONST           
		| CHAR_CONST          
		| STRING_CONST             
		| BOOL_CONST 
	    | '(' expression ')' 
		| leftunaryOp term 	
		| ["++"|"--"] varName
	    | varName ["++"|"--"] 
		| varName
		| varName  {'[' expression ']'}+ 
		| RoutineCall

RoutineCall ::= RoutineName '('  expressionList ')'

expressionList ::= [ expression {',' expression}* ] 

op ::= arithop | cmpop

arithop ::= '+' | '-' | '*' | '/' | '%' | '&&' | '||' | '&' | '|' | '^' | '<<' | '>>'
cmpop ::= '>' | '<' | '==' | '>=' | '<=' | '!='
leftunaryop ::= '-' | '+' | '!' | '&' | '*'
"""

systext = \
"""注释:
	'-' ::= 该元空缺
	TMP(XX) ::= 四元式临时中间变量
1.C语言常用库函数四元式:
	(printf, 实参个数, "-", 函数返回变量)
	(scanf, 实参个数, "-", 函数返回变量)
	(srand, 实参个数, "-", 函数返回变量)
	(time, 实参个数, "-", 函数返回变量)
	(rand, 实参个数, "-", 函数返回变量)
	(sleep, 实参个数, "-", 函数返回变量)
	(kbhit, 实参个数, "-", 函数返回变量)
	(getch, 实参个数, "-", 函数返回变量)
	(system, 实参个数, "-", 函数返回变量)
2.跳转四元式
	(jmp>=, label1, label2, value)
	(jmp>, label1, label2, value)
	(jmp, label1, label2, value)
	(goto, label, "-", "-")
	(call, 函数名, 实参个数, 函数返回变量)
	(return, 储存返回值的临时变量, "-", "-")
	(return, "-", "-", "-")
	(label, labelname, "-", "-")
3.算术四元式
	(unaryop, 符号作用变量, "-", 存储运算后值的变量)
	(aryop, 符号作用变量1, 符号作用变量2, 存储运算后值的变量)
	(左自增/减符号, 作用变量, "-", 存储运算后值的变量)
	(右自增/减符号, "-", 作用变量, 存储运算后值的变量)
4.赋值四元式
	("=", 上一个变量作为赋值对象, "-", 待赋值变量)
	("=", 赋值变量, "-", 临时变量)
5.形参实参说明四元式
	("FORMAL", "-", "-", 待说明为形参的变量)
	("ACTUAL", 上一个临时变量作为实参, 该实参为第几个实参)
6.进出四元式
	(IN, "-", "-", "-")
	(OUT, "-", "-", "-")
"""

aboutus = \
"""内容施工中...
"""