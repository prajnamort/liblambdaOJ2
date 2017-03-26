#include <unistd.h>
#include <sys/types.h>

#include <stdio.h>
#include <stdlib.h>

#include "compile.h"


int main(int argc, char* argv[])
{
    //compile and print output to stdout
    //usage:
    // compile_code <src_file> <output_file> <compiler> <err_log_file>

    char *src_file = argv[1];
    char *output_file = argv[2];
    int compiler = atoi(argv[3]);
    char *err_log_file = argv[4];

    pid_t pid = getpid();
    setpgid(pid, pid);

    int compile_result;
    compile_result = compile(src_file, output_file, compiler, err_log_file);

    return compile_result;
}
