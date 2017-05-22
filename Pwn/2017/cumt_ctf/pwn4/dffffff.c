#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define M_WORLD_SIZE 10

struct mi_craft
{
    int isused;
    int msize;
    char *sundary;
};

struct mi_craft **min_world;

void print_sayu()
{
    write(1, "== >_< ==== >_< ==== >_< === >_< === >_< === >_< ==== >_< ==== >_< === >_< === >_< \n", strlen("== >_< ==== >_< ==== >_< === >_< === >_< === >_< ==== >_< ==== >_< === >_< === >_< \n"));
    return;
}

void exit_err(char *buf)
{
    perror(buf);
    print_sayu();
    write(1, "sakura sakura aitaiyo iyada kimi ni ima sugu aitaiyo\n", strlen("sakura sakura aitaiyo iyada kimi ni ima sugu aitaiyo\n"));
    for(int i=0; i<M_WORLD_SIZE; i++)
    {
        if(min_world[i]->isused == 1)
        {
            min_world[i]->isused = 0;
            min_world[i]->msize = 0;
            if(min_world[i]->sundary != NULL)
                free(min_world[i]->sundary);
        }
    }
    if(min_world != NULL)
        free(min_world);
    exit(1);
}

int read_mbuf(char *buf, int length)
{
    char tmp_ch;
    int i;
    for(i=0; i<length; i++)
    {
        read(0, &tmp_ch, 1);
        if(tmp_ch == '\n')
            break;
        buf[i] = tmp_ch;
    }
    return i;
}

int get_int()
{
    int tmp;
    char tmp_buf[10];
    int length = read_mbuf(tmp_buf, 6);
    if(length<=0)
        return -1;
    return atoi(tmp_buf);
}

void create_mincraft()
{
    print_sayu();
    write(1, "Init the world size:\n", strlen("Init the world size:\n"));
    int siz_wrold = get_int();
    if(siz_wrold<0)
        exit_err("23333");
    if(siz_wrold>0x200)
    {
        write(1, "your machine is too old to create so much\n", strlen("your machine is too old to create so much\n"));
        return;
    }
    for(int i=0; i<M_WORLD_SIZE; i++)
    {
        if(min_world[i]->isused == 0)
        {
            write(1, "Enter\n", strlen("Enter\n"));
            write(1, "Excalibur!\n", strlen("Excalibur!\n"));
            min_world[i]->sundary = malloc(siz_wrold);
            read_mbuf(min_world[i]->sundary, siz_wrold);
            min_world[i]->isused = 1;
            min_world[i]->msize = siz_wrold;
            write(1, "Finished\n", strlen("Finished\n"));
            return;
        }
    }
    write(1, "Wow, you are skilled\n", strlen("Wow, you are skilled\n"));
}

void lookup_minecraft()
{
    write(1, "which one would you like to check\n", strlen("which one would you like to check\n"));
    int mid = get_int();
    if((mid>=0) && (mid<M_WORLD_SIZE))
    {
        if(min_world[mid]->isused == 1)
        {
            print_sayu();
            write(1, "ka kunin ofu lixi masi\n", strlen("ka kunin ofu lixi masi\n"));
            write(1, min_world[mid]->sundary, min_world[mid]->msize);
            write(1, "\nzhunbi xiuliao\n", strlen("\nzhunbi xiuliao\n\n"));
        }
        else
            write(1, "You are not the owner of the space\n", strlen("You are not the owner of the space\n"));
    }
}

void destroy_minecraft()
{
    print_sayu();
    write(1, "Init ds program\n", strlen("Init ds program\n"));
    write(1, "Input id: ", strlen("Input id: "));
    int mid = get_int();
    if((mid>=0) && (mid<M_WORLD_SIZE))
    {
        if(min_world[mid]->isused == 1)
        {
            if(min_world[mid]->sundary != NULL)
                free(min_world[mid]->sundary);
            min_world[mid]->isused = 0;
            min_world[mid]->msize = 0;
            min_world[mid]->sundary = NULL;
            write(1, "destroy ok!\n", strlen("destroy ok!\n"));
        }
        else
        {
            write(1, "Wana use after free?\n", strlen("Want use after free?\n"));
            write(1, "No way!\n", strlen("No way!\n"));
        }
    }
}

void build_minecraft()
{
    print_sayu();
    write(1, "Start build\n", strlen("Start build\n"));
    write(1, "Input id: ", strlen("Input id: "));
    int mid = get_int();
    if((mid>=0) && (mid<M_WORLD_SIZE))
    {
        if(min_world[mid]->isused == 1)
        {
            write(1, "Umm.. How much are .. you\n", strlen("Umm.. How much are .. you\n"));
            int ch_size = get_int();
            if(ch_size<=0)
            {
                write(1, "You do nonthing!\n", strlen("You do nonthing!\n"));
                return;
            }
            write(1, "What are you going\n", strlen("What are you going\n"));
            read_mbuf(min_world[mid]->sundary, ch_size);
            write(1, "Ok Ok\n", strlen("Ok Ok\n"));
        }
    }
}

int get_the_world()
{
    write(1, "1: create minecraft\n", strlen("1: create minecraft\n"));
    write(1, "2: lookup to minecraft\n", strlen("2: lookup to minecraft\n"));
    write(1, "3: destroy minecraft\n", strlen("3: destroy minecraft\n"));
    write(1, "4: build minecraft\n", strlen("4: build minecraft\n"));
    write(1, "5: break Dimension wall\n", strlen("5: break Dimension wall\n"));
    write(1, "23333: \n", strlen("23333: \n"));
    int choice = get_int();
    switch(choice)
    {
        case 1:
            create_mincraft();
            break;
        case 2:
            lookup_minecraft();
            break;
        case 3:
            destroy_minecraft();
            break;
        case 4:
            build_minecraft();
            break;
        case 5:
            exit_err("[*]sakura");
            break;
        default:
            write(1, "0Ops!!! Are you kidding me?\n", strlen("0Ops!!! Are you kidding me?\n"));
            break;
    }
}

void init_world()
{
    min_world = malloc(M_WORLD_SIZE*sizeof(min_world));
    for(int i=0; i<M_WORLD_SIZE; i++)
    {
        min_world[i] = malloc(sizeof(struct mi_craft));
        min_world[i]->isused = 0;
        min_world[i]->msize = 0;
        min_world[i]->sundary = 0;
    }
}

int main()
{
    print_sayu();
    write(1, "Welcome to dffffff 233333\n", strlen("Welcome to dffffff 233333\n"));
    init_world();
    while(1)
        get_the_world();
    return 0;
}


