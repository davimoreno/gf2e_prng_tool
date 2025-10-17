// ============================================================================== 
// GF(2) Polynomial Affine Computation with Modular Reduction                    
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Computes the expression a(x)p(x) + c(x) modulo h(x) over GF(2) for any input polynomial p(x).
// All polynomials have binary coefficients (0 or 1).                             
//                                                                                 
// Constant polynomials a(x), c(x), and h(x) given as:                            
//     - a(x) = x^4 + 1
//     - c(x) = 1
//     - h(x) = x^31 + x^13 + x^8 + x^3 + 1
//                                                                                 
// INPUT:                                                                          
//     - in_poly   : 31-bit input vector representing polynomial p(x)       
//                                                                                 
// OUTPUT:                                                                         
//     - out_poly  : 31-bit output vector representing a(x)p(x) + c(x) modulo h(x)
// ============================================================================== 

module gf2_poly_affine_mod_31 (
    input  wire [31-1:0] in_poly,
    output wire [31-1:0] out_poly
);

    // Declare regs and wires
    wire [31-1:0] w_in_affine;
    wire [35-1:0] w_out_affine;
    wire [35-1:0] w_in_mod;
    wire [31-1:0] w_out_mod;

    // Declare affine transformation module
    gf2_poly_affine_31 GF2_POLY_AFFINE_31 (
        .in_poly(w_in_affine),
        .out_poly(w_out_affine)
    );

    // Declare modular reduction module
    gf2_poly_mod_35 GF2_POLY_MOD_35 (
        .in_poly(w_in_mod),
        .out_poly(w_out_mod)
    );

    // Assign wires
    assign w_in_affine = in_poly;
    assign w_in_mod = w_out_affine;

    // Assign output
    assign out_poly = w_out_mod;
endmodule