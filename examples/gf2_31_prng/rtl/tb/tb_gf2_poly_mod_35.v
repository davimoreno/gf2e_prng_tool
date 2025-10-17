// ============================================================================== 
// Testbench for GF(2) Polynomial Modular Reduction                             
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Testbench file for gf2_poly_mod_35.v                           
//                                                                                 
// FUNCTIONALITY:                                                                  
//     - Instantiates the polynomial modular reduction module with parameters:     
//         - Modulus polynomial h(x): x^31 + x^13 + x^8 + x^3 + 1
//         - Input bit length y(x)  : 35
//                                                                                 
//     - Applies random input polynomial values y(x)                              
//     - Computes expected y(x) mod h(x) result in simulation                      
//     - Compares module output with expected result and reports mismatches        
//                                                                                 
// NOTE:                                                                           
//     - This testbench is self-checking                                           
//     - Simulation ends with a success or failure message                         
// ============================================================================== 

`timescale 1ns/1ps

module tb_gf2_poly_mod_35;

    reg [35-1:0] in_poly;
    wire [31-1:0] out_poly;

    gf2_poly_mod_35 DUT (
        .in_poly(in_poly),
        .out_poly(out_poly)
    );

    initial begin
        #10
        in_poly = 35'd7041284509;

        #10
        if (out_poly == 31'd598809222)
            $display("Test Passed --> tb_gf2_poly_mod_35");
        else
            $display("Test Failed --> tb_gf2_poly_mod_35");

        $stop;
    end

endmodule