// BOOTSTRAP
@256
D=A
@SP
M=D
@COMP_INIT
0;JMP
// JEQ COMP INIT
@R13
M=D
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=0
@END_EQ
D;JNE
@SP
A=M-1
M=-1
(END_EQ)
@R13
A=M
0;JMP
// JGT COMP INIT
@R13
M=D
@SP
AM=M-1
D=M
@GT_FIRST
M=D
@GT_FIRST_POS
D;JGE
@GT_FIRST_NEG
0;JMP
(GT_FIRST_POS)
@SP
A=M-1
D=M
@GT_SECOND
M=D
@GT_FALSE
D;JLT
@GT_SAME_SIGN
0;JMP
(GT_FIRST_NEG)
@SP
A=M-1
D=M
@GT_SECOND
M=D
@GT_TRUE
D;JGT
@GT_SAME_SIGN
0;JMP
(GT_SAME_SIGN)
@GT_FIRST
D=M
@GT_SECOND
D=M-D
@GT_TRUE
D;JGT
@GT_FALSE
0;JMP
(GT_TRUE)
@SP
A=M-1
M=-1
@GT_END
0;JMP
(GT_FALSE)
@SP
A=M-1
M=0
(GT_END)
@R13
A=M
0;JMP
// JLT COMP INIT
@R13
M=D
@SP
AM=M-1
D=M
@LT_FIRST
M=D
@LT_FIRST_POS
D;JGE
@LT_FIRST_NEG
0;JMP
(LT_FIRST_POS)
@SP
A=M-1
D=M
@LT_SECOND
M=D
@LT_TRUE
D;JLT
@LT_SAME_SIGN
0;JMP
(LT_FIRST_NEG)
@SP
A=M-1
D=M
@LT_SECOND
M=D
@LT_FALSE
D;JGT
@LT_SAME_SIGN
0;JMP
(LT_SAME_SIGN)
@LT_FIRST
D=M
@LT_SECOND
D=M-D
@LT_TRUE
D;JLT
@LT_FALSE
0;JMP
(LT_TRUE)
@SP
A=M-1
M=-1
@LT_END
0;JMP
(LT_FALSE)
@SP
A=M-1
M=0
(LT_END)
@R13
A=M
0;JMP
(COMP_INIT)
//PUSH/POP C_PUSH segment:constant index:17
@17
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:17
@17
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP eq
@RET_COMP_JEQ0
D=A
@6
0;JMP
(RET_COMP_JEQ0)
//PUSH/POP C_PUSH segment:constant index:17
@17
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:16
@16
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP eq
@RET_COMP_JEQ1
D=A
@6
0;JMP
(RET_COMP_JEQ1)
//PUSH/POP C_PUSH segment:constant index:16
@16
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:17
@17
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP eq
@RET_COMP_JEQ2
D=A
@6
0;JMP
(RET_COMP_JEQ2)
//PUSH/POP C_PUSH segment:constant index:892
@892
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:891
@891
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP lt
@RET_COMP_JLT0
D=A
@70
0;JMP
(RET_COMP_JLT0)
//PUSH/POP C_PUSH segment:constant index:891
@891
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:892
@892
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP lt
@RET_COMP_JLT1
D=A
@70
0;JMP
(RET_COMP_JLT1)
//PUSH/POP C_PUSH segment:constant index:891
@891
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:891
@891
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP lt
@RET_COMP_JLT2
D=A
@70
0;JMP
(RET_COMP_JLT2)
//PUSH/POP C_PUSH segment:constant index:32767
@32767
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:32766
@32766
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP gt
@RET_COMP_JGT0
D=A
@22
0;JMP
(RET_COMP_JGT0)
//PUSH/POP C_PUSH segment:constant index:32766
@32766
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:32767
@32767
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP gt
@RET_COMP_JGT1
D=A
@22
0;JMP
(RET_COMP_JGT1)
//PUSH/POP C_PUSH segment:constant index:32766
@32766
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:32766
@32766
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// COMP gt
@RET_COMP_JGT2
D=A
@22
0;JMP
(RET_COMP_JGT2)
//PUSH/POP C_PUSH segment:constant index:57
@57
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:31
@31
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:53
@53
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// ARITMETIC add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//PUSH/POP C_PUSH segment:constant index:112
@112
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// ARITMETIC sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// ARITMETIC neg
@SP
AM=M-1
D=M
M=-D
@SP
M=M+1
// ARITMETIC and
@SP
AM=M-1
D=M
A=A-1
M=M&D
//PUSH/POP C_PUSH segment:constant index:82
@82
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// ARITMETIC or
@SP
AM=M-1
D=M
A=A-1
M=D|M
// ARITMETIC not
@SP
AM=M-1
D=M
M=!D
@SP
M=M+1
