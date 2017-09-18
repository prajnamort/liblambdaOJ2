#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import json
from shlex import shlex
import argparse

from oj import Judge


class MyJudge(Judge):

    def check_answer(self, fn1, fn2):
        with open(fn1, 'r') as f1, open(fn2, 'r') as f2:
            s1 = shlex(instream=f1, posix=True)
            s2 = shlex(instream=f2, posix=True)
            while True:
                t1, t2 = s1.get_token(), s2.get_token()
                if t1 is None and t2 is None:
                    return True
                if t1 is None or t2 is None:
                    return False
                if t1 != t2:
                    return False

    def get_test_input_by_id(self, id):
        return ""

    def get_std_answer_by_id(self, id):
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="the c/c++ source code file full path",
                        type=str, action="store")
    parser.add_argument("-c", "--compiler", help="the compiler use to compile the source code",
                        type=str, action="store")
    parser.add_argument("-w", "--work_dir", help="the work dir for compiling code and running judge",
                        type=str, action="store")
    parser.add_argument("-i", "--test_case_dir", help="the test cases(input and std answer) root dir",
                        type=str, action="store")
    parser.add_argument("-n", "--sample_num", help="the total number of samples need to run",
                        type=int, action="store")
    parser.add_argument("-m", "--mem_limit", help="the memory limit(in KBytes)",
                        type=int, action="store")
    parser.add_argument("-t", "--time_limit", help="the time limit(in seconds)",
                        type=int, action="store")
    parser.add_argument("-a", "--default_check", help="use default check function if true else use ta's check",
                        action="store_true")
    parser.add_argument("-b", "--ta_check_file", help="the ta's python file full path with check funtion",
                        type=str, action="store")

    args = parser.parse_args()
    if not args.default_check:
        from importlib.machinery import SourceFileLoader
        compare = SourceFileLoader('compare', args.ta_check_file).load_module()
        MyJudge.check_answer = lambda self, fn1, fn2: compare.compare_func(
            fn1, fn2)

    MyJudge.get_test_input_by_id = lambda self, id: os.path.join(
        args.test_case_dir, "%s.in" % id)
    MyJudge.get_std_answer_by_id = lambda self, id: os.path.join(
        args.test_case_dir, "%s.ans" % id)

    jd = MyJudge(judge_exe="/usr/local/bin/judge",
                 compile_code_exe="/usr/local/bin/compile_code",
                 problem_id="",
                 work_dir=args.work_dir,
                 compiler_name=args.compiler,
                 source_code=args.src,
                 sample_num=args.sample_num,
                 mem_limit=args.mem_limit,
                 time_limit=args.time_limit)

    result = jd.run()
    print(json.dumps(result))