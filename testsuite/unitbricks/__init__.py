import sys
from math import floor

mod = sys.modules[__name__]
mod.elapsed_time = 0

def elapse(ms):
    mod.elapsed_time = mod.elapsed_time + floor(ms)

def get_time():
    return mod.elapsed_time
    
def reset_time():
    mod.elapsed_time = 0
