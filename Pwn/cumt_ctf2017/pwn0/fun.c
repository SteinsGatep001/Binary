#include <stdio.h>
#include <stdlib.h>
#include <error.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

char h233_str[100] = ":)_:)_:)_:)_:)_:)_:)_:)_:)_:)_:)_:)__:)_:)_:)";

int m_readbuf(int new_sockfd, char *buffer, int length)
{
    char tmp;
    int i;
    for(i=0; i<length; i++)
    {
        read(new_sockfd, &tmp, 1);
        if(tmp == '\n')
            break;
        buffer[i] = tmp;
    }
    return i;
}

int main(int argc, char *argv[])
{
    int sockfd, new_sockfd;
    char buffer[2048];
    struct sockaddr_in serv_addr;
    struct hostent *server;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0)
    {
        perror("socket create");
        exit(1);
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons( 28888 );
    if((bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0)
    {
        perror("bin socket");
        exit(1);
    }
    listen(sockfd, 8); 
    struct sockaddr_in clien_addr;
    unsigned int addr_size = sizeof(clien_addr);
    while(1)
    {
        printf("new soc start\n");
        new_sockfd = accept(sockfd, (struct sockaddr *) &clien_addr, &addr_size);
        if(new_sockfd < 0)
        {
            perror("accept sm error");
            exit(1);
        }
        write(new_sockfd, h233_str, strlen(h233_str));
        write(new_sockfd, "guess the length of Force\n", strlen("guess the length of Force\n"));
        int n = m_readbuf(new_sockfd, buffer, 256);
        if(strlen(buffer) > 220)
        {
            FILE *flag_fp = popen("cat flag.txt", "r");
            char tmpbuf[100] = {0};
            write(new_sockfd, "you are close to the flag\n", strlen("you are close to the flag\n"));
            if(!strncmp(&buffer[220], "flag", 4))
            {
                printf("writing flag\n");
                fgets(tmpbuf, sizeof(tmpbuf), flag_fp);
                write(new_sockfd, tmpbuf, strlen(tmpbuf));
            }
            else
            {
                write(new_sockfd, "enough string, ", strlen("enough string, "));
                write(new_sockfd, "padding is exactly 199 or 220 or 221\n", strlen("padding is exactly 199 or 220 or 221\n"));
                write(new_sockfd, "but error code, ", strlen("but error code, "));
                write(new_sockfd, "guess the riddle\n", strlen("guess the riddle\n"));
            }
        }
        else
            write(new_sockfd, "not enough\n", strlen("not enough\n"));
        if(n<0)
            printf("error in read buffer\n");
        else
            printf("read:\n%s\n", buffer);
        close(new_sockfd);
        printf("[+]read over \n");
    }
    return 0;
}


