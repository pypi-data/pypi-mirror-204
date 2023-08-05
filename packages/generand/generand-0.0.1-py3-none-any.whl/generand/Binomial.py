from Uniform import Uniform
import time

class Binomial:

    def generate(self, successProbability:int = 0.5, noOfTrials:int= 10, noOfIterations:int = 1):
        result = []
        
        for i in range(0,noOfIterations):
            u = Uniform(time.perf_counter_ns())
            uniforms = u.generate(noOfTrials)
            trialOutcomes =[int(x >= successProbability) for x in uniforms] 
            result.append(sum(trialOutcomes))

        return result 