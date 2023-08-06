import imp
from re import L
import matplotlib.pyplot as plt
from generand.uniform import Uniform
from generand.binomial import Binomial
from generand.triangular import Triangular
from generand.poisson import Poisson
from generand.weibull import Weibull
from generand.erlang import Erlang
from generand.exponential import Exponential
from generand.geometric import Geometric
from generand.normal import Normal
from generand.bernoulli import Bernoulli

u = Uniform().generate(n=100000)
plt.hist(u, bins=20)
plt.show()

u = Uniform(a=3,b=6).generate(n=100000)
plt.hist(u, bins=20)
plt.show()

ber = Bernoulli(p=0.5).generate(n=100000)
plt.hist(ber, bins=20)
plt.show()


b= Binomial(p=0.5,trials=10).generate2(n=100000)
plt.hist(b, bins=20)
plt.show()

t= Triangular(a=2,b=3,c=4).generate(n=100000)
plt.hist(t, bins=200)
plt.show()
plt

p = Poisson(alpha = 5).generate(n=100000)
plt.hist(p, bins=50)
plt.show()
plt

e = Exponential(lamda=0.5).generate(n=10000)
plt.hist(e, bins=200)
plt.show()

er = Erlang(lamda=0.25,k=10).generate(n=10000)
plt.hist(er, bins=200)
plt.show()

ge = Geometric(p=0.25).generate(n=10000)
plt.hist(ge, bins=200)
plt.show()

normal = Normal(mu=2,sigma=1.5).generate(n=100000)
plt.hist(normal, bins=200)
plt.show()


w = Weibull().generate(lamda=0.5, beta=2, n=100000)
plt.hist(w, bins=200)
plt.show()
