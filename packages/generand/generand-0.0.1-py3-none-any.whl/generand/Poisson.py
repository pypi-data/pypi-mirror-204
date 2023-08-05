from Uniform import Uniform
import time
import math
class Poisson:

    """Generates pseudo poisson random numbers using A-R method"""
    def generate(self, alpha= 1 , count= 1):
        poisson = []
        for i in range(count):
            x = -1
            p = 1
            while p >= math.exp(-alpha):
                u = Uniform(time.perf_counter_ns()).generate()
                x+=1
                p = u[0]*p
            poisson.append(x)
        return poisson

        # def generate(self, alpha= 1 , count= 1):
        #     poisson = []
        #     for _ in range(count):
                
        #         x = 0
        #         p = 1
        #         i= 0
        #         u = Uniform(time.perf_counter_ns()).generate(5*alpha)
        #         while p >= math.exp(-alpha):
                    
        #             x+=1
        #             p = u[i]*p
        #             i+=1
        #         poisson.append(x)
        #     return poisson