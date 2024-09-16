

def fabonacci_algorithm(n):
    if n < 3:
        return 1
    return fabonacci_algorithm(n-1) + fabonacci_algorithm(n-2) * fabonacci_algorithm(n-3)


print(fabonacci_algorithm(1))
