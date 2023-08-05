from Weibull import Weibull

class Exponential:

    """Generates pseudo exponential random numbers using weibull with parameter beta =1"""
    def generate(self, lamda =1, count = 1):
        return Weibull().generate(lamda=lamda,beta=1,count=count)
