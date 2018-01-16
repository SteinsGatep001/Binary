CC=gcc
CFLAGS=-static
RM = rm -f

ELF_BIN=poc

.DEFAULT_GOAL := all
all: $(ELF_BIN)

$(ELF_BIN): poc.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	$(RM) $(ELF_BIN)

