#!/bin/bash

# ==============================================================================
# Script for Compiling and Running Verilog Testbenches using ModelSim
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# Description : This script checks for the availability of ModelSim's `vsim`,
#               compiles the design files using `load.do`, and runs the provided
#               testbenches in batch mode.
#
# Usage       : ./run_tb.sh tb_example1 tb_example2 ...
#
# Notes:
#   - You must have ModelSim installed and accessible via your system PATH.
#   - If vsim is not in the PATH, you can manually set the VSIM variable below.
# ==============================================================================

# -----------------------------
# Configuration (Optional path override)
# -----------------------------
# Uncomment and edit if vsim is not in PATH:
# VSIM="$HOME/intelFPGA_lite/18.1/modelsim_ase/linuxaloem/vsim"
# VSIM="$HOME/intelFPGA_lite/18.1/modelsim_ase/bin/vsim"
# VSIM="$HOME/altera/15.0/modelsim_ase/bin/vsim"

# Use system vsim by default
VSIM=${VSIM:-vsim}

# -----------------------------
# Check if vsim is available
# -----------------------------
if ! command -v "$VSIM" &>/dev/null; then
    echo "[!] Error: ModelSim 'vsim' binary not found in PATH."
    echo
    echo "To fix this, either:"
    echo "  - Add the ModelSim bin folder to your PATH (e.g., ~/intelFPGA_lite/.../modelsim_ase/bin)"
    echo "  - Or set the VSIM variable manually in this script."
    exit 1
fi

# -----------------------------
# Collect testbench names
# -----------------------------
if [ "$#" -eq 0 ]; then
    echo "[!] No testbenches specified."
    echo "Usage: $0 <testbench1> [testbench2] ..."
fi

TESTBENCHES=("$@")

# -----------------------------
# Cleanup old library
# -----------------------------
rm -rf work 2>/dev/null

# -----------------------------
# Compile design
# -----------------------------
"$VSIM" -batch -do load.do

# -----------------------------
# Run each testbench
# -----------------------------
for tb in "${TESTBENCHES[@]}"; do
    echo -e "\n\nRunning testbench: $tb\n"
    "$VSIM" -voptargs="+acc" -batch -quiet "$tb" -do "run -all; quit"
done