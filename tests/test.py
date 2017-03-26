#!/usr/bin/env python3

import os
import unittest
import shutil

from oj import Judge


TEST_CASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_case")
INPUT_DIR = os.path.join(TEST_CASE_DIR, "input")
STD_DIR = os.path.join(TEST_CASE_DIR, "std")
SRC_DIR = os.path.join(TEST_CASE_DIR, "src")

JUDGE_DIR = os.getenv("JUDGE_DIR")


def take_care_of_tmp(d):
    def dct(f):
        def wrapper(self):
            tmp_dir = os.path.join(d, "tmp")
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            os.mkdir(tmp_dir)
            r = f(self)
            shutil.rmtree(tmp_dir)
            return r
        return wrapper
    return dct


class MyJudge(Judge):

    def check_answer(self, fn1, fn2):
        f1 = open(fn1, "r")
        f2 = open(fn2, "r")
        result = (f1.read() == f2.read())
        f1.close()
        f2.close()
        return result

    def get_test_input_by_id(self, id):
        return os.path.join(INPUT_DIR, self.problem_id, str(id))

    def get_std_answer_by_id(self, id):
        return os.path.join(STD_DIR, self.problem_id, str(id))


class TestStringMethods(unittest.TestCase):

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_ac(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "ac.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)
        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [0 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_ce(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "ce.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)
        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 1)

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_wa(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "wa.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [1 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_tle(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "tle.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [2 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_mle(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "mle.c"),
                     sample_num=2,
                     mem_limit=500,
                     time_limit=1)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [3 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_ole(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "ole.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=5)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [4 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_bad_syscall(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "bad_syscall.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [5 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_re(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "re.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [6 for r in results])

    @take_care_of_tmp(TEST_CASE_DIR)
    def test_run_re(self):
        jd = MyJudge(judge_exe=os.path.join(JUDGE_DIR, "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(SRC_DIR, "re2.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=2)

        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [6 for r in results])


if __name__ == '__main__':
    unittest.main()
