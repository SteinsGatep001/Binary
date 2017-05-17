#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MTX_NUM 15
#define FLAG_REL_LEN 15

int crypt_martix[MTX_NUM][MTX_NUM]={
{36, 14, 17, 32, 8, 6, 1, 12, 76, 85, 49, 18, 57, 2, 2},
{33, 16, 16, 30, 6, 4, 2, 10, 72, 84, 47, 19, 57, 1, 1},
{28, 15, 15, 27, 6, 4, 1, 9, 64, 77, 43, 18, 53, 1, 2},
{19, 12, 11, 19, 5, 1, 1, 5, 43, 55, 28, 14, 39, 1, 1},
{25, 10, 11, 20, 6, 4, 1, 8, 49, 55, 30, 13, 38, 1, 1},
{26, 14, 15, 27, 4, 5, 0, 11, 63, 77, 44, 15, 51, 3, 3},
{31, 16, 16, 28, 7, 2, 2, 8, 66, 79, 42, 19, 55, 1, 1},
{15, 6, 8, 16, 2, 2, 0, 5, 37, 41, 26, 7, 26, 1, 1},
{40, 12, 17, 33, 7, 7, 2, 13, 81, 83, 51, 16, 54, 1, 1},
{35, 12, 17, 32, 6, 6, 1, 12, 76, 82, 50, 15, 53, 2, 2},
{24, 8, 11, 21, 4, 4, 1, 8, 51, 54, 33, 10, 35, 1, 1},
{30, 14, 13, 25, 7, 2, 2, 7, 61, 70, 38, 18, 49, 0, 0},
{32, 14, 16, 28, 7, 3, 2, 8, 68, 77, 44, 18, 53, 0, 2},
{29, 15, 15, 27, 7, 5, 1, 10, 64, 78, 42, 18, 54, 2, 3},
{32, 14, 17, 28, 7, 3, 2, 8, 68, 77, 44, 18, 53, 0, 3}};

int res_list[MTX_NUM] = {36561, 35105, 31960, 22284, 23943, 31608, 32782, 17037, 36965, 35429, 23503, 29507, 32688, 32515, 32853};
int mcry_list[MTX_NUM] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0 ,0 , 0};

int cal_flag(char *rd_str)
{
    int i, j, tmp_res;
    for(i=0; i<15; i++)
    {
        tmp_res = 0;
        for(j=0; j<FLAG_REL_LEN; j++)
            tmp_res += (int)(rd_str[j])*crypt_martix[i][j];
        mcry_list[i] = tmp_res;
    }
    for(i=0; i<15; i++)
    {
        if(mcry_list[i] != res_list[i])
            return -1;
    }
    return 0;
}

int main()
{
    char flag_buf[20] = {0};
    int flag_len, i, j, isfla;
    scanf("%s", flag_buf);
    flag_len = strlen(flag_buf);
    if(flag_len != FLAG_REL_LEN)
    {
        printf("error flag\n");
        return -1;
    }
    isfla = cal_flag(flag_buf);
    if(isfla != 0)
    {
        printf("error flag\n");
        return -1;
    }
    printf("right flag\n");
    return 0;
}

