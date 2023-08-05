import matplotlib.pyplot as plt
import generand.Uniform as Uniform


u = UniformUniform(seed = 123).generate(100000)
plt.hist(u, bins=20)
plt.show()


# b= Binomial().generate(0.5,2000,50)
# plt.hist(z, bins=20)
# plt.show()

# t= Triangular().generate(2000000)
# plt.hist(t, bins=200)
# plt.show()
# plt

# p = Poisson().generate(alpha = 5,count=100000)
# plt.hist(p, bins=50)
# plt.show()
# plt

w = Weibull().generate(lamda=0.5, beta=2, count=1000000)
plt.hist(w, bins=200)
plt.show()
plt