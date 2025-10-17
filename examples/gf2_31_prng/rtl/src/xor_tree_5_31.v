// ============================================================================== 
// Binary XOR Tree                                                                
// ------------------------------------------------------------------------------ 
// @author      : Davi Moreno                                                     
// @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE                
//                                                                                 
// Computes the bitwise XOR of multiple binary vectors using a binary tree        
// structure. The module receives a single input vector composed of 5
// concatenated 31-bit vectors (total of 155 bits) and returns a 31-bit output
// representing their bitwise XOR.                                                
//                                                                                 
// INPUT:                                                                          
//     - in_vectors : 155-bit input vector (5 concatenated 31-bit binary vectors)
//                                                                                 
// OUTPUT:                                                                         
//     - out_xor    : 31-bit output vector (bitwise XOR of all 5 input vectors)
//                                                                                 
// NOTE:                                                                           
//     - The XOR operation is performed using a balanced binary tree to           
//       minimize logic depth.                                                    
// ============================================================================== 

module xor_tree_5_31 (
    input  wire [155-1:0] in_vectors,
    output wire [31-1:0] out_xor
);

    // Unpack input vectors
    wire [31-1:0] vec_0_0;
    assign vec_0_0 = in_vectors[30:0];
    wire [31-1:0] vec_0_1;
    assign vec_0_1 = in_vectors[61:31];
    wire [31-1:0] vec_0_2;
    assign vec_0_2 = in_vectors[92:62];
    wire [31-1:0] vec_0_3;
    assign vec_0_3 = in_vectors[123:93];
    wire [31-1:0] vec_0_4;
    assign vec_0_4 = in_vectors[154:124];

    // XOR tree structure
    // Tree stage 1
    wire [31-1:0] vec_1_0;
    assign vec_1_0 = vec_0_0 ^ vec_0_1;
    wire [31-1:0] vec_1_1;
    assign vec_1_1 = vec_0_2 ^ vec_0_3;
    wire [31-1:0] vec_1_2;
    assign vec_1_2 = vec_0_4;

    // Tree stage 2
    wire [31-1:0] vec_2_0;
    assign vec_2_0 = vec_1_0 ^ vec_1_1;
    wire [31-1:0] vec_2_1;
    assign vec_2_1 = vec_1_2;

    // Tree stage 3
    wire [31-1:0] vec_3_0;
    assign vec_3_0 = vec_2_0 ^ vec_2_1;

    // Assign output
    assign out_xor = vec_3_0;
endmodule