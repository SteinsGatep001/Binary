#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <errno.h>
int main()
{
    char* padding[101] = {[0 ... 99] = "A"};//0~99全赋值为"A"
    //Stage 1
    padding['A'] = "\x00";
    padding['B'] = "\x20\x0a\x0d";
    padding['C'] = "55555";//端口号 Stage5
    printf("Start\n");
    //Stage 2
    int pipe1[2],pipe2[2];
    if(pipe(pipe1) < 0 || pipe(pipe2) < 0)
    {
        printf("pipe error!\n");
        exit(-1);
    }
    //Stage 3
    char* envp[2] = {"\xde\xad\xbe\xef=\xca\xfe\xba\xbe"};
    //Stage 4
    FILE *fp = fopen("\x0a", "wb");
    if(!fp)
    {
        printf("File create failed\n");
        exit(-1);
    }
    else
    {
        fwrite("\x00\x00\x00\x00", 4, 1, fp);//这里是写一个4bytes的chunk区
        fclose(fp);
    }
    
    if(fork() == 0)
    {
        printf("Parent Processing is here...\n");
        dup2(pipe1[0],0);
        close(pipe1[1]);
        dup2(pipe2[0],2);
        close(pipe2[1]);
        execve("/home/input/input", padding, envp);
    }
    else
    {
        printf("Son processing is here...\n");
        write(pipe1[1], "\x00\x0a\x00\xff", 4);
        write(pipe2[1], "\x00\x0a\x02\xff", 4);
        
        int sd,cd;
        struct sockaddr_in saddr, caddr;
        sleep(5);
        printf("Connecting\n");
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1)
        {
            printf("socket error~\n");
            return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons(atoi(padding['C']));
        connect(sd, (struct sockaddr *)&saddr, sizeof(saddr));
        send(sd, "\xde\xad\xbe\xef", 4, 0);
        close(sd);
    }
    return 0;
}

