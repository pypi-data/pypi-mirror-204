from Uniform import Uniform
import time
import math
class Weibull:

    def generate(self, lamda =1, beta =1, count = 1):
        weibull = []
        u = Uniform(time.perf_counter_ns()).generate(count)
        for i in range(count):
            weibull.append((-math.log(u[i])**(1/beta))/lamda)
        return weibull
