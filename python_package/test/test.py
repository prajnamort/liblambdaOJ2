import os
import unittest

from lambdaOJ2 import Judge


TEST_CASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_case")
INPUT_DIR = os.path.join(TEST_CASE_DIR, "input")
STD_DIR = os.path.join(TEST_CASE_DIR, "std")


def clear_dir(d):
    fns = os.listdir(d)
    for fn in fns:
        f = os.path.join(d, fn)
        os.system("rm -rf %s" % f)


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

    def test_run_ac(self):
        jd = MyJudge(judge_exe=os.path.join(os.getcwd(), "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(TEST_CASE_DIR, "ac.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)
        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 0)
        self.assertEqual([a for (a,b,c) in results],
                         [0 for r in results])
        clear_dir(os.path.join(TEST_CASE_DIR, "tmp"))

    def test_run_ce(self):
        jd = MyJudge(judge_exe=os.path.join(os.getcwd(), "judge"),
                     problem_id="1",
                     work_dir=os.path.join(TEST_CASE_DIR, "tmp"),
                     compiler_name="c89",
                     source_code=os.path.join(TEST_CASE_DIR, "ce.c"),
                     sample_num=2,
                     mem_limit=1024,
                     time_limit=1)
        (compile_result, results) = jd.run()
        self.assertEqual(compile_result, 1)
        clear_dir(os.path.join(TEST_CASE_DIR, "tmp"))

if __name__ == '__main__':
    os.chdir(TEST_CASE_DIR)
    unittest.main()
