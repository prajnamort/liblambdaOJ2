# compile parameters
COMPILERS = dict([
    ("c89", 0),
    ("c99", 1),
    ("c11", 2),
    ("c++03", 3),
    ("c++11", 4)
])

COMPILE_OK = 0
COMPILE_ERROR = 1

MAX_ERROR_MSG_LENGTH = 4096

# run_task parameters
TASK_ALL_NORMAL                = 0
TASK_TIME_LIMIT_EXCEEDED       = 1
TASK_MEMORY_LIMIT_EXCEEDED     = 2
TASK_OUTPUT_LIMIT_EXCEEDED     = 4
TASK_BAD_SYSCALL               = 8
TASK_RUN_TIME_ERROR            = 16
TASK_UNKNOWN_RESULT            = 32

# task status
ACCEPTED = 0
WRONG_ANSWER = 1

TASK_STATUS = dict([
    (TASK_TIME_LIMIT_EXCEEDED, 2),
    (TASK_MEMORY_LIMIT_EXCEEDED, 3),
    (TASK_OUTPUT_LIMIT_EXCEEDED, 4),
    (TASK_BAD_SYSCALL, 5),
    (TASK_RUN_TIME_ERROR, 6),
    (TASK_UNKNOWN_RESULT, 7)
])
