// ============================================================================== 
// GF(2) Polynomial Modular Reduction                                            
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Computes the polynomial reduction y(x) mod h(x) over GF(2), for any input       
// polynomial y(x) with at most 35 bits.                              
// All polynomials have binary coefficients (0 or 1).                             
//                                                                                 
// Constant polynomial h(x) given as:                                             
//     - h(x) = x^31 + x^13 + x^8 + x^3 + 1
//                                                                                 
// INPUT:                                                                          
//     - in_poly   : 35-bit input vector representing polynomial y(x)  
//                                                                                 
// OUTPUT:                                                                         
//     - out_poly  : 31-bit output vector representing y(x) mod h(x)  
// ============================================================================== 

module gf2_poly_mod_35 (
    input  wire [35-1:0] in_poly,
    output wire [31-1:0] out_poly
);

    // Declare regs and wires
    wire [155-1:0] w_in_vectors;
    wire [31-1:0] w_out_xor;

    // Declare XOR tree module
    xor_tree_5_31 XOR_TREE_5_31 (
        .in_vectors(w_in_vectors),
        .out_xor(w_out_xor)
    );

    // Assign inputs to the XOR tree
    assign w_in_vectors[31-1:0] = in_poly[31]? 31'd8457 : 31'd0;
    assign w_in_vectors[62-1:31] = in_poly[32]? 31'd16914 : 31'd0;
    assign w_in_vectors[93-1:62] = in_poly[33]? 31'd33828 : 31'd0;
    assign w_in_vectors[124-1:93] = in_poly[34]? 31'd67656 : 31'd0;
    assign w_in_vectors[155-1:124] = in_poly[31-1:0];

    // Assign output
    assign out_poly = w_out_xor;
endmodule