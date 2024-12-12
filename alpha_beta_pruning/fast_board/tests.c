#include <stdint.h>
#include <stdio.h>

// =====================================================================================
// Прототипы
// =====================================================================================
void rows(
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
	void flush(void)
);

void cols(
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
	void flush(void)
);

void pri(
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
	void flush(void)
);

void sec(
	const uint8_t* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(uint8_t),
	void push_pop(uint8_t, uint8_t),
	void flush(void)
);
// =====================================================================================
// Тесты
// =====================================================================================
static void push_printf(uint8_t x) {
	printf("push(%c)\n", x);
}

static void push_pop_printf(uint8_t a, uint8_t b) {
	printf("push(%c) pop(%c)\n", a, b);
}

static void flush_printf(void) {
	printf("flush()\n");
}

void test_rows_1() {
	printf(" === test_rows_1 ===\n");

	const char* hor =	"......."
				"......."
				"......."
				"......."
				"......."
				"xxxx...";

	rows( (const uint8_t*)hor, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_cols_1() {
	printf(" === test_cols_1 ===\n");

	const char* vert =	"......."
				"......."
				"..x...."
				"..x...."
				"..x...."
				"..x....";

	cols( (const uint8_t*)vert, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_pri_1() {
	printf(" === test_pri_1 ===\n");

	const char* diag =	"...o..."
				"....o.."
				"x....o."
				".x....o"
				"..x...."
				"...x...";

	pri( (const uint8_t*)diag, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_sec_1() {
	printf(" === test_pri_2 ===\n");

	const char* diag2 = 	"......o"
				"...y.ox"
				"..y.ox."
				".y.ox.."
				"y..x..."
				".......";

	sec( (const uint8_t*)diag2, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

int main() {
	test_rows_1();
	test_cols_1();
	test_pri_1();
	test_sec_1();
}
