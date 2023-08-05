def generate(seed =1, count=1):
    u = []
    a = 16807
    mod = (2**31) - 1
    temp = (a*seed)%mod
    u.append(temp/mod)
    for i in range(1,count):
        temp = (a*temp)%mod
        u.append(temp/mod)

    return u