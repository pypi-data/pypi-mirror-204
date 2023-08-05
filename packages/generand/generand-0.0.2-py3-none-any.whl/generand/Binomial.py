import Uniform
import time


def generate(successProbability:int = 0.5, noOfTrials:int= 10, noOfIterations:int = 1):
    result = []
    
    for i in range(0,noOfIterations):
        uniforms = Uniform.generate(time.perf_counter_ns(),count=noOfTrials)
        trialOutcomes =[int(x >= successProbability) for x in uniforms] 
        result.append(sum(trialOutcomes))

    return result 
