#include <stdint.h>
#include <assert.h>
#include <stdio.h>

// Нужно rows, cols - размер не меняется, всё просто
// Нужно pri, sec - размер меняется, сложнее

// В Си нет генераторов, но есть callback-и
// Делаем итераторы, которые вызывают:
// void push(u8)
// void push_pop(u8, u8)

// Пробежка по строкам
// bitmap	байты доски
// w		ширина
// h		высота
// span		размер окна
// push		добавить в окно
// push_pop	добавить и убрать из окна
// flush	закончить строку
void rows(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
) {
	for (uint32_t i = 0; i < h; i++) {
		for (uint32_t j = 0; j < w; j++) {
			if (j < span) {
				push( bitmap[i*w + j] );
			} else {
				push_pop(
					bitmap[i*w + j],
					bitmap[i*w + j - span]
				);
			}
		}
		flush();
	}
}

// Пробежка по столбцам
void cols(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
) {
	for (uint32_t j = 0; j < w; j++) {
		for (uint32_t i = 0; i < h; i++) {
			if (i < span) {
				push( bitmap[i*w + j] );
			} else {
				push_pop(
					bitmap[i*w + j],
					bitmap[i*w + j - span*w]
				);
			}
		}
		flush();
	}
}

// Пробежка по главной диагонали
void pri(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
) {
	for (uint32_t i = 0; i < h; i++) {
		for (uint32_t j = 0; i*w + j*w + j < w*h; j++) {
			if (j < span) {
				push( bitmap[i*w + j*w + j] );
			} else {
				push_pop(
					bitmap[i*w + j*w + j],
					bitmap[i*w + j*w + j - span*w - span]
				);
			}
		}
		flush();
	}

	for (uint32_t j = 1; j < w; j++) {
		for (uint32_t i = 0; i < h-j+1; i++) {
			if (i < span) {
				push( bitmap[i*w + j + i] );
			} else {
				push_pop(
					bitmap[i*w + j + i],
					bitmap[i*w + j + i - span*w - span]
				);
			}
		}
		flush();
	}
}

// Пробежка по обратной диагонали
void sec(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
) {
	for (uint32_t i = 0; i < h; i++) {
		for (uint32_t j = 0; i*w + j*w + j < w*h; j++) {
			if (j < span) {
				push( bitmap[w - 1 + i*w + j*w - j] );
			} else {
				push_pop(
					bitmap[w - 1 + i*w + j*w - j],
					bitmap[w - 1 + i*w + j*w - j - span*w + span]
				);
			}
		}
		flush();
	}

	for (uint32_t j = 1; j < w; j++) {
		for (uint32_t i = 0; i < h-j+1; i++) {
			if (i < span) {
				push( bitmap[w - 1 + i*w - j - i] );
			} else {
				push_pop(
					bitmap[w - 1 + i*w - j - i],
					bitmap[w - 1 + i*w - j - i - span*w + span]
				);
			}
		}
		flush();
	}
}

void estimate_utility_v2b(const char* bitmap, uint32_t w, uint32_t h, int span) {
	struct acc_t {
		int x;
		int o;
		int d;
		int s;
	} acc = {0};

	struct utility_t {
		int x;
		int o;
	} utility = {0};

	void dump() {
		printf("x=%d o=%d d=%d s=%d u.x=%d u.o=%d\n", acc.x, acc.o, acc.d, acc.s, utility.x, utility.o);
	}

	void step() {
		dump();
		switch (acc.d) {
			case 4:
				break;
			case 3:
				if (acc.x == 1) {
					utility.x += 10;
				} else if (acc.o == 1) {
					utility.o += 10;
				}
				break;
			case 2:
				if (acc.x == 2) {
					utility.x += 100;
				} else if (acc.o == 2) {
					utility.o += 100;
				}
				break;
			case 1:
				if (acc.x == 3) {
					utility.x += 1000;
				} else if (acc.o == 3) {
					utility.o += 1000;
				}
				break;
			case 0:
				if (acc.x == 4) {
					utility.x += 10000;
				} else if (acc.o == 4) {
					utility.o += 10000;
				}
				break;
			default:
				assert(0);
		}
	}

	void push(char x) {
		switch (x) {
			case 'x':
				acc.x++;
				break;
			case 'o':
				acc.o++;
				break;
			case '.':
				acc.d++;
				break;
			case ' ':
				acc.s++;
				break;
			default:
				assert(0);
		}

		if (acc.x + acc.o + acc.d + acc.s >= 4)
			step();
	}

	void push_pop(char a, char b) {
		switch (a) {
			case 'x':
				acc.x++;
				break;
			case 'o':
				acc.o++;
				break;
			case '.':
				acc.d++;
				break;
			case ' ':
				acc.s++;
				break;
			default:
				assert(0);
		}

		switch (b) {
			case 'x':
				acc.x--;
				break;
			case 'o':
				acc.o--;
				break;
			case '.':
				acc.d--;
				break;
			case ' ':
				acc.s--;
				break;
			default:
				assert(0);
		}

		step();
	}

	void flush() {
		acc.x = 0;
		acc.o = 0;
		acc.d = 0;
		acc.s = 0;
		printf("===\n");
	}

	printf("rows:\n");
	rows(bitmap, w, h, span, push, push_pop, flush);
	printf("cols:\n");
	cols(bitmap, w, h, span, push, push_pop, flush);
	printf("pri:\n");
	pri(bitmap, w, h, span, push, push_pop, flush);
	printf("sec:\n");
	sec(bitmap, w, h, span, push, push_pop, flush);
}
