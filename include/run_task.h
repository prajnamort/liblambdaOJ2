#define MAX_VIRTUAL_MEM_LIMIT 1024*1024*60
#define MAX_FILE_SIZE_LIMIT   1024*1024*60

#define EXIT_STATUS_CHILD_NOT_EXECV 2017

#define CHILD_END_NORMAL                0
#define CHILD_END_OUTPUT_LIMIT_EXCEEDED 1
#define CHILD_END_CPU_TIME_EXCEEDED     2
#define CHILD_END_BAD_SYSCALL           4
#define CHILD_END_TERM_BY_SIGNAL        8
#define CHILD_END_STOP_BY_OTHER_SIGNAL  16

#define TASK_ALL_NORMAL                 0
#define TASK_TIME_LIMIT_EXCEEDED        1
#define TASK_MEMORY_LIMIT_EXCEEDED      2
#define TASK_OUTPUT_LIMIT_EXCEEDED      4
#define TASK_BAD_SYSCALL                8
#define TASK_RUN_TIME_ERROR             16
#define TASK_UNKNOWN_RESULT             32


struct task_result {
    int final_result;
    long time_used;
    long mem_used;
};

void run_task(char* exe_file,
              char* input_file,
              char* output_file,
              int max_cpu_time_limit,
              int max_memory_limit,
              struct task_result* tr);

