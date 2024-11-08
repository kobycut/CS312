import random
import sys
import timeit

# This may come in handy...
from fermat import miller_rabin

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return 1, 0, a
    (x1, y1, d1) = ext_euclid(b, a % b)
    x = y1
    y = x1 - ((a // b) * y1)
    return x, y, d1


# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
     specified bit length.
    """
    num = 4
    while miller_rabin(num, 20) != "prime":
        num = random.getrandbits(bits)
    return num  # Guaranteed random prime number obtained through fair dice roll


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Return N, e, d
    - N must be the product of two random prime numbers p and q
    - e and d must be multiplicative inverses mod (p-1)(q-1)
    """

    p = generate_large_prime()
    q = generate_large_prime()
    N = p * q
    e = 3
    relatively_prime = (p - 1) * (q - 1)
    for i in primes:
        if relatively_prime % i != 0:
            e = i
            break
    x, y, f = ext_euclid(relatively_prime, e)
    d = y % relatively_prime

    return N, e, d
[]