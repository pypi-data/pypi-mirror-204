import Uniform
import time
import math

def generate(lamda =1, beta =1, count = 1):
    weibull = []
    u = Uniform.generate(time.perf_counter_ns(), count)
    for i in range(count):
        weibull.append((-math.log(u[i])**(1/beta))/lamda)
    return weibull

