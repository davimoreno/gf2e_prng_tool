# Pseudorandom Number Generator (PRNG) over GF(2^31)

Author      : Davi Moreno
Affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE

Implements a PRNG based on the affine recurrence relation:
```
    x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)
```
All polynomials have binary coefficients (0 or 1). The recurrence operates
over the finite field GF(2^31), defined by the irreducible polynomial h(x).

Constant polynomials given as:
- a(x) = x^4 + 1   // 31-bit vector
- c(x) = 1   // 31-bit vector
- h(x) = x^31 + x^13 + x^8 + x^3 + 1   // 32-bit irreducible polynomial

Project structure:
```
    gf2_31_prng/
    ├── rtl/
    │   ├── src/       # Verilog modules
    │   └── tb/        # Testbenches
    ├── modelsim/      # Simulation scripts
    ├── LICENSE        # License file
    └── README.md      # Project details
```
