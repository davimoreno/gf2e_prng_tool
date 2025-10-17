// ============================================================================== 
// Testbench for Binary XOR Tree                                                  
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Testbench file for xor_tree_5_31.v                        
//                                                                                 
// FUNCTIONALITY:                                                                  
//     - Instantiates the XOR tree module with parameters:                         
//         - Number of input vectors : 5                               
//         - Bit-length per vector   : 31                                
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

module tb_xor_tree_5_31;

    reg [155-1:0] in_vectors;
    wire [31-1:0] out_xor;

    xor_tree_5_31 DUT (
        .in_vectors(in_vectors),
        .out_xor(out_xor)
    );

    initial begin
        #10
        in_vectors = {31'd478163327 ,31'd107420369 ,31'd1181241943 ,31'd1051802512 ,31'd958682846};

        #10
        if (out_xor == 31'd1528435895)
            $display("Test Passed --> tb_xor_tree_5_31");
        else
            $display("Test Failed --> tb_xor_tree_5_31");

        $stop;
    end

endmodule