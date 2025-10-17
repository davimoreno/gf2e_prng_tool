// ============================================================================== 
// Binary XOR Tree                                                                
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Computes the bitwise XOR of multiple binary vectors using a binary tree        
// structure. The module receives a single input vector composed of 3
// concatenated 35-bit vectors (total of 105 bits) and returns a 35-bit output
// representing their bitwise XOR.                                                
//                                                                                 
// INPUT:                                                                          
//     - in_vectors : 105-bit input vector (3 concatenated 35-bit binary vectors)
//                                                                                 
// OUTPUT:                                                                         
//     - out_xor    : 35-bit output vector (bitwise XOR of all 3 input vectors)
//                                                                                 
// NOTE:                                                                           
//     - The XOR operation is performed using a balanced binary tree to           
//       minimize logic depth.                                                    
// ============================================================================== 

module xor_tree_3_35 (
    input  wire [105-1:0] in_vectors,
    output wire [35-1:0] out_xor
);

    // Unpack input vectors
    wire [35-1:0] vec_0_0;
    assign vec_0_0 = in_vectors[34:0];
    wire [35-1:0] vec_0_1;
    assign vec_0_1 = in_vectors[69:35];
    wire [35-1:0] vec_0_2;
    assign vec_0_2 = in_vectors[104:70];

    // XOR tree structure
    // Tree stage 1
    wire [35-1:0] vec_1_0;
    assign vec_1_0 = vec_0_0 ^ vec_0_1;
    wire [35-1:0] vec_1_1;
    assign vec_1_1 = vec_0_2;

    // Tree stage 2
    wire [35-1:0] vec_2_0;
    assign vec_2_0 = vec_1_0 ^ vec_1_1;

    // Assign output
    assign out_xor = vec_2_0;
endmodule