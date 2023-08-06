from .uniform import Uniform
import time

class Binomial:

    def __init__(self,p=0.1,trials=10):
        self.p = p
        self.trials = trials

    def generate(self, n=1):
        result = []
        
        for i in range(n):
            u = Uniform(time.perf_counter_ns())
            uniforms = u.generate(self.trials)
            trialOutcomes =[int(x >= self.p) for x in uniforms] 
            result.append(sum(trialOutcomes))

        return result 

    def generate2(self, n=1):
        random_numbers = []
        alpha = 1 / self.p
        beta = 1 / ( 1 - self.p )
        for j in range(n):
            u = Uniform(time.perf_counter_ns()).generate()[0]
            result = []

            for i in range(self.trials):
                if u <= self.p:
                    result.append(1)
                    #print("i {2} alpha {0} u {1}".format(alpha,u,i))
                    u = alpha * u
                    #print("alpha {0} u {1}".format(alpha,u))
                else:
                    result.append(0)
                    u = beta * ( u - self.p )
                    #print("beta {0} u {1}".format(beta,u))
            random_numbers.append(sum(result))
        return random_numbers


