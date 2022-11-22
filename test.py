#!./test
from unitbricks.runner import run_tests, run_module
import sys

TEST_PATH = "tests"
args = sys.argv
args.pop(0) # first element is command name

if len(args) > 0:
    for arg in args:
        path = f"{arg.replace('.', '/')}.test.py"
        run_module(path)

else:
    run_tests(TEST_PATH)
