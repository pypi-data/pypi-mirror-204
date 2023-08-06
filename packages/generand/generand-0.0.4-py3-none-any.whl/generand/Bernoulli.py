import Uniform

def generate(seed=1, p = 0.5):
    u = Uniform.generate(seed, 1)
    if u > p:
        return 1
    else: 
        return 0