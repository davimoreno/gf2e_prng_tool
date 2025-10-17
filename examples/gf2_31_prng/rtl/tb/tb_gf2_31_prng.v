// ============================================================================== 
// Testbench for Pseudorandom Number Generator (PRNG) over GF(2^31)              
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                    
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE              
//                                                                                 
// Testbench for gf2_31_prng.v                                        
//                                                                                 
// FUNCTIONALITY:                                                                  
//    - Instantiates the PRNG module defined over GF(2^31)                       
//     - Uses the affine recurrence relation:                                     
//                                                                                 
//           x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)                              
//                                                                                 
//     - Simulates PRNG behavior for a random input seed                          
//     - Iterate PRNG 100 times                                                   
//     - Compares PRNG output with a reference software model                     
//                                                                                 
// PARAMETERS:                                                                     
//         - Polynomial a(x) : x^4 + 1   // 31-bit vector 
//         - Polynomial c(x) : 1   // 31-bit vector 
//         - Modulus polynomial h(x): x^31 + x^13 + x^8 + x^3 + 1   // 32-bit irreducible polynomial
//                                                                                 
// NOTE:                                                                           
//     - All polynomials are over GF(2)                                            
//     - This testbench can be extended to perform automated checking              
// ============================================================================== 

`timescale 1ns/1ps

module tb_gf2_31_prng;

    // Declare regs and wires
    reg                    clk;
    reg                    rst;
    reg                    enable;
    reg  [31-1:0] seed;
    wire [31-1:0] prng_out;

    // Declare integer i used to iterate over the PRNG
    integer                    i;
    // Declare PRNG module
    gf2_31_prng DUT (
        .clk       (clk),
        .rst       (rst),
        .enable    (enable),
        .seed      (seed),
        .prng_out  (prng_out)
    );

    always #5 clk = ~clk;
    initial begin
        clk = 1'b0;
        rst = 1'b0;
        enable = 1'b0;
        seed = 31'd478163327;

        #10
        rst = 1'b1;

        #10
        rst = 1'b0;
        enable = 1'b1;

        // Iterate the PRNG 100 times
        i = 0;
        repeat (100) begin
            @(posedge clk);
            i = i + 1;
        end

        #10
        // Compare PRNG output with computation done by software
        if (prng_out == 31'd2137196284)
            $display("Test Passed --> tb_gf2_31_prng");
        else
            $display("Test Failed --> tb_gf2_31_prng");

        $stop;
    end

endmodule