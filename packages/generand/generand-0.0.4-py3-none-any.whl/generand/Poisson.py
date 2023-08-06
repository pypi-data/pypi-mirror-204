import Uniform
import time
import math

    
# def generate(self, alpha= 1 , count= 1):
#     """Generates pseudo poisson random numbers using A-R method"""
#     poisson = []
#     for i in range(count):
#         x = -1
#         p = 1
#         while p >= math.exp(-alpha):
#             u = Uniform().generate()
#             x+=1
#             p = u[0]*p
#         poisson.append(x)
#     return poisson

def generate(alpha= 1 , count= 1):
    poissons = []
    for _ in range(count):
        
        x = 0
        p = 1
        i= 0
        u = Uniform.generate(time.perf_counter_ns(), 10*alpha)
        while p >= math.exp(-alpha):
            
            x+=1
            p = u[i]*p
            i+=1
        poissons.append(x)
    return poissons
