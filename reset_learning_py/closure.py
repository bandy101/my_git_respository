def createCounter():
    fs = []
    def f(i):
        def counter():
            return i+1
        return counter
    for i in range(3):
        fs.append(f(i))
    return fs
# x1,x2,x3 = createCounter()
# print(x1(),x2(),x3())

def closure():
    fs = []
    for _ in range(1,4):
        def f():
            return _**2
        fs.append(f)
    return fs
x1,x2,x3 = closure()
print(x1(),x2(),x3())