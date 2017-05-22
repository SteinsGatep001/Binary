#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int getflag()
{
    char flag_buf[40];
    FILE *flag_fp = popen("cat flag.txt", "r");
    memset(flag_buf, 0, 40);
	write(1, "kazisa!\n", sizeof("kazisa!\n"));
    fgets(flag_buf, sizeof(flag_buf), flag_fp);
	write(1, flag_buf, strlen(flag_buf));
    fclose(flag_fp);
    exit(1);
}


int main()
{
	char m_buf[64];
    memset(m_buf, 0, 64);
	write(1, "Are you White scientist?\n", strlen("Are you White scientist?\n"));
	read(0, m_buf, 256);
    write(1, m_buf, strlen(m_buf));
	write(1, "Clearly I did it first.!\nWhy is it so?\n", strlen("Clearly I did it first.!\nWhy is it so?\n"));
	read(0, m_buf, 256);
	write(1, "Why are you so professional?\n", strlen("Why are you so professional?\n"));

	return 0;
}

