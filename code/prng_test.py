# UFPE PPGEE
# author: Davi Moreno
#
# Python code that implements a PRNG based on a recurrence relation over GF(2^e)
# Recurrence relation: x_{n+1} = (a(x) * x_n + c(x))(mod h(x)) 

import galois
import random

def generate_random_integer(min_val, max_val, seed=42):
    random.seed(seed)
    return random.randint(min_val, max_val)

# Main
def main():
    # Parameters
    e = 31 # exponent
    order = 2**e # field order
    ax = "x^4 + 1"
    cx = "1"
    hx = "x^31 + x^13 + x^8 + x^3 + 1"
    # x0 = generate_random_integer(0, order-1) # initial condition
    x0 = 478163327

    # Creating GF(2^e)
    GF = galois.GF(order, irreducible_poly=hx)
    
    # Converting parameters to elements in GF
    ax = GF(ax)
    cx = GF(cx)
    x0 = GF(x0)

    # Iterating 100 times the PRNG
    x = x0
    print(f"Initial Cond. : {x0}")
    for i in range(100):
        x = ax * x + cx
        prng_out = x
        print(f"i: {i}, prng_out: {prng_out}")

if __name__ == "__main__":
    main()