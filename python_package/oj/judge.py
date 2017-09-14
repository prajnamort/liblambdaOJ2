import os
import signal
import subprocess
from abc import ABCMeta, abstractmethod

from .consts import (COMPILERS, COMPILE_OK, COMPILE_ERROR, MAX_ERROR_MSG_LENGTH,
                     ACCEPTED, WRONG_ANSWER, TASK_STATUS, TASK_ALL_NORMAL)


class Judge(metaclass=ABCMeta):
    """
    This class implements the Python API for the C lib lambdaOJ2.
    And this class has 5 abstractmethod, to use it you have to
    inherit Judge, and implement these abstractmethod.

    * check_answer: (str * str) -> bool
    * get_test_input_by_id: int -> str
    * get_std_answer_by_id: int -> str

    The method run is to check submitted code, the return data of
    run is alawys a 2-element tuple:
    * (COMPILE_OK : integer, [(status : integer,
                               time_used : integer, in ms,
                               mem_used : integer, in KBytes)])
    * (COMPILE_ERROR: integer, error_message : string)

    The object can only by initialized by key-word parameters:
      judge_exe: string(full path of judge executable file),
      compile_code_exe: string(full path of compile_code executable file),
      problem_id: string(can be used to determine the input and std_answer path),
      work_dir: string(full path of the temp dir for judging),
      compiler_name: string, can only be one of keys of .consts.COMPILERS,
      source_code: string, (full path of the code submitted),
      sample_num: integer(the number of total test sample),
      mem_limit: integer(the memory limit, in KBytes),
      time_limit: integer(the time limit, in Seconds)
    """

    def __init__(self, * , judge_exe, compile_code_exe, problem_id,
                 work_dir, compiler_name, source_code, sample_num,
                 mem_limit, time_limit):
        self.judge_exe = judge_exe
        self.compile_code_exe = compile_code_exe
        self.problem_id = str(problem_id)
        self.work_dir = work_dir
        self.compiler_name = compiler_name
        self.source_code = source_code
        self.sample_num = sample_num
        self.mem_limit = str(mem_limit)
        self.time_limit = str(time_limit)

    def compile(self):
        self.exe_file = os.path.join(self.work_dir, "a.out")
        self.err_log = os.path.join(self.work_dir, "compile_err_msg")

        compiler = COMPILERS.get(self.compiler_name, -1)

        proc = subprocess.Popen([self.compile_code_exe, self.source_code,
                                 self.exe_file, str(compiler), self.err_log],
                                stdout=subprocess.PIPE)
        try:
            compile_result = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            compile_result = COMPILE_ERROR
        except:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            compile_result = COMPILE_ERROR
        return compile_result

    def run(self):
        if self.compile() == COMPILE_OK:
            results = (COMPILE_OK, self.run_samples())
        else:
            results = (COMPILE_ERROR, self.get_compile_err_msg())
        return results

    def try_decode(self, data):
        try:
            s = data.decode("utf-8").replace('\x00', '')
        except:
            s= ""
        return s

    def get_compile_err_msg(self):
        if os.path.exists(self.err_log):
            with open(self.err_log, "rb") as f:
                err_msg =  self.try_decode(f.read(MAX_ERROR_MSG_LENGTH))
        else:
            err_msg = ""
        return err_msg

    def run_samples(self):
        results = [self.run_one_sample(i) for i in range(self.sample_num)]
        return results

    @abstractmethod
    def get_test_input_by_id(self, id):
        return

    def get_sample_output_by_id(self, id):
        return os.path.join(self.work_dir, "out%s" % id)

    @abstractmethod
    def get_std_answer_by_id(self, id):
        return

    @abstractmethod
    def check_answer(self, std_answer, submit_output):
        return

    def run_one_sample(self, id):
        test_input = self.get_test_input_by_id(id)
        sample_output = self.get_sample_output_by_id(id)

        proc = subprocess.Popen([self.judge_exe, self.exe_file,
                                 test_input, sample_output,
                                 self.time_limit, self.mem_limit],
                                stdout=subprocess.PIPE)

        try:
            result = proc.communicate(timeout=3*int(self.time_limit))[0].decode("utf8")
            final_result, time_used, mem_used = [int(s) for s in result.split(',')]
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise NeedRejudgeError("Timeout for communicating")
        except:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise NeedRejudgeError("Other Reasons")

        if final_result == TASK_ALL_NORMAL:
            std_answer = self.get_std_answer_by_id(id)
            if self.check_answer(std_answer, sample_output):
                return (ACCEPTED, time_used, mem_used)
            else:
                return (WRONG_ANSWER, 0, 0)
        else:
            status = TASK_STATUS.get(final_result, -1)
            return (status, 0, 0)


class NeedRejudgeError(Exception):
    """
    Errors happend when read the stdout from judge process or
    when parsing the stdout from judge.
    """

    def __init__(self, message):
        self.message = message
