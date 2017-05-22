#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

int main()
{
    int mseed = time(0);
    srand(mseed);
    int tmp_randn;
    for(int i=0; i<10; i++)
    {
        tmp_randn = rand();
        printf("0x%8x\n", tmp_randn);
    }

    /**
    printf("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n");
    srand(mseed);
    for(int i=0; i<10; i++)
    {
        tmp_randn = rand();
        printf("0x%8x\n", tmp_randn);
    }
    **/

    return 0;
}


