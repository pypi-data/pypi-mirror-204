from .exponential import Exponential

class Erlang:

    def __init__(self,lamda=0.1,k=3):
        self.lamda = lamda
        self.k = k

    """Generates pseudo exponential random numbers using exponential"""
    def generate(self,n=1):
        erlang = []
        for _ in range(n):
            erlang.append(sum(Exponential(lamda=self.lamda).generate(n=self.k)))
        return erlang
