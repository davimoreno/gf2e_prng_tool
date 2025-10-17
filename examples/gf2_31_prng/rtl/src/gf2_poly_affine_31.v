// ============================================================================== 
// GF(2) Polynomial Affine Computation                                           
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Computes the expression a(x)p(x) + c(x) over GF(2) for any input polynomial p(x).
// All polynomials have binary coefficients (0 or 1).                             
//                                                                                 
// Constant polynomials a(x) and c(x) given as:                                   
//     - a(x) = x^4 + 1
//     - c(x) = 1
//                                                                                 
// INPUT:                                                                          
//     - in_poly   : 31-bit input vector representing polynomial p(x)       
//                                                                                 
// OUTPUT:                                                                         
//     - out_poly  : 35-bit output vector representing a(x)p(x) + c(x)   
// ============================================================================== 

module gf2_poly_affine_31 (
    input  wire [31-1:0] in_poly,
    output wire [35-1:0] out_poly
);

    // Declare regs and wires
    wire [105-1:0] w_in_vectors;
    wire [35-1:0] w_out_xor;

    // Declare XOR tree module
    xor_tree_3_35 XOR_TREE_3_35 (
        .in_vectors(w_in_vectors),
        .out_xor(w_out_xor)
    );

    // Assign inputs to the XOR tree
    assign w_in_vectors[35-1:0] = in_poly << 4;
    assign w_in_vectors[70-1:35] = in_poly;
    assign w_in_vectors[105-1:70] = 35'd1;

    // Assign output
    assign out_poly = w_out_xor;
endmodule