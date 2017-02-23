#include <unistd.h>
#include <sys/types.h>

#include <stdio.h>
#include <stdlib.h>

#include "run_task.h"


int main(int argc, char *argv[])
{
    //run_task and print output to stdout
    //usage:
    //  judge <exe_file> <input> <output> <time_limit> <mem_limit>

    char *exe_file = argv[1];
    char *input_file = argv[2];
    char *output_file = argv[3];

    int time_limit = atoi(argv[4]);
    int mem_limit = atoi(argv[5]);

    //create a new process group
    pid_t pid = getpid();
    setpgid(pid, pid);

    struct task_result tr;
    run_task(exe_file, input_file, output_file, time_limit, mem_limit, &tr);

    printf("%d,%ld,%ld", tr.final_result, tr.time_used, tr.mem_used);
    return 0;
}
