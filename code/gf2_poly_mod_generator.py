# ==============================================================================
# Verilog Generator for Polynomial Reduction y(x) mod h(x) over GF(2)
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Generates Verilog code and a corresponding testbench to compute the polynomial
# reduction operation:
#
#     y(x) mod h(x)
#
# where y(x) and h(x) are binary polynomials over GF(2), with coefficients either
# 0 or 1. The input polynomial y(x) is variable and has at most {y_bit_length} bits,
# while h(x) is a fixed polynomial defined at generation time.
#
# VERILOG FUNCTIONALITY:
#
#     - Receives a {y_bit_length}-bit input vector representing polynomial y(x)
#
#     - Outputs a {out_bit_length}-bit vector representing the remainder of
#       y(x) modulo h(x)
#
#     - All arithmetic follows binary polynomial rules (modulo 2, no carries)
#
# The corresponding testbench applies random inputs for y(x), computes the expected
# remainder in Python, and compares it against the Verilog module’s output.
#
# COMMAND-LINE INTERFACE:
#
#     This script accepts the following arguments:
#
#     - h            : Irreducible polynomial h(x) (positive integer)
#     - y_bit_length : Bit length of the input polynomial y(x) to be reduced (positive integer)
#     - -d, --dir    : Optional output directory (default: current directory)
#
#     Example usage:
#         $ python3 gf2_poly_mod_generator.py 285 16 --dir ./output
#
#     This will produce:
#         - src/gf2_poly_mod_16.v          : Verilog module file
#         - tb/tb_gf2_poly_mod_16.v        : Verilog testbench file
#         - Any necessary submodules and their respective testbenches saved inside
#           src/ and tb/ directories, respectively.
#
# NOTE:
#     - All arithmetic is performed over GF(2)
#     - The output bit-width is determined by the degree of h(x)
#     - The design is purely combinational
# ==============================================================================

from gf2_poly_utils import poly_degree, poly_mod, int_poly_to_str

import argparse
import os
import random
import xor_tree_generator

def get_reduction_constants(h, y_bit_length):
    """
    Generate constants needed for the reduction step
    """
    # Get polynomials degrees
    deg_h = poly_degree(h)
    deg_y = y_bit_length-1

    # Compute number of constants needed
    num_consts = max(deg_y - deg_h + 1, 0)

    # Compute constants
    consts = []
    for i in range(num_consts):
        y = 1 << (deg_h + i)
        const = poly_mod(y, h)
        consts.append(const)

    return consts

def generate_src(h, y_bit_length):
    """
    Generate main module verilog code
    """

    # Get parameters needed to implement the code
    h_bit_length = h.bit_length()
    in_bit_length = y_bit_length
    out_bit_length = h_bit_length - 1
    reduction_constants = get_reduction_constants(h, y_bit_length)

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append("// GF(2) Polynomial Modular Reduction                                            ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append(f"// Computes the polynomial reduction y(x) mod h(x) over GF(2), for any input       ")
    lines.append(f"// polynomial y(x) with at most {y_bit_length} bits.                              ")
    lines.append("// All polynomials have binary coefficients (0 or 1).                             ")
    lines.append("//                                                                                 ")
    lines.append(f"// Constant polynomial h(x) given as:                                             ")
    lines.append(f"//     - h(x) = {int_poly_to_str(h, 'alg')}")
    lines.append("//                                                                                 ")
    lines.append(f"// INPUT:                                                                          ")
    lines.append(f"//     - in_poly   : {in_bit_length}-bit input vector representing polynomial y(x)  ")
    lines.append("//                                                                                 ")
    lines.append(f"// OUTPUT:                                                                         ")
    lines.append(f"//     - out_poly  : {out_bit_length}-bit output vector representing y(x) mod h(x)  ")
    lines.append("// ============================================================================== ")
    lines.append("")


    # Module declaration
    lines.append(f"module gf2_poly_mod_{y_bit_length} (")
    lines.append(f"    input  wire [{in_bit_length}-1:0] in_poly,")
    lines.append(f"    output wire [{out_bit_length}-1:0] out_poly")
    lines.append(");")
    lines.append("")

    # Declare regs and wires
    xor_tree_num_vectors = len(reduction_constants) + 1
    xor_tree_bit_length = out_bit_length
    lines.append("    // Declare regs and wires")
    lines.append(f"    wire [{xor_tree_num_vectors * xor_tree_bit_length}-1:0] w_in_vectors;")
    lines.append(f"    wire [{xor_tree_bit_length}-1:0] w_out_xor;")
    lines.append("")

    # Declare XOR tree module
    lines.append("    // Declare XOR tree module")
    lines.append(f"    xor_tree_{xor_tree_num_vectors}_{xor_tree_bit_length} XOR_TREE_{xor_tree_num_vectors}_{xor_tree_bit_length} (")
    lines.append("        .in_vectors(w_in_vectors),")
    lines.append("        .out_xor(w_out_xor)")
    lines.append("    );")
    lines.append("")

    # Reduction step
    lines.append("    // Assign inputs to the XOR tree")
    for i,constant in enumerate(reduction_constants):
        y_idx = out_bit_length + i
        lines.append(f"    assign w_in_vectors[{(i+1) * xor_tree_bit_length}-1:{i * xor_tree_bit_length}] = in_poly[{y_idx}]? {xor_tree_bit_length}'d{constant} : {xor_tree_bit_length}'d{0};")
    # Assign the least signficant bits of input y (these bits are not affected by the reduction step)
    lines.append(f"    assign w_in_vectors[{xor_tree_num_vectors * xor_tree_bit_length}-1:{(xor_tree_num_vectors-1) * xor_tree_bit_length}] = in_poly[{xor_tree_bit_length}-1:0];")
    lines.append("")

    # Assign output
    lines.append("    // Assign output")
    lines.append(f"    assign out_poly = w_out_xor;")
    lines.append("endmodule")

    return "\n".join(lines)

def generate_random_integers(num_vectors, bit_length, seed=42):
    """
    Generates num_vectors random integers with at most bit_length bits each
    """
    random.seed(seed)
    max_val = 2**bit_length - 1
    return [random.randint(0, max_val) for _ in range(num_vectors)]

def random_computation_example(h, y_bit_length, seed=42):
    """
    Generate computation example for some random input 
    """
    # Generate random input
    code_input = generate_random_integers(1, y_bit_length, seed=seed)[0]
    expected_code_output = poly_mod(code_input, h)
    return code_input, expected_code_output

def generate_tb(h, y_bit_length):
    """
    Generate module testbench code
    """
    # Generate random test
    code_input, expected_code_output = random_computation_example(h, y_bit_length, seed=42)

    # Get parameters needed to implement the code
    h_bit_length = len(f"{h:b}")
    in_bit_length = y_bit_length
    out_bit_length = h_bit_length - 1

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append("// Testbench for GF(2) Polynomial Modular Reduction                             ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append(f"// Testbench file for gf2_poly_mod_{y_bit_length}.v                           ")
    lines.append("//                                                                                 ")
    lines.append("// FUNCTIONALITY:                                                                  ")
    lines.append("//     - Instantiates the polynomial modular reduction module with parameters:     ")
    lines.append(f"//         - Modulus polynomial h(x): {int_poly_to_str(h, 'alg')}")
    lines.append(f"//         - Input bit length y(x)  : {y_bit_length}") 
    lines.append("//                                                                                 ")
    lines.append("//     - Applies random input polynomial values y(x)                              ")
    lines.append("//     - Computes expected y(x) mod h(x) result in simulation                      ")
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
    lines.append(f"module tb_gf2_poly_mod_{y_bit_length};")
    lines.append("")

    # Declare regs and wires
    lines.append(f"    reg [{in_bit_length}-1:0] in_poly;")
    lines.append(f"    wire [{out_bit_length}-1:0] out_poly;")
    lines.append("")

    # Device Under Test (DUT) declaration
    lines.append(f"    gf2_poly_mod_{y_bit_length} DUT (")
    lines.append("        .in_poly(in_poly),")
    lines.append("        .out_poly(out_poly)")
    lines.append("    );")
    lines.append("")

    # Testing
    lines.append("    initial begin")
    lines.append("        #10")
    lines.append(f"        in_poly = {in_bit_length}'d{code_input};")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        if (out_poly == {out_bit_length}'d{expected_code_output})")
    lines.append(f"            $display(\"Test Passed --> tb_gf2_poly_mod_{y_bit_length}\");")
    lines.append("        else")
    lines.append(f"            $display(\"Test Failed --> tb_gf2_poly_mod_{y_bit_length}\");")
    lines.append("")
    lines.append("        $stop;")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")

    return "\n".join(lines)

def generate_submodules_verilog_and_tb_to_files(h, y_bit_length, save_dir):
    """
    Generate submodules needed for this code to run:
        - xor_tree
    """
    # Get XOR tree parameters
    h_bit_length = h.bit_length()
    out_bit_length = h_bit_length - 1 
    num_vectors = max(y_bit_length - out_bit_length + 1, 0)
    bit_length = out_bit_length

    # Generate and save XOR tree verilog and testbench files
    xor_tree_generator.generate_verilog_and_tb_to_files(num_vectors, bit_length, save_dir)

def generate_verilog_and_tb_to_files(h, y_bit_length, save_dir):
    """
    Generate verilog and testbench files and save them inside save_dir
    """
    # Generate and save submodule files
    generate_submodules_verilog_and_tb_to_files(h, y_bit_length, save_dir)

    # Create directory to put src and tb files
    src_dir = save_dir + "/src"
    tb_dir = save_dir + "/tb"
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tb_dir, exist_ok=True)

    # Set files path
    out_filename = f"gf2_poly_mod_{y_bit_length}.v"
    out_tb_filename = "tb_" + out_filename
    path_out_filename = src_dir + "/" + out_filename
    path_out_tb_filename = tb_dir + "/" + out_tb_filename

    # Generate and save verilog code
    verilog_code = generate_src(h, y_bit_length)
    with open(path_out_filename, "w") as f:
        f.write(verilog_code)
    print(f"Verilog generated in {path_out_filename}")

    # Generate and save tb files
    verilog_tb_code = generate_tb(h, y_bit_length)
    with open(path_out_tb_filename, "w") as f:
        f.write(verilog_tb_code)
    print(f"Verilog testbench generated in {path_out_tb_filename}")

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
        "Generate Verilog code and a corresponding testbench to compute the polynomial "
        "reduction y(x) mod h(x) over GF(2), where h(x) is a constant binary polynomial "
        "and y(x) is a binary input polynomial of configurable bit-length. "
        "The generated Verilog module will be saved as "
        "src/gf2_poly_mod_{y_bit_length}.v, and the testbench as "
        "tb/tb_gf2_poly_mod_{y_bit_length}.v."
        "Necessary submodules and their testbenches are saved inside rtl/src/ and rtl/tb/."
    )
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("h", type=positive_int, help="Polynomial h(x) (positive integer)")
    parser.add_argument("y_bit_length", type=positive_int, help="Bit length of polynomial y(x) to be reduced (positive integer)")
    parser.add_argument("-d", "--dir", default=".", help="Directory to save files (default: current directory)")
    args = parser.parse_args()
    return args

# Main
def main():
    # Read command line arguments
    args = argument_parser()

    # Set parameters
    h = args.h
    y_bit_length = args.y_bit_length  # Vector bit length
    save_dir = os.path.abspath(args.dir)  # Get absolute path

    # Generate verilog code and testbench and save them to files
    generate_verilog_and_tb_to_files(h, y_bit_length, save_dir)

if __name__ == "__main__":
    main()