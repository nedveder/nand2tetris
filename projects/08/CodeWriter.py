"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import os
from typing import List, Dict, TextIO

# Pop stack value into D
STACK_POP: list[str] = ["@SP", "AM=M-1", "D=M"]
# Push value into stack from D
STACK_PUSH: list[str] = ["@SP", "M=M+1", "A=M-1", "M=D"]


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: TextIO) -> None:
        """Initializes the CodeWriter.
        Args:
            output_stream (typing.TextIO): output stream.
        """
        self._output_stream = output_stream
        self._total_lines_written = 0
        self._call_dict: Dict[str, int] = dict()
        self.comp_code: Dict[str, List] = {"eq": [6, 0, "JEQ"], "gt": [22, 0, "JGT"],
                                           "lt": [70, 0, "JLT"]}
        self._file_name = ""
        self._function_name = ""

    def write_code(self, code) -> None:
        self._total_lines_written += len(code)
        self._output_stream.writelines(f"{line}\n" for line in code)

    def write_bootstrap(self) -> None:
        """
        Adds bootstrap code sets RAM[0]=256 and adds Comparison routines
        """
        code: list[str] = ["// BOOTSTRAP"]
        # Set stack pointer so 256
        code += ["@256", "D=A", "@SP", "M=D"]
        #Init Comparison routines
        code += ["@118", "0;JMP"]
        code += ["// JEQ COMP INIT", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=0", "@END_EQ", "D;JNE", "@SP", "A=M-1", "M=-1", "(END_EQ)", "@R13", "A=M", "0;JMP",
                 "// JGT COMP INIT", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@GT_FIRST", "M=D", "@GT_FIRST_POS", "D;JGE", "@GT_FIRST_NEG", "0;JMP", "(GT_FIRST_POS)", "@SP", "A=M-1", "D=M", "@GT_SECOND", "M=D", "@GT_FALSE", "D;JLT", "@GT_SAME_SIGN", "0;JMP", "(GT_FIRST_NEG)", "@SP", "A=M-1", "D=M", "@GT_SECOND", "M=D", "@GT_TRUE", "D;JGT", "@GT_SAME_SIGN", "0;JMP", "(GT_SAME_SIGN)", "@GT_FIRST", "D=M", "@GT_SECOND", "D=M-D", "@GT_TRUE", "D;JGT", "@GT_FALSE", "0;JMP", "(GT_TRUE)", "@SP", "A=M-1", "M=-1", "@GT_END", "0;JMP", "(GT_FALSE)", "@SP", "A=M-1", "M=0", "(GT_END)", "@R13", "A=M", "0;JMP",
                 "// JLT COMP INIT", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@LT_FIRST", "M=D", "@LT_FIRST_POS", "D;JGE", "@LT_FIRST_NEG", "0;JMP", "(LT_FIRST_POS)", "@SP", "A=M-1", "D=M", "@LT_SECOND", "M=D", "@LT_TRUE", "D;JLT", "@LT_SAME_SIGN", "0;JMP", "(LT_FIRST_NEG)", "@SP", "A=M-1", "D=M", "@LT_SECOND", "M=D", "@LT_FALSE", "D;JGT", "@LT_SAME_SIGN", "0;JMP", "(LT_SAME_SIGN)", "@LT_FIRST", "D=M", "@LT_SECOND", "D=M-D", "@LT_TRUE", "D;JLT", "@LT_FALSE", "0;JMP", "(LT_TRUE)", "@SP", "A=M-1", "M=-1", "@LT_END", "0;JMP", "(LT_FALSE)", "@SP", "A=M-1", "M=0", "(LT_END)", "@R13", "A=M", "0;JMP"]
        # call Sys.init
        code+= [f"// CALL Sys.init"]
        # Push SP into stack
        code += ["@SP", "D=A"]+STACK_PUSH
        # Push LCL into stack
        code += ["@LCL", "D=M"]+STACK_PUSH
        # Push ARG into stack
        code += ["@ARG", "D=M"]+STACK_PUSH
        # Push THIS into stack
        code += ["@THIS", "D=M"]+STACK_PUSH
        # Push THAT into stack
        code += ["@THAT", "D=M"]+STACK_PUSH
        # Set ARG = SP-5 (5 for SP,LCL,ARG,THIS,THAT)
        code += ["@5", "D=A", "@SP", "D=M-D", "@ARG", "M=D"]
        # Set LCL = SP 
        code += ["@SP", "D=M", "@LCL", "M=D"]
        # Go to function
        code += [f"@Sys.init", "0;JMP"]
        # Return label
        self.write_code(code)
        #self.write_call(f"Sys.init", 0)

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self._file_name, trash = os.path.splitext(os.path.basename(filename))

    def write_comp(self, command: str) -> None:
        # self.comp_code = { COMMAND : [ROW_NUM,OCCURENCES,SYMBOL] }
        code: list[str] = [f"// COMP {command}"]
        code += [f"@RET_COMP_{self.comp_code[command][2]}{self.comp_code[command][1]}",
                 "D=A",
                 f"@{self.comp_code[command][0]}",
                 "0;JMP",
                 f"(RET_COMP_{self.comp_code[command][2]}{self.comp_code[command][1]})"]
        # Increase call count
        self.comp_code[command][1] += 1
        self.write_code(code)

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Handle comparator operations
        if command in self.comp_code:
            self.write_comp(command)
            return
        code: list[str] = [f"// ARITMETIC {command}"]
        # Pop one argument from Stack into D  (D=Y)
        code += STACK_POP
        # If arithmetic command requires two paramaters,Pop from stack into M (M=X)
        self.code_dict: dict[str, str] = {"add": "M=M+D", "sub": "M=M-D", "neg": "M=-D",
                          "and": "M=M&D", "or": "M=D|M", "not": "M=!D", "shiftleft": "M=D<<", "shiftright": "M=D>>"}
        code += [self.code_dict[command], "@SP", "M=M+1"] if command in \
            ["neg", "not", "shiftleft", "shiftright"] else ["A=A-1", self.code_dict[command]]
        self.write_code(code)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        code=[]
        segments=["local","argument","this","that"]
        if command=="C_PUSH":
            if segment in segments:
                code+=[f"@{index}", "D=A",f"@{segments.index(segment)+1}", "A=M+D", "D=M"]
            elif segment=="constant":
                code+=[f"@{index}", "D=A"]
            elif segment=="temp":
                code+=[f"@{index+5}", "D=M"]
            elif segment=="static":
                code+=[f"@{self._file_name}.{index}", "D=M"]
            elif segment=="pointer":
                code+=[f"@{4 if index else 3}", "D=M"]
            code+=STACK_PUSH
        if command=="C_POP":
            if segment in segments:
                code+=[f"@{index}","D=A",f"@{segments.index(segment)+1}","D=D+M","@SP","AM=M-1","D=D+M","A=D-M","M=D-A"]
            elif segment=="temp":
                code+=[f"@{5+index}","D=A","@SP","AM=M-1","D=D+M","A=D-M","M=D-A"]
            elif segment=="static":
                code+=["@SP","AM=M-1","D=M",f"@{self._file_name}.{index}", "M=D"]
            elif segment=="pointer":
                code+=["@SP","AM=M-1","D=M",f"@{4 if index else 3}", "M=D"]
        self.write_code(code)


    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        code: list[str] = [f"//LABEL {label}"]
        code += [f"({self._function_name}${label})"] if self._function_name else [f"({label})"]
        self.write_code(code)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        code: list[str] = [f"//GOTO {label}"]
        code += [f"@{self._function_name}${label}",
                 "0;JMP"] if self._function_name else [f"@{label}", "0;JMP"]
        self.write_code(code)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        code: list[str] = [f"// IF {label}"]
        code += STACK_POP
        code += [f"@{self._function_name}${label}",
                 "D;JNE"] if self._function_name else [f"@{label}", "D;JNE"]
        self.write_code(code)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        code: list[str] = [f"// FUNCTION {function_name} vars:{n_vars}"]
        self._function_name = function_name
        if function_name not in self._call_dict:
            self._call_dict[function_name] = 0
        code += [f"({function_name})"]
        # Push 0 into stack for each local variable
        code += (["D=0"]+STACK_PUSH) * n_vars
        self.write_code(code)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "foo" be a function within the file Xxx.vm.
        The handling of each "call" command within foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        code: list[str] = [f"// CALL {function_name} vars:{n_args}"]
        # Push return address into stack
        if function_name not in self._call_dict:
            self._call_dict[function_name] = 0
        return_address: str = f"{self._function_name}$ret{self._call_dict[self._function_name]}"
        # Push return address
        code += [f"@{return_address}", "D=A"]+STACK_PUSH
        self._call_dict[self._function_name] += 1
        # Push LCL into stack
        code += ["@LCL", "D=M"]+STACK_PUSH
        # Push ARG into stack
        code += ["@ARG", "D=M"]+STACK_PUSH
        # Push THIS into stack
        code += ["@THIS", "D=M"]+STACK_PUSH
        # Push THAT into stack
        code += ["@THAT", "D=M"]+STACK_PUSH
        # Set ARG = SP-5-n_args
        allignment: int = n_args+5
        code += [f"@{allignment}", "D=A", "@SP", "D=M-D", "@ARG", "M=D"]
        # Set LCL = SP
        code += ["@SP", "D=M", "@LCL", "M=D"]
        # Go to function
        code += [f"@{function_name}", "0;JMP"]
        # Return label
        code += [f"({return_address})"]
        self.write_code(code)

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        code: list[str] = [f"// RETURN {self._function_name}"]
        # Put frame(R14) = LCL
        code += ["@LCL", "D=M", "@R14", "M=D"]
        # Put retAddress(R15) = frame - 5
        code += ["@5", "A=D-A", "D=M", "@R15", "M=D"]
        # Pop stack into ARG : this is the return value
        code += STACK_POP+["@ARG", "A=M", "M=D"]
        # Set SP to ARG+1 : reposition SP for caller
        code += ["@ARG", "D=M", "@SP", "M=D+1"]
        # Set THIS from saved value on callers stack
        code += ["@R14", "AM=M-1", "D=M", "@THAT", "M=D"]
        # Set THAT from saved value on callers stack
        code += ["@R14", "AM=M-1", "D=M", "@THIS", "M=D"]
        # Set ARG from saved value on callers stack
        code += ["@R14", "AM=M-1", "D=M", "@ARG", "M=D"]
        # Set LCL from saved value on callers stack
        code += ["@R14", "AM=M-1", "D=M", "@LCL", "M=D"]
        # Go to return address
        code += ["@R15", "A=M", "0;JMP"]
        self.write_code(code)
