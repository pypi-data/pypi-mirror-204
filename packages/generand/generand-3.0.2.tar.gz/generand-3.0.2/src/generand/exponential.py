from .weibull import Weibull

class Exponential:

    def __init__(self,lamda=0.1):
        self.lamda = lamda

    """Generates pseudo exponential random numbers using weibull with parameter beta =1"""
    def generate(self, n = 1):
        return Weibull(lamda=self.lamda, beta=1).generate(n=n)

