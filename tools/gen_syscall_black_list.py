#!/usr/bin/env python3

import sys
from itertools import islice


USAGE = """
    python gen_syscall_black_list.py <black_list_option> path

    where <black_list_option> can only be black or white
          path is a file contains integer(syscall number) splitted by newline
"""

def make_line(loi):
    return "  " + ",".join([str(i) for i in loi])

def get_element_lines(syscall_black_list, step=30):
    return "\n".join([make_line(syscall_black_list[i:i+step])
                      for i in islice(range(329), 0, None, step)])

def load_from_file(fn, is_black_list=True):
    """
    fn: the file that contains number of syscalls, splitted by newline
    is_black_list: if True means the number in fn is banned syscall
                   if False means the number in fn is safe syscall

    This function print result to stdout. The output is a C statement:
    static const int SYSCALL_BLACK_LIST[329] = {
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    };
    """
    syscall_black_list = [0] * 329 if is_black_list else [1] * 329

    with open(fn, "r") as f:
        sys_calls = [int(i)
                     for i in f.read().strip().split("\n") if i.isdigit()]

    for sys_call in sys_calls:
        syscall_black_list[sys_call] = 1 if is_black_list else 0

    first_line = "static const int SYSCALL_BLACK_LIST[329] = {"
    element_lines = get_element_lines(syscall_black_list)
    end_line = "};"
    return "\n".join([first_line, element_lines, end_line])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error number of command arguments!", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(127)

    black_list_option, fn = sys.argv[1], sys.argv[2]
    if black_list_option not in ['black', 'white']:
        print("black_list_option error!", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(126)

    c_statement = load_from_file(fn, black_list_option=='black')
    print(c_statement, file=sys.stdout)
