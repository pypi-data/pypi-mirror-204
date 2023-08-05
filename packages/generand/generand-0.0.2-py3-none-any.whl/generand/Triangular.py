import time
import Uniform


def generate(count=1):
    t = []

    for i in range(count):
        u = Uniform.generate(time.perf_counter_ns(), count=2)
        t.append(u[0] + u[1])
    
    return t
