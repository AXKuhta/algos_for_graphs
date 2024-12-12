#include <stdint.h>
#include <assert.h>

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
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
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
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
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
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
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
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
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

/*
int estimate_utility_v2b(uint8_t* bitmap, uint32_t w, uint32_t h) {
}

struct acc_t {
	int x;
	int o;
	int d;
	int s;
} acc = {0};

static void push(uint8_t value) {

}

static void pop(uint8_t value) {

}
*/
