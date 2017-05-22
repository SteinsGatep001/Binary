#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#define MAX 8                     // 矩阵大小
#define PT 10                     // 附矩阵 随机初始值的最大值
#define bianhuan 100             // 由对角线矩阵生成满秩矩阵所需的行变化次数
struct changs                    // 记录变化的过程， 以便逆过来求其逆矩阵
{
    int temp1 ; 
    int temp2 ;
}change[bianhuan + 1 ] ;

int Matrix[MAX][MAX] ;       // 满秩矩阵
int R_matrix[MAX][MAX];      // 逆矩阵

// ***** 生成 满秩矩阵 并求出该满秩矩阵的逆矩阵 ****************************//
void creat()
{
    int i  ,  k  ; 
    int flage = 0 ; 
    for(i = 0 ; i < MAX ; i ++ )                               // 生成主对角线矩阵
        Matrix[i][i] = R_matrix[i][i] = 1 ;
    for(k = 0 ; k < bianhuan ; k ++ )                         // 进行 行 随意变化生成满秩矩阵 ， 并记录下变化过程
    {
        int x1 = change[k].temp1  =  rand() % MAX ; 
        int x2 = rand() % MAX ; 
        while( x2  == x1 )
            x2 = rand() % MAX ;
        change[k].temp2  = x2 ;
        for(i = 0 ; i < MAX ; i ++ )
            if( Matrix[x1][i] + Matrix[x2][i] >= 31 ) break ;  // 控制矩阵中最大的数的范围在30内
        if(i >= MAX ) 
        {
            for(i = 0 ; i < MAX ; i ++ )
                Matrix[x1][i] += Matrix[x2][i] ;
        }
        else
            k-- ,flage ++ ;

        if(flage > 2000 )
        {
            k++; 
            break ;
        }  
    }
    for(k-- ; k >= 0 ; k -- )                                   // 行逆变换， 求出其逆矩阵
    {
        for( i = 0 ;  i < MAX ; i ++ )
            R_matrix[ change[k].temp1 ][i] -= R_matrix[ change[k].temp2 ][i] ;
    }
    return ;
}

int main()
{
    int i , j ;
    srand(time(0)) ;
    creat() ; 
    printf("加密矩阵为：\n") ;
    for(i =0 ; i < MAX ; i ++ )
    {
        for(j =0 ; j < MAX ; j ++)
            printf("%4d " , Matrix[i][j]) ;
        printf("\n") ;
    }
    printf("\n") ;
    printf("解密矩阵为：\n") ;
    for( i = 0;  i < MAX ; i ++ )
    {
        for(j =0 ; j  < MAX ; j ++ )
            printf("%4d ",R_matrix[i][j]) ;
            printf("\n");
    }
    return 0 ; 
}
