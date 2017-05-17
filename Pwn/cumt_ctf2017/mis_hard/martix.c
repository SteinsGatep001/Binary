#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MARTIX_MAX 40
#define FLG_MARTIX_COL 1
#define KEY_MAX_NUM 90
#define END_FLG_NUM 2000

struct changes                    // 记录变化的过程， 以便逆过来求其逆矩阵
{
    int x1; 
    int x2;
}change_ls[MARTIX_MAX*MARTIX_MAX + 1 ] ;

int key_martix[MARTIX_MAX][MARTIX_MAX];    // key martix
int sol_martix[MARTIX_MAX][MARTIX_MAX];    // solve martix

char flag_str[MARTIX_MAX] = "mart1x_m1sc_233";


int prod_martix(int rows)
{
    int i,j,k;
    int end_num=0;
    int martix_totlen = rows*rows;
    for(i=0; i<MARTIX_MAX; i++)
        key_martix[i][i] = sol_martix[i][i] = 1;
    for(k=0; k<martix_totlen; k++)
    {
        int x1 = change_ls[k].x1 = rand()%rows;
        int x2 = rand()%rows;
        while(x1==x2)
            x2 = rand()%rows;
        change_ls[k].x2 = x2;
        for(i=0; i<rows; i++)
        {
            if(key_martix[x1][i] + key_martix[x2][i] >= KEY_MAX_NUM)
                break;
        }
        if(i>=rows)
        {
            for(i=0; i<rows; i++)
                key_martix[x1][i] += key_martix[x2][i];
        }
        else
        {
            k--;
            end_num++;
        }
        if(end_num >= END_FLG_NUM)
        {
            k++;
            break;
        }
    }
    for(k--; k>=0; k--)
    {
        for(i=0; i<rows; i++)
            sol_martix[change_ls[k].x1][i] -= sol_martix[change_ls[k].x2][i];
    }
    return 0;
}

int main()
{
    int len_flag = strlen(flag_str);
    int i, j;
    srand(time(0));
    // init 2 martix
    for(i=0; i<MARTIX_MAX; i++)
    {
        for(j=0; j<MARTIX_MAX; j++)
            key_martix[i][j] = sol_martix[i][j] = 0;
    }
    printf("flag length: %d\n", len_flag);
    printf("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n");

    // start convert
    prod_martix(len_flag);

    // print result
    printf("key martix:\n");
    for(i=0; i<len_flag; i++)
    {
        for(j=0; j<len_flag-1; j++)
            printf("%d ", key_martix[i][j]);
        printf("%d", key_martix[i][j]);
        printf("\n");
    }
    printf("reverse martix:\n");
    for(i=0; i<len_flag; i++)
    {
        for(j=0; j<len_flag-1; j++)
            printf("%d ", sol_martix[i][j]);
        printf("%d", sol_martix[i][j]);
        printf("\n");
    }
    return 0;
}


