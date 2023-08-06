class Uniform:
    """Uses desert island (LCG) Xi = 16807Xi-1*MOD(2^31 - 1) to generate U[0,1]"""
    def __init__(self, seed= 123456789,a=0,b=1):
        if seed <= 0:
            raise ValueError("Seed should be >=1")

        self.__a = 16807
        self.__mod = (2**31) - 1 
        self.seed = seed
        self.a = a
        self.b = b

    def generate(self, n=1):
        u = []
        temp = (self.__a*self.seed)%self.__mod
        u.append(temp/self.__mod)
        for i in range(1,n):
            temp = (self.__a*temp)%self.__mod
            u.append(self.a+(self.b-self.a)*(temp/self.__mod))

        return u