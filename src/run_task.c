#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/user.h>
#include <sys/syscall.h>

#include <stdio.h>
#include <stdlib.h>

#include "run_task.h"


static void set_cpu_time_limit(int);
static void set_file_size_limit(int);
static void set_virtual_mem_limit(int);

static int is_safe(int);
static long convert2ms(struct timeval*);
static long get_cost_time(struct rusage* usage);

static void handle_normal_exit(struct task_result*, int);

//if SYSCALL_BLACK_LIST[syscall_id] = 0 means safe
static const int SYSCALL_BLACK_LIST[329] = {
    0,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
};


void run_task(char* exe_file,
              char* input_file,
              char* output_file,
              int max_cpu_time_limit,
              int max_memory_limit,
              struct task_result* tr)
{
    pid_t pid;

    pid = fork();

    if (pid == 0) {
        //child process, which do execv

        //set resource limit first
        set_cpu_time_limit(max_cpu_time_limit);
        set_file_size_limit(MAX_FILE_SIZE_LIMIT);
        set_virtual_mem_limit(MAX_VIRTUAL_MEM_LIMIT);

        freopen(input_file, "r", stdin) ;
        freopen(output_file, "w", stdout) ;

        char *args[] = {exe_file, NULL};

        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execv(exe_file, args);

        exit(EXIT_STATUS_CHILD_NOT_EXECV);
    } else {
        //parent process
        ptrace(PTRACE_SYSCALL, pid, NULL, NULL);

        int status;
        int child_end_state;
        struct user context;
        int is_first_syscall = 1;
        int in_out_flag = 0;

        while (1) {
            wait(&status);
            //child exit normal
            if (WIFEXITED(status)) {
                child_end_state = CHILD_END_NORMAL;
                break;
            }
            //child stopped
            if (WIFSTOPPED(status)) {
                if (WSTOPSIG(status) == SIGXFSZ) {
                    kill(pid, SIGKILL);
                    wait(NULL);
                    child_end_state = CHILD_END_OUTPUT_LIMIT_EXCEEDED;
                    break;
                }
                if (WSTOPSIG(status) == SIGXCPU) {
                    kill(pid, SIGKILL);
                    wait(NULL);
                    child_end_state = CHILD_END_CPU_TIME_EXCEEDED;
                    break;
                }
                if (WSTOPSIG(status)==SIGTRAP) {
                    if (is_first_syscall) {
                        ptrace(PTRACE_SYSCALL, pid, NULL, NULL);
                        is_first_syscall = 0;
                        continue;
                    }
                    if (in_out_flag) {
                        ptrace(PTRACE_SYSCALL, pid, NULL, NULL);
                    } else {
                        ptrace(PTRACE_GETREGS, pid, NULL, &context.regs);
                        int syscall_number = context.regs.orig_rax;
                        if (!is_safe(syscall_number)) {
                            kill(pid, SIGKILL);
                            wait(NULL);
                            child_end_state = CHILD_END_BAD_SYSCALL;
                            break;
                        }
                    }
                    in_out_flag = 1 - in_out_flag;
                    ptrace(PTRACE_SYSCALL,pid,NULL,NULL);
                    continue;
                }
                //stopped by other signal
                kill(pid, SIGKILL);
                wait(NULL);
                child_end_state = CHILD_END_STOP_BY_OTHER_SIGNAL;
                break;
            };
            //child term by other signal
            if (WIFSIGNALED(status)) {
                kill(pid, SIGKILL);
                wait(NULL);
                child_end_state = CHILD_END_TERM_BY_SIGNAL;
                break;
            };
        }

        switch(child_end_state) {
        case CHILD_END_NORMAL:
            handle_normal_exit(tr, max_memory_limit);
            break;
        case CHILD_END_OUTPUT_LIMIT_EXCEEDED:
            tr->final_result = TASK_OUTPUT_LIMIT_EXCEEDED;
            break;
        case CHILD_END_CPU_TIME_EXCEEDED:
            tr->final_result = TASK_TIME_LIMIT_EXCEEDED;
            break;
        case CHILD_END_BAD_SYSCALL:
            tr->final_result = TASK_BAD_SYSCALL;
            break;
        case CHILD_END_STOP_BY_OTHER_SIGNAL:
        case CHILD_END_TERM_BY_SIGNAL:
            tr->final_result = TASK_RUN_TIME_ERROR;
            break;
        default:
            tr->final_result = TASK_UNKNOWN_RESULT;
        }
    }
}

static void set_cpu_time_limit(int max_cpu_time_limit)
{
    struct rlimit rl_cpu;
    getrlimit(RLIMIT_CPU, &rl_cpu);
    rl_cpu.rlim_cur = max_cpu_time_limit;
    setrlimit(RLIMIT_CPU, &rl_cpu);
}

static void set_file_size_limit(int max_file_size_limit)
{
    struct rlimit rl_fsize;
    getrlimit(RLIMIT_FSIZE, &rl_fsize);
    rl_fsize.rlim_cur = max_file_size_limit;
    setrlimit(RLIMIT_FSIZE, &rl_fsize);
}

static void set_virtual_mem_limit(int max_virtual_mem_limit)
{
    struct rlimit rl_as;
    getrlimit(RLIMIT_AS, &rl_as);
    rl_as.rlim_cur = max_virtual_mem_limit;
    setrlimit(RLIMIT_AS, &rl_as);
}

static int is_safe(int syscall_number)
{
    return SYSCALL_BLACK_LIST[syscall_number] == 0;
}

static long convert2ms(struct timeval *tv)
{
    return (tv->tv_sec*1000000 + tv->tv_usec)/1000 ;
}

static long get_cost_time(struct rusage* usage)
{
    long cost_time;
    cost_time = convert2ms(&usage->ru_utime) + convert2ms(&usage->ru_stime);
    return cost_time;
}

static void handle_normal_exit(struct task_result* tr, int mem_limit)
{
    struct rusage usage ;
    getrusage(RUSAGE_CHILDREN, &usage) ;

    long mem = usage.ru_maxrss;
    if (mem > mem_limit) {
        tr->final_result = TASK_MEMORY_LIMIT_EXCEEDED;
        return;
    }

    long time = get_cost_time(&usage);

    tr->mem_used = mem;
    tr->time_used = time;
    tr->final_result = TASK_ALL_NORMAL;
}
