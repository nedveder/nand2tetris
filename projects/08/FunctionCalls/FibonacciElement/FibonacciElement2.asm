// BOOTSTRAP
@256
D=A
@SP
M=D
@54
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
A=A-1
D=M-D
M=0
@END_GT
D;JLE
@SP
A=M-1
M=-1
(END_GT)
@R13
A=M
0;JMP
// JLT COMP INIT
@R13
M=D
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=0
@END_LT
D;JGE
@SP
A=M-1
M=-1
(END_LT)
@R13
A=M
0;JMP
// CALL Sys.init vars:0
@Sys.init$ret0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init$ret0)
// FUNCTION Main.fibonacci vars:0
(Main.fibonacci)
//PUSH/POP C_PUSH segment:argument index:0
@2
D=M
@0
A=A+D
D=A
@R14
M=D
@R14
A=M
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:2
@2
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
@38
0;JMP
(RET_COMP_JLT0)
// IF IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
//GOTO IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
//LABEL IF_TRUE
(Main.fibonacci$IF_TRUE)
//PUSH/POP C_PUSH segment:argument index:0
@2
D=M
@0
A=A+D
D=A
@R14
M=D
@R14
A=M
D=M
@SP
M=M+1
A=M-1
M=D
// RETURN Main.fibonacci
@LCL
D=M
@R14
M=D
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R14
AM=M-1
D=M
@THAT
M=D
@R14
AM=M-1
D=M
@THIS
M=D
@R14
AM=M-1
D=M
@ARG
M=D
@R14
AM=M-1
D=M
@LCL
M=D
@R15
A=M
0;JMP
//LABEL IF_FALSE
(Main.fibonacci$IF_FALSE)
//PUSH/POP C_PUSH segment:argument index:0
@2
D=M
@0
A=A+D
D=A
@R14
M=D
@R14
A=M
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:2
@2
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
// CALL Main.fibonacci vars:1
@Main.fibonacci$ret0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret0)
//PUSH/POP C_PUSH segment:argument index:0
@2
D=M
@0
A=A+D
D=A
@R14
M=D
@R14
A=M
D=M
@SP
M=M+1
A=M-1
M=D
//PUSH/POP C_PUSH segment:constant index:1
@1
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
// CALL Main.fibonacci vars:1
@Main.fibonacci$ret1
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret1)
// ARITMETIC add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// RETURN Main.fibonacci
@LCL
D=M
@R14
M=D
@5
A=D-A
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R14
AM=M-1
D=M
@THAT
M=D
@R14
AM=M-1
D=M
@THIS
M=D
@R14
AM=M-1
D=M
@ARG
M=D
@R14
AM=M-1
D=M
@LCL
M=D
@R15
A=M
0;JMP
// FUNCTION Sys.init vars:0
(Sys.init)
//PUSH/POP C_PUSH segment:constant index:4
@4
D=A
@R14
M=D
@R14
D=M
@SP
M=M+1
A=M-1
M=D
// CALL Main.fibonacci vars:1
@Main.fibonacci$ret0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret0)
//LABEL WHILE
(Sys.init$WHILE)
//GOTO WHILE
@Sys.init$WHILE
0;JMP
