// ============================================================================== 
// Testbench for Binary XOR Tree                                                  
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Testbench file for xor_tree_3_35.v                        
//                                                                                 
// FUNCTIONALITY:                                                                  
//     - Instantiates the XOR tree module with parameters:                         
//         - Number of input vectors : 3                               
//         - Bit-length per vector   : 35                                
//                                                                                 
//     - Applies random input values to the design                                 
//     - Computes the expected XOR result in simulation                            
//     - Compares module output with expected result and reports mismatches        
//                                                                                 
// NOTE:                                                                           
//     - This testbench is self-checking                                           
//     - Simulation ends with a success or failure message                         
// ============================================================================== 

`timescale 1ns/1ps

module tb_xor_tree_3_35;

    reg [105-1:0] in_vectors;
    wire [35-1:0] out_xor;

    xor_tree_3_35 DUT (
        .in_vectors(in_vectors),
        .out_xor(out_xor)
    );

    initial begin
        #10
        in_vectors = {35'd7041284509 ,35'd14066143831 ,35'd9548617438};

        #10
        if (out_xor == 35'd3707600148)
            $display("Test Passed --> tb_xor_tree_3_35");
        else
            $display("Test Failed --> tb_xor_tree_3_35");

        $stop;
    end

endmodule