def fib(n):
    if n is 0:
        return 0
    if n is 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def better_fib_go(n, a, b):
    if n is 0:
        return a
    return better_fib_go(n - 1, b, a + b)


def better_fib(n):
    return better_fib_go(n, 0, 1)


for x in range(998):
    print(x, ":", better_fib(x)) # 997

# for x in range(50):
#     print(x, ":", fib(x)) # 35
