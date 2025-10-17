# ==============================================================================
# Binary XOR Tree Verilog Generator
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Generates Verilog code and a corresponding testbench for a binary XOR tree.
# The XOR logic is implemented using a binary tree structure for efficient 
# reduction of multiple input vectors.
#
# The generated Verilog module performs the bitwise XOR of {num_vectors}
# vectors, each of {bit_length} bits, concatenated into a single input bus
# of {num_vectors * bit_length} bits.
#
# VERILOG FUNCTIONALITY:
#
#     - Receives a {num_vectors * bit_length}-bit input representing the
#       concatenation of {num_vectors} vectors of {bit_length} bits each
#
#     - Outputs a {bit_length}-bit vector representing the XOR of all
#       input vectors
#
#     - The XOR operation is structured as a binary tree to optimize logic depth
#
# The corresponding testbench applies random input vectors and verifies that
# the output matches the expected XOR result.
#
# COMMAND-LINE INTERFACE:
#
#     This script accepts the following arguments:
#
#     - num_vectors  : Number of input vectors (positive integer)
#     - bit_length   : Length in bits of each vector (positive integer)
#     - -d, --dir    : Optional output directory (default: current directory)
#
#     Example usage:
#         $ python3 xor_tree_generator.py 8 32 --dir ./output
#
#     This will produce:
#         - src/xor_tree_256_32.v     : Verilog module file
#         - tb/tb_xor_tree_256_32.v  : Verilog testbench file
#
# NOTE:
#     - All logic is purely combinational
#     - Assumes inputs are stable during evaluation
# ==============================================================================

import argparse
import os
import random

def generate_src(num_vectors, bit_length):
    """
    Generate main module verilog code
    """
    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append("// Binary XOR Tree                                                                ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append("// Computes the bitwise XOR of multiple binary vectors using a binary tree        ")
    lines.append(f"// structure. The module receives a single input vector composed of {num_vectors}")
    lines.append(f"// concatenated {bit_length}-bit vectors (total of {num_vectors * bit_length} bits) and returns a {bit_length}-bit output")
    lines.append("// representing their bitwise XOR.                                                ")
    lines.append("//                                                                                 ")
    lines.append("// INPUT:                                                                          ")
    lines.append(f"//     - in_vectors : {num_vectors * bit_length}-bit input vector ({num_vectors} concatenated {bit_length}-bit binary vectors)")
    lines.append("//                                                                                 ")
    lines.append("// OUTPUT:                                                                         ")
    lines.append(f"//     - out_xor    : {bit_length}-bit output vector (bitwise XOR of all {num_vectors} input vectors)")
    lines.append("//                                                                                 ")
    lines.append("// NOTE:                                                                           ")
    lines.append("//     - The XOR operation is performed using a balanced binary tree to           ")
    lines.append("//       minimize logic depth.                                                    ")
    lines.append("// ============================================================================== ")
    lines.append("")

    # Module declaration
    lines.append(f"module xor_tree_{num_vectors}_{bit_length} (")
    lines.append(f"    input  wire [{num_vectors * bit_length}-1:0] in_vectors,")
    lines.append(f"    output wire [{bit_length}-1:0] out_xor")
    lines.append(");")
    lines.append("")

    # Unpack input
    lines.append("    // Unpack input vectors")
    for i in range(num_vectors):
        begin_idx = i * bit_length
        end_idx = (i+1) * bit_length - 1
        # Declaration
        lines.append(f"    wire [{bit_length}-1:0] vec_{0}_{i};")
        # Assignment
        lines.append(f"    assign vec_{0}_{i} = in_vectors[{end_idx}:{begin_idx}];")
    lines.append("")

    # Tree structure
    lines.append("    // XOR tree structure")
    current_level = [(0, i) for i in range(num_vectors)]  # List of (stage, index)
    stage = 1

    while len(current_level) > 1:
        next_level = []
        i = 0
        lines.append(f"    // Tree stage {stage}")
        while i < len(current_level):
            if i + 1 < len(current_level):
                a_stage, a_idx = current_level[i]
                b_stage, b_idx = current_level[i+1]
                new_idx = len(next_level)
                # Declaration
                lines.append(f"    wire [{bit_length}-1:0] vec_{stage}_{new_idx};")
                # Assignment
                lines.append(f"    assign vec_{stage}_{new_idx} = vec_{a_stage}_{a_idx} ^ vec_{b_stage}_{b_idx};")
                next_level.append((stage, new_idx))
                i += 2
            else:
                # Odd element, just propagate
                a_stage, a_idx = current_level[i]
                new_idx = len(next_level)
                # Declaration
                lines.append(f"    wire [{bit_length}-1:0] vec_{stage}_{new_idx};")
                # Assignment
                lines.append(f"    assign vec_{stage}_{new_idx} = vec_{a_stage}_{a_idx};")
                next_level.append((stage, new_idx))
                i += 1
        lines.append("")
        current_level = next_level
        stage += 1

    # Final output
    final_stage, final_idx = current_level[0]
    lines.append("    // Assign output")
    lines.append(f"    assign out_xor = vec_{final_stage}_{final_idx};")
    lines.append("endmodule")

    return "\n".join(lines)

def generate_random_integers(num_vectors, bit_length, seed=42):
    """
    Generates num_vectors random integers with at most bit_length bits each
    """
    random.seed(seed)
    max_val = 2**bit_length - 1
    return [random.randint(0, max_val) for _ in range(num_vectors)]

def xor_integers(int_list):
    """
    XOR all integers in a list of integers
    """
    result = 0
    for v in int_list:
        result ^= v
    return result


def random_computation_example(num_vectors, bit_length, seed=42):
    """
    Generate computation example for some random input 
    """
    # Generate random input
    code_input = generate_random_integers(num_vectors, bit_length, seed=seed)
    expected_code_output = xor_integers(code_input)
    return code_input, expected_code_output

def int_list_to_verilog_vector(int_list, bit_length):
    formated_int_list = [f"{bit_length}'d{v}" for v in int_list]
    return "{" + " ,".join(formated_int_list) + "}"

def generate_tb(num_vectors, bit_length):
    """
    Generate module testbench code
    """
    # Generate random test
    int_list_code_input, expected_code_output = random_computation_example(num_vectors, bit_length, seed=42)

    # Convert integers to verilog input format
    code_input = int_list_to_verilog_vector(int_list_code_input, bit_length)

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append("// Testbench for Binary XOR Tree                                                  ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                     ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                ")
    lines.append("//                                                                                 ")
    lines.append(f"// Testbench file for xor_tree_{num_vectors}_{bit_length}.v                        ")
    lines.append("//                                                                                 ")
    lines.append("// FUNCTIONALITY:                                                                  ")
    lines.append("//     - Instantiates the XOR tree module with parameters:                         ")
    lines.append(f"//         - Number of input vectors : {num_vectors}                               ")
    lines.append(f"//         - Bit-length per vector   : {bit_length}                                ")
    lines.append("//                                                                                 ")
    lines.append("//     - Applies random input values to the design                                 ")
    lines.append("//     - Computes the expected XOR result in simulation                            ")
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
    lines.append(f"module tb_xor_tree_{num_vectors}_{bit_length};")
    lines.append("")

    # Declare regs and wires
    lines.append(f"    reg [{num_vectors * bit_length}-1:0] in_vectors;")
    lines.append(f"    wire [{bit_length}-1:0] out_xor;")
    lines.append("")

    # Device Under Test (DUT) declaration
    lines.append(f"    xor_tree_{num_vectors}_{bit_length} DUT (")
    lines.append("        .in_vectors(in_vectors),")
    lines.append("        .out_xor(out_xor)")
    lines.append("    );")
    lines.append("")

    # Testing
    lines.append("    initial begin")
    lines.append("        #10")
    lines.append(f"        in_vectors = {code_input};")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        if (out_xor == {bit_length}'d{expected_code_output})")
    lines.append(f"            $display(\"Test Passed --> tb_xor_tree_{num_vectors}_{bit_length}\");")
    lines.append("        else")
    lines.append(f"            $display(\"Test Failed --> tb_xor_tree_{num_vectors}_{bit_length}\");")
    lines.append("")
    lines.append("        $stop;")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")
    
    return "\n".join(lines)


def generate_verilog_and_tb_to_files(num_vectors, bit_length, save_dir):
    """
    Generate verilog and testbench files and save them inside save_dir
    """
    # Create directory to put src and tb files
    src_dir = save_dir + "/src"
    tb_dir = save_dir + "/tb"
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tb_dir, exist_ok=True)

    # Set files path
    out_filename = f"xor_tree_{num_vectors}_{bit_length}.v"
    out_tb_filename = "tb_" + out_filename
    path_out_filename = src_dir + "/" + out_filename
    path_out_tb_filename = tb_dir + "/" + out_tb_filename

    # Generate and save verilog code
    verilog_code = generate_src(num_vectors, bit_length)
    with open(path_out_filename, "w") as f:
        f.write(verilog_code)
    print(f"Verilog generated in {path_out_filename}")

    # Generate and save tb files
    verilog_tb_code = generate_tb(num_vectors, bit_length)
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
        "Generate a Verilog module implementing a binary XOR tree and its corresponding "
        "testbench. The source file will be saved in the src/ directory as "
        "xor_tree_{num_vectors}_{bit_length}.v, and the testbench will be saved in the "
        "tb/ directory as tb_xor_tree_{num_vectors}_{bit_length}.v."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("num_vectors", type=positive_int, help="Number of input vectors (positive integer)")
    parser.add_argument("bit_length", type=positive_int, help="Size of each vector in bits (positive integer)")
    parser.add_argument("-d", "--dir", default=".", help="Directory to save files (default: current directory)")
    args = parser.parse_args()
    return args

# Main
def main():
    # Read command line arguments
    args = argument_parser()

    # Set parameters
    num_vectors = args.num_vectors  # Number of vectors
    bit_length = args.bit_length  # Vector bit length
    save_dir = os.path.abspath(args.dir)  # Get absolute path

    # Generate verilog code and testbench and save them to files
    generate_verilog_and_tb_to_files(num_vectors, bit_length, save_dir)

if __name__ == "__main__":
    main()