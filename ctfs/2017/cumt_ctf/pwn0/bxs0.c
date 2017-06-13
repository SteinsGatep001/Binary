#include <stdio.h>
#include <stdlib.h>
#include <error.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#define BUF_LENGTH 2048
#define MAX_CONNECT_LIMIT 1000

void *recv_data(void *fd);

int m_readbuf(int sockfd, char *buffer, int length)
{
    char tmp;
    int i;
    for(i=0; i<length; i++)
    {
        read(sockfd, &tmp, 1);
        if(tmp == '\n')
            break;
        buffer[i] = tmp;
    }
    return i;
}

int main(int argc, char *argv[])
{
    int server_sockfd, fd;
    struct sockaddr_in serv_addr;

    server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(server_sockfd < 0)
    {
        perror("socket create");
        exit(1);
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons( 28888 );
    if((bind(server_sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0)
    {
        perror("bind");
        exit(1);
    }
    if((listen(server_sockfd, MAX_CONNECT_LIMIT))<0)
    {
        perror("listen");
        exit(1);
    }
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(struct sockaddr);
    int *client_sockfd;
    printf("start listen connect\n");
    while(1)
    {
        pthread_t thread;
        client_sockfd = (int *)malloc(sizeof(int));
        *client_sockfd = accept(server_sockfd, (struct sockaddr *) &client_addr, &client_len);
        if(*client_sockfd == -1)
        {
            perror("client_sockfd");
            continue;
        }
        fd = pthread_create(&thread, NULL, recv_data, client_sockfd);
        if(fd != 0)
        {
            perror("pthread_create");
            break;
        }
    }
    shutdown(*client_sockfd, 2);
    shutdown(server_sockfd, 2);
    return 0;
}

void *recv_data(void *fd)
{
    char buffer[BUF_LENGTH];
    int client_sockfd = *((int*)fd);
    free(fd);       // free server created heap
    int n = m_readbuf(client_sockfd, buffer, BUF_LENGTH/2);
    if(strlen(buffer) > 233)
    {
        char tmpbuf[100] = {0};
        if(!strncmp(&buffer[233], "flag", 4))
        {
            FILE *flag_fp = popen("cat flag.txt", "r");
            printf("writing flag\n");
            fgets(tmpbuf, sizeof(tmpbuf), flag_fp);
            write(client_sockfd, tmpbuf, strlen(tmpbuf));
            fclose(flag_fp);
        }
        else
        {
            write(client_sockfd, "you are close to the flag\n", strlen("you are close to the flag\n"));
            if(strlen(buffer) > 237)
            {
                write(client_sockfd, "Too much string\n", strlen("Too much string\n"));
            }
            if(strlen(buffer) == 237)
            {
                write(client_sockfd, "enough string, ", strlen("enough string, "));
                write(client_sockfd, "but error code, ", strlen("but error code, "));
                write(client_sockfd, "replace the last 4 chars\n", strlen("replace the last 4 chars\n"));
            }
        }
    }
    else
        write(client_sockfd, "not enough\n", strlen("not enough\n"));
    if(n<0)
        printf("error in read buffer\n");
    else
        printf("read:\n%s\n", &buffer[233]);
    close(client_sockfd);
    pthread_exit(NULL);
}


