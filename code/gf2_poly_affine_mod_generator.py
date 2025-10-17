# ==============================================================================
# Verilog Generator for a(x)p(x) + c(x) modulo h(x) over GF(2)
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Generates Verilog code and a corresponding testbench to compute the expression:
#
#     (a(x)p(x) + c(x)) mod h(x)
#
# where a(x), p(x), c(x), and h(x) are binary polynomials over GF(2), meaning their
# coefficients are either 0 or 1. The input polynomial p(x) is variable, while
# a(x), c(x), and h(x) are constants defined at generation time.
#
# VERILOG FUNCTIONALITY:
#
#     - Receives a {bit_length}-bit input vector representing the polynomial p(x)
#
#     - Outputs a {out_bit_length}-bit vector representing the result of
#       (a(x)p(x) + c(x)) mod h(x), with multiplication, addition, and modular reduction
#       performed over GF(2)
#
#     - All arithmetic follows binary polynomial rules (modulo 2, no carries)
#
# The corresponding testbench applies random input values for p(x), computes the
# expected output in Python, and compares it against the Verilog module’s output.
#
# COMMAND-LINE INTERFACE:
#
#     This script accepts the following arguments:
#
#     - a            : Constant polynomial a(x) (positive integer)
#     - c            : Constant polynomial c(x) (non-negative integer)
#     - h            : Modulus polynomial h(x) (positive integer)
#     - bit_length   : Length in bits of the input polynomial p(x) (positive integer)
#     - -d, --dir    : Optional output directory (default: current directory)
#
#     Example usage:
#         $ python3 gf2_poly_affine_mod_generator.py 17 1 285 16 --dir ./output
#
#     This will produce:
#         - src/gf2_poly_affine_mod_16.v   : Verilog module file
#         - tb/tb_gf2_poly_affine_mod_16.v : Verilog testbench file
#         - Any necessary submodules and their respective testbenches saved inside
#           src/ and tb/ directories, respectively.
#
# NOTE:
#     - All arithmetic is performed over GF(2)
#     - The output bit-width is automatically determined from a(x), h(x), and {bit_length}
#     - The design is purely combinational
# ==============================================================================

from gf2_poly_utils import get_bit_positions, poly_degree, poly_mod, poly_affine_mod, int_poly_to_str

import argparse
import gf2_poly_affine_generator
import gf2_poly_mod_generator
import os
import random

def generate_src(a: int, c: int, h: int, bit_length: int) -> str:
    """
    Generate main module verilog code
    """

    # Get input and output bit lengths
    in_bit_length = bit_length
    out_bit_length = h.bit_length() - 1

    lines = []
    
    # Header
    lines.append("// ============================================================================== ")
    lines.append("// GF(2) Polynomial Affine Computation with Modular Reduction                    ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append(f"// Computes the expression a(x)p(x) + c(x) modulo h(x) over GF(2) for any input polynomial p(x).")
    lines.append(f"// All polynomials have binary coefficients (0 or 1).                             ")
    lines.append("//                                                                                 ")
    lines.append(f"// Constant polynomials a(x), c(x), and h(x) given as:                            ")
    lines.append(f"//     - a(x) = {int_poly_to_str(a, 'alg')}") 
    lines.append(f"//     - c(x) = {int_poly_to_str(c, 'alg')}") 
    lines.append(f"//     - h(x) = {int_poly_to_str(h, 'alg')}")
    lines.append("//                                                                                 ")
    lines.append(f"// INPUT:                                                                          ")
    lines.append(f"//     - in_poly   : {bit_length}-bit input vector representing polynomial p(x)       ")
    lines.append("//                                                                                 ")
    lines.append(f"// OUTPUT:                                                                         ")
    lines.append(f"//     - out_poly  : {out_bit_length}-bit output vector representing a(x)p(x) + c(x) modulo h(x)")
    lines.append("// ============================================================================== ")
    lines.append("")


    # Module declaration
    lines.append(f"module gf2_poly_affine_mod_{bit_length} (")
    lines.append(f"    input  wire [{in_bit_length}-1:0] in_poly,")
    lines.append(f"    output wire [{out_bit_length}-1:0] out_poly")
    lines.append(");")
    lines.append("")

    # Declare regs and wires
    affine_in_bit_length = in_bit_length
    affine_out_bit_length = in_bit_length + poly_degree(a)
    mod_in_bit_length = affine_out_bit_length
    mod_out_bit_length = out_bit_length
    lines.append("    // Declare regs and wires")
    lines.append(f"    wire [{in_bit_length}-1:0] w_in_affine;")
    lines.append(f"    wire [{affine_out_bit_length}-1:0] w_out_affine;")
    lines.append(f"    wire [{mod_in_bit_length}-1:0] w_in_mod;")
    lines.append(f"    wire [{mod_out_bit_length}-1:0] w_out_mod;")
    lines.append("")

    # Declare affine transformation module
    lines.append("    // Declare affine transformation module")
    lines.append(f"    gf2_poly_affine_{affine_in_bit_length} GF2_POLY_AFFINE_{affine_in_bit_length} (")
    lines.append("        .in_poly(w_in_affine),")
    lines.append("        .out_poly(w_out_affine)")
    lines.append("    );")
    lines.append("")

    # Declare modular reduction module
    lines.append("    // Declare modular reduction module")
    lines.append(f"    gf2_poly_mod_{mod_in_bit_length} GF2_POLY_MOD_{mod_in_bit_length} (")
    lines.append("        .in_poly(w_in_mod),")
    lines.append("        .out_poly(w_out_mod)")
    lines.append("    );")
    lines.append("")

    # Assign wires
    lines.append("    // Assign wires")
    lines.append("    assign w_in_affine = in_poly;")
    lines.append("    assign w_in_mod = w_out_affine;")
    lines.append("")

    # Assign output
    lines.append("    // Assign output")
    lines.append(f"    assign out_poly = w_out_mod;")
    lines.append("endmodule")

    return "\n".join(lines)

def generate_random_integers(num_vectors: int, bit_length: int, seed: int=42) -> list:
    """
    Generates num_vectors random integers with at most bit_length bits each
    """
    random.seed(seed)
    max_val = 2**bit_length - 1
    return [random.randint(0, max_val) for _ in range(num_vectors)]


def random_computation_example(a: int, c: int, h: int, bit_length: int, seed: int=42) -> tuple:
    """
    Generate computation example for some random input 
    """
    # Generate random input
    code_input = generate_random_integers(1, bit_length, seed=seed)[0]
    expected_code_output = poly_affine_mod(a, code_input, c, h)
    return code_input, expected_code_output

def generate_tb(a: int, c: int, h: int, bit_length: int) -> str:
    """
    Generate module testbench code
    """
    # Get input and output bit lengths
    in_bit_length = bit_length
    out_bit_length = h.bit_length() - 1

    # Generate random test
    code_input, expected_code_output = random_computation_example(a, c, h, bit_length)

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append("// Testbench for GF(2) Polynomial Affine Modular Computation                     ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append(f"// Testbench file for gf2_poly_affine_mod_{bit_length}.v              ")
    lines.append("//                                                                                 ")
    lines.append("// FUNCTIONALITY:                                                                  ")
    lines.append("//     - Instantiates the polynomial affine modular module with parameters:        ")
    lines.append(f"//         - Polynomial a(x) : {int_poly_to_str(a, 'alg')}")
    lines.append(f"//         - Polynomial c(x) : {int_poly_to_str(c, 'alg')}") 
    lines.append(f"//         - Modulus polynomial h(x): {int_poly_to_str(h, 'alg')}")
    lines.append(f"//         - Input bit length      : {bit_length}                                 ")
    lines.append("//                                                                                 ")
    lines.append("//     - Applies random input values to the design                                 ")
    lines.append("//     - Computes the expected result modulo h(x) in simulation                    ")
    lines.append("//     - Compares module output with expected result and reports mismatches        ")
    lines.append("//                                                                                 ")
    lines.append("// NOTE:                                                                           ")
    lines.append("//     - This testbench is self-checking                                           ")
    lines.append("//     - Simulation ends with a success or failure message                         ")
    lines.append("// ============================================================================== ")
    lines.append("")

    lines.append("`timescale 1ns/1ps")
    lines.append("")

    # Module declaration
    lines.append(f"module tb_gf2_poly_affine_mod_{bit_length};")
    lines.append("")

    # Declare regs and wires
    lines.append(f"    reg [{in_bit_length}-1:0] in_poly;")
    lines.append(f"    wire [{out_bit_length}-1:0] out_poly;")
    lines.append("")

    # Device Under Test (DUT) declaration
    lines.append(f"    gf2_poly_affine_mod_{bit_length} DUT (")
    lines.append("        .in_poly(in_poly),")
    lines.append("        .out_poly(out_poly)")
    lines.append("    );")
    lines.append("")

    # Testing
    lines.append("    initial begin")
    lines.append("        #10")
    lines.append(f"        in_poly = {bit_length}'d{code_input};")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        if (out_poly == {out_bit_length}'d{expected_code_output})")
    lines.append(f"            $display(\"Test Passed --> tb_gf2_poly_affine_mod_{bit_length}\");")
    lines.append("        else")
    lines.append(f"            $display(\"Test Failed --> tb_gf2_poly_affine_mod_{bit_length}\");")
    lines.append("")
    lines.append("        $stop;")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")

    return "\n".join(lines)

def generate_submodules_verilog_and_tb_to_files(a: int, c: int, h: int, bit_length: int, save_dir: str) -> None:
    """
    Generate submodules needed for this code to run:
        - gf2_poly_affine
        - gf2_poly_mod
    """

    # Compute parameters needed to generate gf2_poly_affine and gf2_poly_mod
    affine_in_bit_length = bit_length
    affine_out_bit_length = bit_length + poly_degree(a)
    mod_in_bit_length = affine_out_bit_length

    # Generate submodules
    gf2_poly_affine_generator.generate_verilog_and_tb_to_files(a, c, affine_in_bit_length, save_dir)
    gf2_poly_mod_generator.generate_verilog_and_tb_to_files(h, mod_in_bit_length, save_dir)

    return

def generate_verilog_and_tb_to_files(a: int, c: int, h: int, bit_length: int, save_dir: str) -> None:
    """
    Generate verilog and testbench files and save them inside save_dir
    """
    # Generate and save submodule files
    generate_submodules_verilog_and_tb_to_files(a, c, h, bit_length, save_dir)

    # Create directory to put src and tb files
    src_dir = save_dir + "/src"
    tb_dir = save_dir + "/tb"
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tb_dir, exist_ok=True)

    # Set files path
    out_filename = f"gf2_poly_affine_mod_{bit_length}.v"
    out_tb_filename = "tb_" + out_filename
    path_out_filename = src_dir + "/" + out_filename
    path_out_tb_filename = tb_dir + "/" + out_tb_filename

    # Generate and save verilog code
    verilog_code = generate_src(a, c, h, bit_length)
    with open(path_out_filename, "w") as f:
        f.write(verilog_code)
    print(f"Verilog generated in {path_out_filename}")

    # Generate and save tb files
    verilog_tb_code = generate_tb(a, c, h, bit_length)
    with open(path_out_tb_filename, "w") as f:
        f.write(verilog_tb_code)
    print(f"Verilog testbench generated in {path_out_tb_filename}")

def nonnegative_int(value):
    """
    Check if given parameter is a nonnegative integer
    """
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def positive_int(value):
    """
    Check if given parameter is a positive integer
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def argument_parser():
    """
    Parse command line arguments
    """

    description = (
        "Generate Verilog code and a corresponding testbench to compute the expression "
        "a(x)p(x) + c(x) modulo h(x) over GF(2), where a(x), c(x), and h(x) are constant "
        "binary polynomials represented as integers, and p(x) is a binary input polynomial "
        "of configurable bit-length. The generated Verilog module will be saved as "
        "src/gf2_poly_affine_mod_{bit_length}.v, and the testbench as "
        "tb/tb_gf2_poly_affine_mod_{bit_length}.v."
        "Necessary submodules and their testbenches are saved inside rtl/src/ and rtl/tb/."
    )
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("a", type=positive_int, help="Polynomial a(x) (positive integer)")
    parser.add_argument("c", type=nonnegative_int, help="Polynomial c(x) (nonnegative integer)")
    parser.add_argument("h", type=positive_int, help="Polynomial h(x) (positive integer)")
    parser.add_argument("bit_length", type=positive_int, help="Size of input p(x) in bits (positive integer)")
    parser.add_argument("-d", "--dir", default=".", help="Directory to save files (default: current directory)")
    args = parser.parse_args()

    return args

# Main
def main():
    # Read command line arguments
    args = argument_parser()

    # Set parameters
    h = args.h
    a = poly_mod(args.a, h) # simplify a(x) if possible
    c = poly_mod(args.c, h) # simplify c(x) if possible
    bit_length = args.bit_length
    save_dir = os.path.abspath(args.dir)  # Get absolute path

    # Generate verilog code and testbench and save them to files
    generate_verilog_and_tb_to_files(a, c, h, bit_length, save_dir)

if __name__ == "__main__":
    main()
