# compile parameters
COMPILERS = dict([
    ("c89", 0),
    ("c99", 1),
    ("c11", 2),
    ("c++03", 3),
    ("c++11", 4)
])

COMPILE_OK = 0
COMPILE_ERROR = -1

# run_task parameters
TASK_ALL_NORMAL                = 0
TASK_TIME_LIMIT_EXCEEDED       = 1
TASK_MEMORY_LIMIT_EXCEEDED     = 2
TASK_OUTPUT_LIMIT_EXCEEDED     = 4
TASK_BAD_SYSCALL               = 8
TASK_RUN_TIME_ERROR            = 16
TASK_UNKNOWN_RESULT            = 32
