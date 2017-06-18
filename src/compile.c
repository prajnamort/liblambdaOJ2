#include <unistd.h>
#include <setjmp.h>
#include <signal.h>

#include <sys/wait.h>
#include <sys/types.h>

#include <stdio.h>
#include <stdlib.h>

#include "compile.h"


volatile sig_atomic_t compile_result;


static void log_to_file(char*, char*);
static void compile_term(int);
static void time_up(int);
static int file_size(char *);

static void set_sig_action_for_chld();
static void set_sig_action_for_alarm();
static void block_sig(int);

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

static void set_sig_action_for_chld()
{
    struct sigaction act;
    act.sa_handler = compile_term;
    sigemptyset(&act.sa_mask);
    sigaddset(&act.sa_mask, SIGALRM);
    sigaction(SIGCHLD, &act, NULL);
}

static void set_sig_action_for_alarm()
{
    struct sigaction act;
    act.sa_handler = time_up;
    sigemptyset(&act.sa_mask);
    sigaddset(&act.sa_mask, SIGCHLD);
    sigaction(SIGALRM, &act, NULL);
}

void compile_code(char *compile_cmd,
                  char *compile_args[],
                  char *err_file,
                  int max_compile_time)
{
    /* first block SIGCHLD and SIGALRM*/
    sigset_t new_mask, old_mask;
    sigemptyset(&new_mask);
    sigaddset(&new_mask, SIGCHLD);
    sigaddset(&new_mask, SIGALRM);
    sigprocmask(SIG_BLOCK, &new_mask, &old_mask);

    set_sig_action_for_chld();
    set_sig_action_for_alarm();

    pid_t pid;
    pid = fork();
    if (pid == 0) {
        setpgid(0, getpid());
        freopen(err_file, "w", stderr);
        execv(compile_cmd, compile_args);
        exit(0);
    }

    /* max_compile_time > 0 */
    alarm(max_compile_time);

    sigsuspend(&old_mask);

    if (compile_result == TIME_UP) {
        log_to_file(err_file, "compile error!");
        kill(-pid, SIGKILL);
        wait(NULL);
    }
}

static void block_sig(int signo)
{
    sigset_t m;
    sigemptyset(&m);
    sigaddset(&m, signo);
    sigprocmask(SIG_BLOCK, &m, NULL);
}

static void log_to_file(char *file_path, char *msg)
{
    FILE* f = fopen(file_path, "w");
    fprintf(f, "%s", msg);
    fclose(f);
}

static void compile_term(int sig)
{
    compile_result = NOT_TIME_UP;
    block_sig(SIGALRM);
}

static void time_up(int sig)
{
    compile_result = TIME_UP;
    block_sig(SIGCHLD);
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
