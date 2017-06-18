#define C89    0
#define C99    1
#define C11    2
#define CPP03  3
#define CPP11  4

#define MAX_COMPILE_TIME 6

#define NOT_TIME_UP 0
#define TIME_UP 1


int compile(char *source_code,
            char *exe_file,
            int compiler,
            char *err_log);
