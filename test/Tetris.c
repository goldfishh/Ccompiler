// ����˹����.cpp : �������̨Ӧ�ó������ڵ㡣
//����ͷ�ļ��Լ�����
#include "stdio.h"
#include "time.h"
#include "windows.h"
#include "stdlib.h"
#include "conio.h"
void initialization();   //��ʼ������
void round();            //����غϺ��������ڳ�ʼ��һ�غ������������
void show();             //������ʾ����
void control();          //����ٿغ���
void drop();             //������亯�������Ƶ��䣬��ȥ�ȣ�
void del();              //����ȥ��������������ȥ
void check();            //�����麯�������ڼ�鵱ǰ�����ƶ��Ƿ����
void jturn();            //��������ת����
void kturn();            //��������ת����
void scan();             //����ɨ�躯����ɨ�赱ǰ��ת�����Լ�������������
void current();          //����ֱ������
void losecheck();        //������Ϸ���жϺ���
char step;               //������Ʊ������ݶ�ad����,s���٣�j��ת��k��ת,lֱ��
int amovecheck;          //�������ƶ������������ڼ�⵱ǰ�����Ƿ����
int dmovecheck;          //�������ƶ������������ڼ�⵱ǰ�����Ƿ����
int smovecheck;          //�������ƶ������������ڼ�⵱ǰ�����Ƿ����
int count;               //�����ʱ�������ݶ�ÿ100us����һ�Σ�ÿ��100����
int roundcount;          //����غϼ�������
int score;               //���������������
int mode;                //������Ϸ�Ѷȣ��ݶ���1s����ͨ0.6s������0.2s
int modetime;            //�����Ѷȶ�Ӧʱ����
int board[20][10];       //��������20*10���Ҳ�������ʾ������˱����������жϣ�
int gamejudge;           //������Ϸ�жϱ����������ж���Ϸ������
int firstblock;          //�����һ����������
int block;               //���巽�����࣬7�֣����è�����ѵ���
int nextblock;           //������һ�������࣬7��
int dropjudge;           //��������жϱ����������ж��Ƿ��ܹ�˳������
int o[2];                //������ת���ģ���ֵΪ3������
int point[3][2];         //�����������飬��ֵΪ2������
int turncheck;           //������ת������
int temp;                //������ת��ʱ����
int min;                 //����ֱ����ʱ���������ڼ�¼������С����
int mintemp;             //����ֱ����ʱ���������������ʱ��¼�������
int currentflag;         //����ֱ���жϱ������ж���ײ��Ƿ��з���
int conti;               //�����ؿ�����

						 //������
int main()
{
	initialization();
	Sleep(1000);
	round();
	return 0;
}

//��ʼ��ģ��
void initialization()
{
	int i;
	int j;
	printf("����˹����\n");
	printf("��������Ϸ�Ѷ�\n1 ��   2 ��ͨ   3����   4����\n");
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

//����ģ��
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

//��ʾģ��
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
				printf("��");
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
				printf("          ����");
			}
			if (nextblock == 2)
			{
				printf("          ����");
			}
			if (nextblock == 3)
			{
				printf("            ����");
			}
			if (nextblock == 4)
			{
				printf("          ��");
			}
			if (nextblock == 5)
			{
				printf("              ��");
			}
			if (nextblock == 6)
			{
				printf("          ��������");
			}
			if (nextblock == 7)
			{
				printf("            ��");
			}
		}
		if (i == 5)
		{
			if (nextblock == 1)
			{
				printf("          ����");
			}
			if (nextblock == 2)
			{
				printf("            ����");
			}
			if (nextblock == 3)
			{
				printf("          ����");
			}
			if (nextblock == 4)
			{
				printf("          ������");
			}
			if (nextblock == 5)
			{
				printf("          ������");
			}
			if (nextblock == 6)
			{
				printf("");
			}
			if (nextblock == 7)
			{
				printf("          ������");
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
			printf("          ��Ϸ����");
		}
		if (i == 11)
		{
			printf("          A���ƣ�D���ƣ�S�����½���J��ת��K��ת��Lֱ��");
		}
		if (i == 12)
		{
			printf("          ��Ϸ���");
		}
		if (i == 14)
		{
			printf("          Made By ½����");
		}
		printf("\n");
	}
	printf("----------------------");
}

//�غ�ģ��
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

//����ģ��
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

//ȥ��ģ��
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

//�����ƶ����ģ��
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

//����תģ��
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

//����תģ��
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

//��תɨ��ģ��
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

//����ֱ��ģ��
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

//�����ж�ģ��
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
		printf("                            Game Over\n\n                             Score:%d\n\n                   ����0������Ϸ������1���¿�ʼ\n", score);
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