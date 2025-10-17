# ==============================================================================
# ModelSim Load Script for Simulation
# ------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
#
# DESCRIPTION:
#     - Creates the default working library (`work`)
#     - Defines source and testbench directories
#     - Compiles all Verilog source (*.v) files in the RTL and testbench folders
#
# USAGE:
#     - Load this script in ModelSim with: `do load.do`
#
# NOTES:
#     - Paths are set relative to the current script location
#     - Assumes Verilog sources are organized in:
#         ../rtl/src  -> For design source files
#         ../rtl/tb   -> For testbench files
# ==============================================================================

# Create a library for working in
vlib work

set rtl  "../rtl"

# Common source and tests
set common_src  $rtl/src
set common_tb   $rtl/tb

vlog -quiet $common_src/*.v
vlog -quiet $common_tb/*.v

quit