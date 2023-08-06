
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
import matplotlib.ticker as t

fig, axs = plt.subplots(4, 3)
fig.tight_layout()

def plot_chart(x,n,title,chart_num,ylabel="Probability"):
    # setup figures
    ax_0 = chart_num // 3
    ax_1 = chart_num % 3
    axs[ax_0,ax_1].hist(x,bins=20)
    scale_y = n
    ticks_y = t.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    axs[ax_0,ax_1].yaxis.set_major_formatter(ticks_y)
    axs[ax_0,ax_1].set_ylabel(ylabel)
    axs[ax_0,ax_1].set_title(title)

uniform = Uniform().generate(n=100000)
plot_chart(uniform,100000,"Uniform Distribution (0,1)",0)

a=3
b=6
uniform2 = Uniform(a=a,b=b).generate(n=100000)
plot_chart(uniform2,100000,"Uniform Distribution ({0},{1})".format(a,b),1)

p=0.5
ber = Bernoulli(p).generate(n=100000)
plot_chart(ber,100000,"Bernoulli Distribution (p={0})".format(p),2)

p=0.5
trials=10
binomial= Binomial(p,trials).generate2(n=100000)
plot_chart(binomial,100000,"Binomial Distribution (p={0}, trials={1})".format(p,trials),3)

a=2
b=3
c=4
triangular= Triangular(a,b,c).generate(n=100000)
plot_chart(triangular,100000,"Triangular Distribution (a={0} b={1} c={2})".format(a,b,c),4)

alpha = 5
poisson = Poisson(alpha).generate(n=100000)
plot_chart(poisson,100000,"Poisson Distribution (alpha = {0})".format(alpha),5)

lamda=0.5
e = Exponential(lamda).generate(n=10000)
plot_chart(e,100000,"Exponential Distribution (lambda={0})".format(lamda),6)

lamda=0.25
k=3
er = Erlang(lamda,k).generate(n=10000)
plot_chart(er,100000,"Erlang Distribution (lambda={0} k={1})".format(lamda,k),7)

p=0.25
ge = Geometric(p).generate(n=10000)
plot_chart(ge,100000,"Geometric Distribution (p={0})".format(p),8)

mu=2
sigma=1.5
normal = Normal(mu,sigma).generate(n=100000)
#plt.hist(normal, bins=200)
#plt.show()
plot_chart(normal,100000,"Normal Distribution (mu={0} sigma={1})".format(mu,sigma),9)

lamda=0.5
beta=2
w = Weibull(lamda, beta).generate( n=100000)
plot_chart(w,100000,"Weibull Distribution (lambda={0}, beta={1})".format(lamda,beta),10)


plt.show()