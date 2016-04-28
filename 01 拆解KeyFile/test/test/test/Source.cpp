#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;
#define ROW 9
#define COL 16
#define TIMES 18*4

unsigned char key[TIMES] = { 0 };
int des[4][2]=
{
	{-1,0},//上
	{0,1},//右
	{1,0},//下
	{0,-1}//左
};
bool keygen(char g[ROW][COL],int x,int y,int keyn)
{
	if (g[x][y] == 'X')
		return true;
	if (keyn > TIMES)
		return false;
	g[x][y] = ' ';
	for (int i = 0;i < 4;i++)
	{
		int nx = des[i][0] + x;
		int ny = des[i][1] + y;
		if (nx >= 0 && ny >= 0 && (nx < ROW) && (ny < COL)&&g[nx][ny]!='*'&&g[nx][ny] != ' ')
		{
			key[keyn] = i;
			if (keyn == 70)
				cout << ' ';
			if (keygen(g, nx, ny, keyn + 1))
				return true;
			g[nx][ny] = '.';
			key[keyn] = -1;
		}
	}
}

int main()
{
	unsigned char name[100] = { 0 };
	char g[ROW][COL] = { 0 };
	unsigned char kk[TIMES / 4] = { 0 };
	for (int i = 0;i < TIMES;i++)
		key[i] = -1;
	for (int i = 0;i < ROW;i++)
		for (int j = 0; j < COL; j++)
			cin >> g[i][j];
	ofstream outfile;
	outfile.open("KwazyWeb.bit");
	if (keygen(g, 0, 0, 0))
	{
		for (int i = 0;i < TIMES;i += 4)
		{
			char kx = key[i];
			kx = (kx << 2) | key[i + 1];
			kx = (kx << 2) | key[i + 2];
			kx = (kx << 2) | key[i + 3];
			cout << hex<< kx << ' ';
			kk[i / 4] = kx;
		}
		cout << endl;
	}
	unsigned int number;
	cout << "请输入用户名字符个数";
	cin >> number;
	outfile << hex << unsigned char(number);
	cout << "请输入用户名";
	cin >> name;
	unsigned int c = 0;
	for (int i = 0;i < number;i++)
	{
		c += name[i];
		outfile << hex << name[i];
	}
	cout << unsigned char(c);
	for (int i = 0;i < TIMES / 4;i++)
	{
		kk[i] ^= unsigned char(c);
		cout << hex << kk[i]<<' ';
		outfile << hex << kk[i];
	}
	outfile.close();
	system("pause");
	return 0;
}
