#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void callsystem()
{
    system("/bin/sh");
}

void vulnerable_function()
{
    char buf[128];
    read(STDIN_FILENO, buf, 512);
}

int main()
{
    write(STDOUT_FILENO, "Hello, seigai\n", 14);
    vulnerable_function();
}
