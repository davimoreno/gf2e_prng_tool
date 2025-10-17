// ============================================================================== 
// Pseudorandom Number Generator (PRNG) over GF(2^31)                             
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                    
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE              
//                                                                                 
// Implements a PRNG based on the affine recurrence relation:                     
//                                                                                 
//     x_{n+1}(x) = a(x)·x_n(x) + c(x) mod h(x)                                    
//                                                                                 
// All polynomials have binary coefficients (0 or 1). The recurrence operates     
// over the finite field GF(2^31), defined by the irreducible polynomial h(x).
//                                                                                 
// Constant polynomials given as:                                                 
//     - a(x) = x^4 + 1   // 31-bit vector
//     - c(x) = 1   // 31-bit vector
//     - h(x) = x^31 + x^13 + x^8 + x^3 + 1   // 32-bit irreducible polynomial
//                                                                                 
// INPUTS:                                                                         
//     - clk       : Clock signal                                                  
//     - rst       : Synchronous active-high reset                                 
//     - enable    : When high, triggers the generation of the next PRNG value     
//     - seed      : Initial value x_0 (31-bit input vector)              
//                                                                                 
// OUTPUT:                                                                         
//     - prng_out  : Pseudorandom output (31-bit output vector)         
//                                                                                 
// NOTE:                                                                           
//     - All arithmetic is performed over GF(2), with reduction modulo h(x).      
// ============================================================================== 

module gf2_31_prng (
    input  wire              clk,
    input  wire              rst,        // Reset signal (active high)
    input  wire              enable,     // Enable signal for updating state
    input  wire [31-1:0]     seed,       // Initial polynomial/condition
    output wire [31-1:0]     prng_out    // Output of current PRNG state
);

    // Internal state register holds current PRNG state
    reg [31-1:0] state;

    // Wire to hold next PRNG state after applying recurrence
    wire [31-1:0] next_state;

    // Declare module that computes recurrence relation in GF(2^31)
    gf2_poly_affine_mod_31 GF2_POLY_AFFINE_MOD_31 (
        .in_poly(state),
        .out_poly(next_state)
    );

    // PRNG state update logic
    always @(posedge clk) begin
        if (rst)
            state <= seed;                  // Load seed on reset
        else if (enable)
            state <= next_state;            // Update state only when enabled
    end

    // Assign PRNG output
    assign prng_out = state;

endmodule