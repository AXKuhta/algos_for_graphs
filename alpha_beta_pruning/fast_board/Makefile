
all: lib.so tests.elf

lib.so: lib.c
	@gcc -g -O2 -Wall -shared lib.c -o lib.so

tests.elf: tests.c lib.c
	@gcc -g -O2 -Wall lib.c tests.c -o tests.elf

clean:
	@rm lib.so tests.elf
