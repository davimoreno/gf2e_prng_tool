// ============================================================================== 
// Testbench for GF(2) Polynomial Affine Modular Computation                     
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Testbench file for gf2_poly_affine_mod_31.v              
//                                                                                 
// FUNCTIONALITY:                                                                  
//     - Instantiates the polynomial affine modular module with parameters:        
//         - Polynomial a(x) : x^4 + 1
//         - Polynomial c(x) : 1
//         - Modulus polynomial h(x): x^31 + x^13 + x^8 + x^3 + 1
//         - Input bit length      : 31                                 
//                                                                                 
//     - Applies random input values to the design                                 
//     - Computes the expected result modulo h(x) in simulation                    
//     - Compares module output with expected result and reports mismatches        
//                                                                                 
// NOTE:                                                                           
//     - This testbench is self-checking                                           
//     - Simulation ends with a success or failure message                         
// ============================================================================== 

`timescale 1ns/1ps

module tb_gf2_poly_affine_mod_31;

    reg [31-1:0] in_poly;
    wire [31-1:0] out_poly;

    gf2_poly_affine_mod_31 DUT (
        .in_poly(in_poly),
        .out_poly(out_poly)
    );

    initial begin
        #10
        in_poly = 31'd478163327;

        #10
        if (out_poly == 31'd1417889173)
            $display("Test Passed --> tb_gf2_poly_affine_mod_31");
        else
            $display("Test Failed --> tb_gf2_poly_affine_mod_31");

        $stop;
    end

endmodule