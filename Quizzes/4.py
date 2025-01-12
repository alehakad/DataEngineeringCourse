from functools import partial

functions = []
for i in range(10):
    # functions.append((lambda x: lambda: x)(i)) # first solution - IIFE - self executing anonymous function
    functions.append(lambda x=i: x)  # 2 solution - default lambda parameter
    # functions.append(partial(lambda x: x, i))# 3 solution - functools.partial 
for f in functions:
    print(f())
