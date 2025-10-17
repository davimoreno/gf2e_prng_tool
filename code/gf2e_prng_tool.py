# ==============================================================================
# Verilog Generator for a PRNG over GF(2^e) using Affine Recurrence
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Generates Verilog project for a Pseudorandom Number Generator (PRNG) based on 
# the affine recurrence relation:
#
#     x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)
#
# where all polynomials have binary coefficients over GF(2), and arithmetic is
# performed in the finite field GF(2^e), defined by the irreducible polynomial h(x).
# All elements in GF(2^e) have e-bits (referred here as {bit_length}-bits).
#
# The input polynomials a(x), c(x), and h(x) are specified as integers, with h(x)
# defining the field and a(x), c(x) controlling the recurrence dynamics.
#
# VERILOG FUNCTIONALITY:
#
#     - Receives a {bit_length}-bit input seed vector representing x₀(x)
#     - At each rising edge of clk, if enable is high, computes:
#
#         x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)
#
#     - Outputs the result as a {bit_length}-bit vector
#     - All arithmetic is over GF(2), including polynomial multiplication and modular
#       reduction with respect to h(x)
#
# PROJECT STRUCTURE:
#
#     Running this script with the appropriate arguments creates a project
#     directory named:
#
#         gf2_{e}_prng
#
#     inside the specified save directory (or current directory by default),
#     with the following subdirectory layout:
#
#         - rtl/src/      : Verilog module and submodules implementing the PRNG
#         - rtl/tb/       : Self-checking Verilog testbenchs
#         - modelsim/     : Auxiliary files for ModelSim simulation
#
#     File names are automatically generated using the input parameters.
#
# COMMAND-LINE INTERFACE:
#
#     This script accepts the following arguments:
#
#     - a            : Constant polynomial a(x) (positive integer)
#     - c            : Constant polynomial c(x) (non-negative integer)
#     - h            : Irreducible polynomial h(x) defining GF(2^e) (positive integer)
#     - -d, --dir    : Optional output directory (default: current directory)
#
#     Example usage:
#         $ python3 gf2e_prng_tool.py 23 5 285 --dir ./output
#
#     This will produce a project directory gf2_8_prng with:
#         - README.md              : Project details
#         - LICENSE                : License file\n"
#         - modelsim/              : ModelSim dir with simulation scripts
#         - rtl/src/gf2_8_prng.v   : Verilog PRNG module file
#         - rtl/tb/tb_gf2_8_prng.v : Verilog PRNG testbench file
#         - Any necessary submodules and their respective testbenches saved inside
#           rtl/src/ and rtl/tb/ directories, respectively.
#
# NOTE:
#     - The design uses GF(2) polynomial arithmetic with modular reduction by h(x)
#     - Output size is {bit_length}-bits, corresponding to GF(2^{bit_length})
#     - Sequential design driven by clk and reset
# ==============================================================================

from gf2_poly_utils import *

import argparse
import gf2_poly_affine_mod_generator
import os
import random
import shutil

def create_modelsim_dir(project_dir: str) -> None:
    """
    Copy the base modelsim dir to the project directory
    """
    # Absolute path to the dir containing this script 
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Absolute path to the base modelsim dir
    modelsim_dir = os.path.abspath(os.path.join(script_dir, "..", "modelsim"))

    # Absolute path to the destination project dir
    project_dir = os.path.abspath(project_dir)

    # Make sure destination project directory exists
    os.makedirs(project_dir, exist_ok=True)

    # Construct the modelsim dir inside destination project dir
    dest_modelsim_dir = os.path.join(project_dir, "modelsim")

    # Copy modelsim dir files
    shutil.copytree(modelsim_dir, dest_modelsim_dir, dirs_exist_ok=True)
    # print(f"Copied {modelsim_dir} -> {dest_modelsim_dir}")

    return

def copy_license(project_dir: str) -> None:
    """
    Copy LICENSE file to project directory
    """

    # Absolute path to the dir containing this script 
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Absolute path to the base LICENSE file
    license_file_path = os.path.abspath(os.path.join(script_dir, "..", "LICENSE"))

    # Absolute path to the destination project dir
    project_dir = os.path.abspath(project_dir)

    # Make sure destination project directory exists
    os.makedirs(project_dir, exist_ok=True)

    # Copy the LICENSE file
    shutil.copy(license_file_path, project_dir)

    return

def create_readme(a: int, c: int, h: int, project_dir: str) -> None:
    """
    Create README.md for created project in the project directory 
    """
    # Get finite field GF(2^e) order
    e = bit_length = poly_degree(h)

    lines = []
    # Header
    lines.append(f"# Pseudorandom Number Generator (PRNG) over GF(2^{e})")
    lines.append("")
    lines.append("Author      : Davi Moreno")
    lines.append("Affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE")
    lines.append("")
    lines.append("Implements a PRNG based on the affine recurrence relation:")
    lines.append("```")
    lines.append("    x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)")
    lines.append("```")
    lines.append("All polynomials have binary coefficients (0 or 1). The recurrence operates")
    lines.append(f"over the finite field GF(2^{e}), defined by the irreducible polynomial h(x).")
    lines.append("")
    lines.append("Constant polynomials given as:")
    lines.append(f"- a(x) = {int_poly_to_str(a, 'alg')}   // {bit_length}-bit vector") 
    lines.append(f"- c(x) = {int_poly_to_str(c, 'alg')}   // {bit_length}-bit vector") 
    lines.append(f"- h(x) = {int_poly_to_str(h, 'alg')}   // {bit_length + 1}-bit irreducible polynomial")
    lines.append("")
    lines.append("Project structure:")
    lines.append("```")
    lines.append(f"    gf2_{e}_prng/")
    lines.append("    ├── rtl/")
    lines.append("    │   ├── src/       # Verilog modules")
    lines.append("    │   └── tb/        # Testbenches")
    lines.append("    ├── modelsim/      # Simulation scripts")
    lines.append("    ├── LICENSE        # License file")
    lines.append("    └── README.md      # Project details")
    lines.append("```")
    lines.append("")

    readme_text = "\n".join(lines)

    # Absolute path to the destination project dir
    project_dir = os.path.abspath(project_dir)

    # Make sure destination project directory exists
    os.makedirs(project_dir, exist_ok=True)

    # Save README.md file
    path_out_filename = os.path.join(project_dir, "README.md")
    with open(path_out_filename, "w") as f:
        f.write(readme_text)
    # print(f"README generated in {path_out_filename}")

    return "\n".join(lines)

def generate_src(a: int, c: int, h: int) -> str:
    """
    Generate main module verilog code
    """
    # Compute the bit length of the elements in the GF(2^e), defined by the irreducible polynomial h(x)
    e = bit_length = poly_degree(h)

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append(f"// Pseudorandom Number Generator (PRNG) over GF(2^{e})                             ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                    ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE              ")
    lines.append("//                                                                                 ")
    lines.append("// Implements a PRNG based on the affine recurrence relation:                     ")
    lines.append("//                                                                                 ")
    lines.append("//     x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)                                    ")
    lines.append("//                                                                                 ")
    lines.append("// All polynomials have binary coefficients (0 or 1). The recurrence operates     ")
    lines.append(f"// over the finite field GF(2^{e}), defined by the irreducible polynomial h(x).")
    lines.append("//                                                                                 ")
    lines.append("// Constant polynomials given as:                                                 ")
    lines.append(f"//     - a(x) = {int_poly_to_str(a, 'alg')}   // {bit_length}-bit vector") 
    lines.append(f"//     - c(x) = {int_poly_to_str(c, 'alg')}   // {bit_length}-bit vector") 
    lines.append(f"//     - h(x) = {int_poly_to_str(h, 'alg')}   // {bit_length + 1}-bit irreducible polynomial")
    lines.append("//                                                                                 ")
    lines.append("// INPUTS:                                                                         ")
    lines.append("//     - clk       : Clock signal                                                  ")
    lines.append("//     - rst       : Synchronous active-high reset                                 ")
    lines.append("//     - enable    : When high, triggers the generation of the next PRNG value     ")
    lines.append(f"//     - seed      : Initial value x_0 ({bit_length}-bit input vector)              ")
    lines.append("//                                                                                 ")
    lines.append("// OUTPUT:                                                                         ")
    lines.append(f"//     - prng_out  : Pseudorandom output ({bit_length}-bit output vector)         ")
    lines.append("//                                                                                 ")
    lines.append("// NOTE:                                                                           ")
    lines.append("//     - All arithmetic is performed over GF(2), with reduction modulo h(x).      ")
    lines.append("// ============================================================================== ")
    lines.append("")

    # Module declaration
    lines.append(f"module gf2_{e}_prng (")
    lines.append("    input  wire              clk,")
    lines.append("    input  wire              rst,        // Reset signal (active high)")
    lines.append("    input  wire              enable,     // Enable signal for updating state")
    lines.append(f"    input  wire [{bit_length}-1:0]     seed,       // Initial polynomial/condition")
    lines.append(f"    output wire [{bit_length}-1:0]     prng_out    // Output of current PRNG state")
    lines.append(");")
    lines.append("")

    # Declare regs and wires
    lines.append(f"    // Internal state register holds current PRNG state")
    lines.append(f"    reg [{bit_length}-1:0] state;")
    lines.append("")
    lines.append(f"    // Wire to hold next PRNG state after applying recurrence")
    lines.append(f"    wire [{bit_length}-1:0] next_state;")
    lines.append("")

    # Declare module that computes a(x)x_n(x) + c(x)(mod h(x))
    lines.append(f"    // Declare module that computes recurrence relation in GF(2^{bit_length})")
    lines.append(f"    gf2_poly_affine_mod_{bit_length} GF2_POLY_AFFINE_MOD_{bit_length} (")
    lines.append(f"        .in_poly(state),")
    lines.append(f"        .out_poly(next_state)")
    lines.append(f"    );")
    lines.append("")

    # PRNG update output logic
    lines.append(f"    // PRNG state update logic")
    lines.append(f"    always @(posedge clk) begin")
    lines.append(f"        if (rst)")
    lines.append(f"            state <= seed;                  // Load seed on reset")
    lines.append(f"        else if (enable)")
    lines.append(f"            state <= next_state;            // Update state only when enabled")
    lines.append(f"    end")
    lines.append("")

    # Assign PRNG output
    lines.append(f"    // Assign PRNG output")
    lines.append(f"    assign prng_out = state;")
    lines.append("")

    lines.append("endmodule")

    return "\n".join(lines)

def generate_random_integers(num_vectors, bit_length, seed=42):
    """
    Generates num_vectors random integers with at most bit_length bits each
    """
    random.seed(seed)
    max_val = 2**bit_length - 1
    return [random.randint(0, max_val) for _ in range(num_vectors)]

def random_computation_example(a, c, h, seed=42):
    """
    Generate computation example for some random input 
    """
    # Compute input bit length
    bit_length = poly_degree(h)
    
    # Generate random input
    code_input = generate_random_integers(1, bit_length, seed=seed)[0]

    # Iterate 100 times the PRNG
    prng_in = code_input
    for _ in range(100):
        prng_out = poly_affine_mod(a, prng_in, c, h)
        prng_in = prng_out

    expected_code_output = prng_out

    return code_input, expected_code_output

def generate_tb(a: int, c: int, h: int) -> str:
    """
    Generate module testbench code
    """
    # Compute the bit length of the elements in the GF(2^e), defined by the irreducible polynomial h(x)
    e = bit_length = poly_degree(h)

    # Generate random test
    code_input, expected_code_output = random_computation_example(a, c, h, seed=42)

    lines = []

    # Header
    lines.append("// ============================================================================== ")
    lines.append(f"// Testbench for Pseudorandom Number Generator (PRNG) over GF(2^{e})              ")
    lines.append("// ------------------------------------------------------------------------------ ")
    lines.append("// @author      : Davi Moreno                                                    ")
    lines.append("// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE              ")
    lines.append("//                                                                                 ")
    lines.append(f"// Testbench for gf2_{e}_prng.v                                        ")
    lines.append("//                                                                                 ")
    lines.append("// FUNCTIONALITY:                                                                  ")
    lines.append(f"//    - Instantiates the PRNG module defined over GF(2^{e})                       ")
    lines.append("//     - Uses the affine recurrence relation:                                     ")
    lines.append("//                                                                                 ")
    lines.append("//           x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)                              ")
    lines.append("//                                                                                 ")
    lines.append("//     - Simulates PRNG behavior for a random input seed                          ")
    lines.append("//     - Iterate PRNG 100 times                                                   ")
    lines.append("//     - Compares PRNG output with a reference software model                     ")
    lines.append("//                                                                                 ")
    lines.append("// PARAMETERS:                                                                     ")
    lines.append(f"//         - Polynomial a(x) : {int_poly_to_str(a, 'alg')}   // {bit_length}-bit vector ")
    lines.append(f"//         - Polynomial c(x) : {int_poly_to_str(c, 'alg')}   // {bit_length}-bit vector ") 
    lines.append(f"//         - Modulus polynomial h(x): {int_poly_to_str(h, 'alg')}   // {bit_length + 1}-bit irreducible polynomial")
    lines.append("//                                                                                 ")
    lines.append("// NOTE:                                                                           ")
    lines.append("//     - All polynomials are over GF(2)                                            ")
    lines.append("//     - This testbench can be extended to perform automated checking              ")
    lines.append("// ============================================================================== ")
    lines.append("")

    lines.append("`timescale 1ns/1ps")
    lines.append("")

    # Module declaration
    lines.append(f"module tb_gf2_{e}_prng;")
    lines.append("")

    # Declare regs and wires
    lines.append(f"    // Declare regs and wires")
    lines.append(f"    reg                    clk;")
    lines.append(f"    reg                    rst;")
    lines.append(f"    reg                    enable;")
    lines.append(f"    reg  [{bit_length}-1:0] seed;")
    lines.append(f"    wire [{bit_length}-1:0] prng_out;")
    lines.append("")

    lines.append(f"    // Declare integer i used to iterate over the PRNG")
    lines.append(f"    integer                    i;")

    # Declare PRNG module
    lines.append(f"    // Declare PRNG module")
    lines.append(f"    gf2_{e}_prng DUT (")
    lines.append(f"        .clk       (clk),")
    lines.append(f"        .rst       (rst),")
    lines.append(f"        .enable    (enable),")
    lines.append(f"        .seed      (seed),")
    lines.append(f"        .prng_out  (prng_out)")
    lines.append(f"    );")
    lines.append("")

    # Create clock logic
    lines.append(f"    always #5 clk = ~clk;")

    # Testing
    lines.append("    initial begin")
    lines.append(f"        clk = 1'b0;")
    lines.append(f"        rst = 1'b0;")
    lines.append(f"        enable = 1'b0;")
    lines.append(f"        seed = {bit_length}'d{code_input};")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        rst = 1'b1;")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        rst = 1'b0;")
    lines.append(f"        enable = 1'b1;")
    lines.append("")
    lines.append(f"        // Iterate the PRNG 100 times")
    lines.append(f"        i = 0;")
    lines.append(f"        repeat (100) begin")
    lines.append(f"            @(posedge clk);")
    lines.append(f"            i = i + 1;")
    lines.append(f"        end")
    lines.append("")
    lines.append("        #10")
    lines.append(f"        // Compare PRNG output with computation done by software")
    lines.append(f"        if (prng_out == {bit_length}'d{expected_code_output})")
    lines.append(f"            $display(\"Test Passed --> tb_gf2_{e}_prng\");")
    lines.append("        else")
    lines.append(f"            $display(\"Test Failed --> tb_gf2_{e}_prng\");")
    lines.append("")
    lines.append("        $stop;")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")

    return "\n".join(lines)


def generate_submodules_verilog_and_tb_to_files(a: int, c: int, h: int, save_dir: str) -> None:
    """
    Generate submodules needed for this code to run:
        - gf2_poly_affine_mod
    """

    # Compute parameters needed to generate gf2_poly_affine_mod
    bit_length = poly_degree(h)

    # Generate submodules
    gf2_poly_affine_mod_generator.generate_verilog_and_tb_to_files(a, c, h, bit_length, save_dir)

    return

def generate_verilog_and_tb_to_files(a: int, c: int, h: int, save_dir: str) -> None:
    """
    Generate verilog and testbench files and save them inside save_dir
    """
    # Generate and save submodule src and tb files
    generate_submodules_verilog_and_tb_to_files(a, c, h, save_dir)

    # Create directory to put src and tb files
    src_dir = save_dir + "/src"
    tb_dir = save_dir + "/tb"
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tb_dir, exist_ok=True)

    # Set files path
    e = poly_degree(h)
    out_filename = f"gf2_{e}_prng.v"
    out_tb_filename = "tb_" + out_filename
    path_out_filename = src_dir + "/" + out_filename
    path_out_tb_filename = tb_dir + "/" + out_tb_filename

    # Generate and save verilog code
    verilog_code = generate_src(a, c, h)
    with open(path_out_filename, "w") as f:
        f.write(verilog_code)
    print(f"Verilog generated in {path_out_filename}")

    # Generate and save tb files
    verilog_tb_code = generate_tb(a, c, h)
    with open(path_out_tb_filename, "w") as f:
        f.write(verilog_tb_code)
    print(f"Verilog testbench generated in {path_out_tb_filename}")

def generate_project(a: int, c: int, h: int, save_dir: str) -> None:
    """
    Create project dir
    Create subdir rtl with all src and tb files
    Create subdir modelsim with simulation files
    """
    # Create project directory
    e = poly_degree(h)
    project_dir = save_dir + f"/gf2_{e}_prng"
    os.makedirs(project_dir, exist_ok=True)

    # Create RTL directory to save src and tb files
    rtl_dir = project_dir + "/rtl"
    os.makedirs(rtl_dir, exist_ok=True)

    # Generate project src and tb files inside rtl_dir
    generate_verilog_and_tb_to_files(a, c, h, rtl_dir)

    # Copy base modelsim dir to project_dir to help with simulation
    create_modelsim_dir(project_dir)

    # Add README.md to project
    create_readme(a, c, h, project_dir)

    # Copy LICENSE file to project
    copy_license(project_dir)

    return

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
        "  ___ ___ ___ ___   ___ ___ _  _  ___   _____ ___   ___  _    \n"
        " / __| __|_  ) __| | _ \\ _ \\ \\| |/ __| |_   _/ _ \\ / _ \\| |   \n"
        "| (_ | _| / /| _|  |  _/   / .` | (_ |   | || (_) | (_) | |__ \n"
        " \\___|_| /___|___| |_| |_|_\\_|\\_|\\___|   |_| \\___/ \\___/|____|\n"
        "                   by Davi Moreno (@davimoreno)\n\n"
        "Generate Verilog code and a corresponding testbench for a Pseudorandom Number "
        "Generator (PRNG) based on an affine recurrence relation over GF(2^e), defined by\n\n"
        "x_{n+1}(x) = a(x)x_n(x) + c(x) mod h(x).\n\nThe irreducible polynomial h(x) defines "
        "the extension field GF(2^e), and the constants a(x) and c(x) are binary polynomials "
        "represented as integers.\n\nAll generated files will be saved inside the directory "
        "gf2_{e}_prng, including:\n"
        "    - README.md                       : Project details\n"
        "    - LICENSE                         : License file\n"
        "    - modelsim/                       : ModelSim simulation scripts\n"
        "    - rtl/src/gf2_{e}_prng.v          : Verilog PRNG module file\n"
        "    - rtl/tb/tb_gf2_{e}_prng.v        : Verilog PRNG testbench file\n"
        "    - Necessary submodules and their testbenches inside rtl/src/ and rtl/tb/\n"
    )

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("a", type=positive_int, help="Polynomial a(x) (positive integer)")
    parser.add_argument("c", type=nonnegative_int, help="Polynomial c(x) (nonnegative integer)")
    parser.add_argument("h", type=positive_int, help="Irreducible polynomial h(x) (positive integer)")
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
    save_dir = os.path.abspath(args.dir)  # Get absolute path

    # Generate PRNG project from the given parameters
    generate_project(a, c, h, save_dir)

if __name__ == "__main__":
    main()
