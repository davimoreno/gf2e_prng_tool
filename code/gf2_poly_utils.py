# ==============================================================================
# Utility Functions for Polynomial Arithmetic over GF(2)
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Description:
#     This module provides core utility functions for performing arithmetic 
#     operations on polynomials with binary coefficients over the finite field GF(2).
#     Each polynomial is represented as an integer, where each bit corresponds to 
#     a coefficient: the bit 0, or least significant bit (LSB), represents the constant 
#     term, and bit i corresponds to the coefficient of x^i.
#
#     Supported operations:
#         - Identifying bit positions in binary representation
#         - Computing the degree of a binary polynomial
#         - Performing polynomial modular reduction over GF(2)
#         - Computing affine transformations of the form a(x)·p(x) + c(x)
#         - Reducing affine results modulo an irreducible polynomial h(x)
#
# ==============================================================================


from typing import List

import re

def get_bit_positions(n: int) -> List[int]:
    """
    Get positions of bits set to 1 in the binary representation of an integer.

    Parameters:
        n (int): The integer to analyze.

    Returns:
        List[int]: List of bit positions where n has a '1' bit.
                   The least significant bit is at position 0.

    Example:
        >>> get_bit_positions(0b10110)
        [1, 2, 4]  # Corresponds to x^1 + x^2 + x^4
    """
    positions = []
    position = 0
    while n:
        if n & 1:
            positions.append(position)
        n >>= 1
        position += 1
    return positions


def poly_degree(p: int) -> int:
    """
    Compute the degree of a binary polynomial.

    Parameters:
        p (int): Polynomial represented as an integer.

    Returns:
        int: Degree of the polynomial (highest exponent with non-zero coefficient),
             or -1 if p == 0.
    """
    if p == 0:
        return -1
    return p.bit_length() - 1


def poly_mod(y: int, h: int) -> int:
    """
    Compute y(x) mod h(x) over GF(2), using XOR-based long division.

    Parameters:
        y (int): Dividend polynomial (as an integer).
        h (int): Modulus polynomial (as an integer), typically irreducible.

    Returns:
        int: Remainder polynomial after modular reduction.
    """
    deg_h = poly_degree(h)
    rem = y
    while poly_degree(rem) >= deg_h:
        shift = poly_degree(rem) - deg_h
        rem ^= h << shift
    return rem


def poly_affine(a: int, p: int, c: int) -> int:
    """
    Compute a(x)·p(x) + c(x) over GF(2), where all polynomials have binary coefficients.

    Parameters:
        a (int): Multiplier polynomial a(x), as an integer.
        p (int): Input polynomial p(x), as an integer.
        c (int): Constant polynomial c(x), as an integer.

    Returns:
        int: Result of a(x)·p(x) + c(x) without modular reduction.

    Note:
        This operation corresponds to a linear feedback transformation.
    """
    out = 0
    for i in get_bit_positions(a):
        out ^= p << i
    return out ^ c


def poly_affine_mod(a: int, p: int, c: int, h: int) -> int:
    """
    Compute a(x)·p(x) + c(x) mod h(x) over GF(2).

    Parameters:
        a (int): Multiplier polynomial a(x), as an integer.
        p (int): Input polynomial p(x), as an integer.
        c (int): Constant polynomial c(x), as an integer.
        h (int): Irreducible modulus polynomial h(x), as an integer.

    Returns:
        int: Final result of the affine transformation reduced modulo h(x).
    """
    result = poly_affine(a, p, c)
    return poly_mod(result, h)

def str_poly_to_int(poly_str: str, poly_format: str) -> int:
    """
    Converts a binary polynomial over GF(2), given as a string into 
    its corresponding integer representation.

    Allowed input str format:
        - int  (e.g. "17")
        - hex  (e.g. "0x11")
        - bin  (e.g. "0b10001")
        - alg (e.g. "x^4 + 1")

    Parameters:
        poly_str (str): A string representing the binary polynomial.
        poly_format (str) : A string indicating the poly_str format.

    Returns:
        int: The integer representation of the binary polynomial.

    Example:
        str_poly_to_int("x^3 + x + 1", "alg") -> 11 (0b1011)
    """
    # Remove spaces for easier processing
    poly_str = poly_str.replace(" ", "")

    if poly_format == "int":
        # Guarantee that int polynomial is positive
        poly_int = abs(int(poly_str))
        return poly_int
    elif poly_format == "hex":
        poly_int = int(poly_str, 16)
        return poly_int
    elif poly_format == "bin":
        poly_int = int(poly_str, 2)
        return poly_int
    elif poly_format == "alg":
        # Match terms like x^n, x, or 1
        terms = re.findall(r'x\^\d+|x|1', poly_str)
        value = 0
        for term in terms:
            if term == '1':
                degree = 0
            elif term == 'x':
                degree = 1
            else:  # term like x^n
                degree = int(term[2:])

            value |= 1 << degree
        poly_int = value
        return poly_int
    else:
        raise Exception(f"{poly_format} is not a valid polynomial format.")

def int_poly_to_str(poly_int: int, poly_format: str) -> str:
    """
    Converts a binary polynomial over GF(2), given as an integer (e.g., 11),
    into its corresponding string representation format.

    Allowed output str format:
        - int  (e.g. "17")
        - hex  (e.g. "0x11")
        - bin  (e.g. "0b10001")
        - alg (e.g. "x^4 + 1")

    Parameters:
        poly_int (int): An integer representing the binary polynomial.
        poly_format (str): Output polynomial format

    Returns:
        str: A string representation of the binary polynomial.

    Example:
        int_poly_to_str(11) -> "x^3 + x + 1"
    """
    # Guarantee that int polynomial is positive/valid
    poly_int = abs(int(poly_int))

    if poly_format == "int":
        poly_str = str(poly_int) 
        return poly_str
    elif poly_format == "hex":
        poly_str = hex(poly_int) 
        return poly_str
    elif poly_format == "bin":
        poly_str = bin(poly_int) 
        return poly_str
    elif poly_format == "alg":
        # If the polynomial given is 0, return "0"
        if poly_int == 0:
            return "0"

        # Get polynomial bit positions with non-zero coefficients in decreasing order
        poly_ones = get_bit_positions(poly_int)[::-1]

        # Generate polynomial str
        poly_terms = []
        for order in poly_ones:
            if order == 0:
                poly_terms.append("1")
            elif order == 1:
                poly_terms.append("x")
            else:
                poly_terms.append(f"x^{order}")
        poly_str = " + ".join(poly_terms) 
        return poly_str
    else:
        raise Exception(f"{poly_format} is not a valid polynomial format.")

