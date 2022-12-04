// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.    
    //init max=-16384 and min=16384 which are edge case values
    @16384
    D=A
    @MAX
    M=-D
    @MIN
    M=D
    // ADDRESS_i = R15 + R14 (array end location)
    @R15
    D=M-1
    @R14
    D=D+M
    @ADDRESS_i
    M=D
(OUTER_LOOP)
    // if i>=0
    @ADDRESS_i
    D = M
    @R14
    D=D-M
    @OUTER_LOOP_END
    D;JLT
    // get address of arr[i] and content
    @ADDRESS_i
    A=M
    D=M
    @CONTENT_i
    M=D
    //max - arr[i] < 0 ? arr[i] : max
    @MAX
    D=M-D
    @DONT_SWAP_MAX
    D;JGE
    @CONTENT_i
    D=M
    @MAX
    M=D
    @ADDRESS_i
    D=M
    @MAX_ADDRESS
    M=D
(DONT_SWAP_MAX)
    // get address of arr[i] and content
    @ADDRESS_i
    A=M
    D=M
    @CONTENT_i
    M=D
    //min - arr[i] > 0 ? arr[i] : min
    @MIN
    D=M-D
    @DONT_SWAP_MIN
    D;JLE
    @CONTENT_i
    D=M
    @MIN
    M=D
    @ADDRESS_i
    D=M
    @MIN_ADDRESS
    M=D
(DONT_SWAP_MIN)
    // ADDRESS_i--
    @ADDRESS_i
    M=M-1
    @OUTER_LOOP
    0;JMP
(OUTER_LOOP_END)
    //swap values
    @MAX
    D=M
    @MIN_ADDRESS
    A=M
    M=D
    @MIN
    D=M
    @MAX_ADDRESS
    A=M
    M=D
// End Program
(END)
    @END
    0;JMP