#include <stdio.h>
#include <stdlib.h>

int main()
{
    // char ch=getchar()
    // int ch=-1;
    char ch = getchar();
    if(ch==EOF) { printf("\nEOF: %d",EOF); }
    if((ch!=EOF)==0) { printf("\nit is equal to 0"); }
    if((ch!=EOF)==1) { printf("\nit is equal to 1"); }
    else { printf("\n it is equal to other value"); }
    system("/bin/sh");
    return 0;
}
