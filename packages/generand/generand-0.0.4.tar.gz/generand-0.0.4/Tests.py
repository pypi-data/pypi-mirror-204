import matplotlib.pyplot as plt
import generand.Uniform as Uniform
import generand.Binomial as Binomial
import generand.Triangular as Triangular
import generand.Poisson as Poisson
import generand.Weibull as Weibull
import generand.Exponential as Exponential



u = Uniform.generate(seed= 123, count= 100000)
plt.hist(u, bins=20)
plt.show()


b= Binomial.generate(0.5,2000,50)
plt.hist(b, bins=20)
plt.show()

t= Triangular.generate(2000000)
plt.hist(t, bins=200)
plt.show()


p = Poisson.generate(alpha = 5,count=100000)
plt.hist(p, bins=50)
plt.show()


w = Weibull.generate(lamda=0.5, beta=2, count=1000000)
plt.hist(w, bins=200)
plt.show()
plt