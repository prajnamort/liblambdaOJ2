#include <unistd.h>
#include <setjmp.h>
#include <signal.h>

#include <sys/wait.h>
#include <sys/types.h>

#include <stdio.h>
#include <stdlib.h>

#include "compile.h"


static sigjmp_buf buf ;

static void log_to_file(char*, char*);
static void compile_term(int);
static int file_size(char *);

static void c89_compile_handler(char*, char*, char*);
static void c99_compile_handler(char*, char*, char*);
static void c11_compile_handler(char*, char*, char*);
static void cpp03_compile_handler(char*, char*, char*);
static void cpp11_compile_handler(char*, char*, char*);


int compile(char *source_code,
            char *exe_file,
            int compiler,
            char *err_log)
{
    switch (compiler){
    case C89:
        c89_compile_handler(source_code, exe_file, err_log);
        break;
    case C99:
        c99_compile_handler(source_code, exe_file, err_log);
        break;
    case C11:
        c11_compile_handler(source_code, exe_file, err_log);
        break;
    case CPP03:
        cpp03_compile_handler(source_code, exe_file, err_log);
        break;
    case CPP11:
        cpp11_compile_handler(source_code, exe_file, err_log);
        break;
    }
    int err_len = file_size(err_log);
    if (err_len == 0)
        return 0;
    else
        return -1;
}

void compile_code(char *compile_cmd,
                  char *compile_args[],
                  char *err_file,
                  int max_compile_time)
{
    signal(SIGCHLD, compile_term);
    pid_t pid;

    if (sigsetjmp(buf,1)==0) {
        pid = fork();
        if (pid == 0) {
            setpgid(pid, pid);
            freopen(err_file, "w", stderr);
            execv(compile_cmd, compile_args);
            exit(0);
        }

        sleep(max_compile_time);
        signal(SIGCHLD,SIG_DFL);
        kill(-pid, SIGKILL);
		wait(NULL);

        log_to_file(err_file, "compile error!");
        return ;
    }
}

static void log_to_file(char *file_path, char *msg)
{
    FILE* f = fopen(file_path, "w");
    fprintf(f, "%s", msg);
    fclose(f);
}

static void compile_term(int sig)
{
    signal(SIGCHLD, SIG_DFL);
    while (waitpid(-1, 0, WNOHANG) > 0);
    siglongjmp(buf,1);
}


static void c89_compile_handler(char* source_code, char* exe_file, char* err_log)
{
    char *compile_cmd = "/usr/bin/gcc";
    char *args[] = {"/usr/bin/gcc", "-std=c89", "-static",
                    "-O2", "-w", "-lm", "-o",
                    exe_file, source_code, NULL};
    compile_code(compile_cmd, args, err_log, MAX_COMPILE_TIME);
}

static void c99_compile_handler(char* source_code, char* exe_file, char* err_log)
{
    char *compile_cmd = "/usr/bin/gcc";
    char *args[] = {"/usr/bin/gcc", "-std=c99", "-static",
                    "-O2", "-w", "-lm", "-o",
                    exe_file, source_code, NULL};
    compile_code(compile_cmd, args, err_log, MAX_COMPILE_TIME);
}

static void c11_compile_handler(char* source_code, char* exe_file, char* err_log)
{
    char *compile_cmd = "/usr/bin/gcc";
    char *args[] = {"/usr/bin/gcc", "-std=c11", "-static",
                    "-O2", "-w", "-lm", "-o",
                    exe_file, source_code, NULL};
    compile_code(compile_cmd, args, err_log, MAX_COMPILE_TIME);
}

static void cpp03_compile_handler(char* source_code, char* exe_file, char* err_log)
{
    char *compile_cmd = "/usr/bin/g++";
    char *args[] = {"/usr/bin/g++", "-std=c++03", "-static",
                    "-O2", "-w", "-lm", "-o",
                    exe_file, source_code, NULL};
    compile_code(compile_cmd, args, err_log, MAX_COMPILE_TIME);
}

static void cpp11_compile_handler(char* source_code, char* exe_file, char* err_log)
{
    char *compile_cmd = "/usr/bin/g++";
    char *args[] = {"/usr/bin/g++", "-std=c++11", "-static",
                    "-O2", "-w", "-lm", "-o",
                    exe_file, source_code, NULL};
    compile_code(compile_cmd, args, err_log, MAX_COMPILE_TIME);
}

static int file_size(char *file)
{
    FILE *fp = fopen(file, "rb");
    fseek(fp, 0, SEEK_END);
    int length = ftell(fp);
    fclose(fp);
    return length;
}
