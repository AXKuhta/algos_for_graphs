#include <stdint.h>
#include <assert.h>
#include <stdio.h>

// =====================================================================================
// Прототипы
// =====================================================================================
void rows(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
);

void cols(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
);

void pri(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
);

void sec(
	const char* bitmap,
	uint32_t w,
	uint32_t h,
	uint32_t span,
	void push(char),
	void push_pop(char, char),
	void flush(void)
);

int estimate_utility_v2b(const char* bitmap, uint32_t w, uint32_t h, int span);
// =====================================================================================
// Тесты
// =====================================================================================
static void push_printf(char x) {
	printf("push(%c)\n", x);
}

static void push_pop_printf(char a, char b) {
	printf("push(%c) pop(%c)\n", a, b);
}

static void flush_printf(void) {
	printf("flush()\n");
}

void test_rows_1() {
	printf(" === %s ===\n", __func__);

	const char* hor =	"......."
				"......."
				"......."
				"......."
				"......."
				"xxxx...";

	rows(hor, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_cols_1() {
	printf(" === %s ===\n", __func__);

	const char* vert =	"......."
				"......."
				"..x...."
				"..x...."
				"..x...."
				"..x....";

	cols(vert, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_pri_1() {
	printf(" === %s ===\n", __func__);

	const char* diag =	"...o..."
				"....o.."
				"x....o."
				".x....o"
				"..x...."
				"...x...";

	pri(diag, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_pri_2() {
	printf(" === %s ===\n", __func__);

	const char* diag =	"0xyz9"
				"u0xyz"
				"vu0xy"
				"wvu0x"
				"1wvu0";

	pri(diag, 5, 5, 4, push_printf, push_pop_printf, flush_printf);
}

void test_sec_1() {
	printf(" === %s ===\n", __func__);

	const char* diag2 = 	"......o"
				"...y.ox"
				"..y.ox."
				".y.ox.."
				"y..x..."
				".......";

	sec(diag2, 7, 6, 4, push_printf, push_pop_printf, flush_printf);
}

void test_sec_2() {
	printf(" === %s ===\n", __func__);

	const char* diag2 =	"9zyx0"
				"zyx0u"
				"yx0uv"
				"x0uvw"
				"0uvw1";

	sec(diag2, 5, 5, 4, push_printf, push_pop_printf, flush_printf);
}

void test_estimate_rows() {
	printf(" === %s ===\n", __func__);

	const char* hor =	"......."
				"......."
				"......."
				"......."
				"......."
				"xxxx...";

	estimate_utility_v2b(hor, 7, 6, 4);
}

void test_estimate_cols() {
	printf(" === %s ===\n", __func__);

	const char* vert =	"......."
				"......."
				"..x...."
				"..x...."
				"..x...."
				"..x....";

	estimate_utility_v2b(vert, 7, 6, 4);
}

void test_estimate_pri() {
	printf(" === %s ===\n", __func__);

	const char* diag =	"...o..."
				"....o.."
				"x....o."
				".x....o"
				"..x...."
				"...x...";

	estimate_utility_v2b(diag, 7, 6, 4);
}

void test_estimate_sec() {
	printf(" === %s ===\n", __func__);

	const char* diag2 = 	"......o"
				".....ox"
				"....ox."
				"...ox.."
				"...x..."
				".......";

	estimate_utility_v2b(diag2, 7, 6, 4);
}

void test_estimate_utility_1() {
	printf(" === %s ===\n", __func__);

	const char* board = 	"......."
				"......."
				"......."
				"......."
				"......."
				"......x";

	int utility = estimate_utility_v2b(board, 7, 6, 4);

	assert(utility == 30);
}

void test_estimate_utility_2() {
	printf(" === %s ===\n", __func__);

	const char* board = 	"......."
				"......."
				"......."
				"......."
				"......."
				"o.....x";

	int utility = estimate_utility_v2b(board, 7, 6, 4);

	assert(utility == 0);
}

void test_estimate_utility_3() {
	printf(" === %s ===\n", __func__);

	const char* board = 	"       "
				"       "
				"       "
				"   .   "
				"  .x   "
				"..oo...";

	int utility = estimate_utility_v2b(board, 7, 6, 4);

	printf("Utility: %d\n", utility);
}

int main() {
	test_rows_1();
	test_cols_1();
	test_pri_1();
	test_pri_2();
	test_sec_1();
	test_sec_2();

	test_estimate_rows();
	test_estimate_cols();
	test_estimate_pri();
	test_estimate_sec();
	test_estimate_utility_1();
	test_estimate_utility_2();
	test_estimate_utility_3();
}
