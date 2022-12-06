"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

special_chars_dict = {'&': "<symbol> &amp; </symbol>", '<': "<symbol> &lt; </symbol>", '>': "<symbol> &gt; </symbol>"}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self._input = input_stream
        self._indentation = 0
        self._output = output_stream

    def write_token(self):
        indentation = self._indentation * '  '
        if self._input.token() in special_chars_dict:
            self._output.write(f"{indentation}{special_chars_dict[self._input.token()]}\n")
        else:
            self._output.write(f"{indentation}{self._input.token_output_xml()}\n")
        self._input.advance()

    def write_tag(self, tag):
        if "/" in tag:
            self._indentation += -1
            indentation = self._indentation * '  '
            self._output.write(f"{indentation}{tag}\n")
        else:
            indentation = self._indentation * '  '
            self._output.write(f"{indentation}{tag}\n")
            self._indentation += 1

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.write_tag("<class>")
        self.write_token()  # class
        self.write_token()  # class name
        self.write_token()  # open bracket
        while self._input.token() in ["static", "field"]:
            self.compile_class_var_dec()
        while self._input.token() in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.write_token()  # close bracket
        self.write_tag("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.write_tag("<classVarDec>")
        self.write_token()  # var kind name
        self.write_token()  # type
        self.write_token()  # varName
        while self._input.token() == ",":
            self.write_token()  # ,
            self.write_token()  # varName
        self.write_token()  # ;
        self.write_tag("</classVarDec>")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.write_tag("<subroutineDec>")
        self.write_token()  # subroutine type
        self.write_token()  # subroutine return type
        self.write_token()  # subroutine name
        self.write_token()  # open bracket
        self.compile_parameter_list()
        self.write_token()  # close bracket
        self.compile_subroutine_body()
        self.write_tag("</subroutineDec>")

    def compile_subroutine_body(self) -> None:
        """
        Compiles the body of the subroutine
        """
        self.write_tag("<subroutineBody>")
        self.write_token()  # body open bracket
        while self._input.token() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.write_token()  # body close bracket
        self.write_tag("</subroutineBody>")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.write_tag("<parameterList>")
        if self._input.token() in ["int", "char", "boolean"] or self._input.token_type() == "identifier":
            self.write_token()  # type
            self.write_token()  # varName
            while self._input.token() == ",":
                self.write_token()  # ,
                self.write_token()  # type
                self.write_token()  # varName
        self.write_tag("</parameterList>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.write_tag("<varDec>")
        self.write_token()  # var
        self.write_token()  # type
        self.write_token()  # varName
        while self._input.token() == ",":
            self.write_token()  # ,
            self.write_token()  # varName
        self.write_token()  # ;
        self.write_tag("</varDec>")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.write_tag("<statements>")
        while self._input.token() in ["let", "if", "while", "do", "return"]:
            if self._input.token() == "let":
                self.compile_let()
            elif self._input.token() == "if":
                self.compile_if()
            elif self._input.token() == "while":
                self.compile_while()
            elif self._input.token() == "do":
                self.compile_do()
            elif self._input.token() == "return":
                self.compile_return()
        self.write_tag("</statements>")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.write_tag("<doStatement>")
        self.write_token()  # do
        self.write_token()  # subroutineName or className or varName
        if self._input.token() == ".":
            self.write_token()  # .
            self.write_token()  # subroutineName if className or varName before
        self.write_token()  # open bracket
        self.compile_expression_list()
        self.write_token()  # close bracket
        self.write_token()  # ;
        self.write_tag("</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.write_tag("<letStatement>")
        self.write_token()  # let
        self.write_token()  # varName
        if self._input.token() == "[":
            self.write_token()  # [ bracket
            self.compile_expression()
            self.write_token()  # ] bracket
        self.write_token()  # =
        self.compile_expression()
        self.write_token()  # ;
        self.write_tag("</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.write_tag("<whileStatement>")
        self.write_token()  # while
        self.write_token()  # open bracket
        self.compile_expression()
        self.write_token()  # close bracket
        self.write_token()  # open bracket
        self.compile_statements()
        self.write_token()  # close bracket
        self.write_tag("</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.write_tag("<returnStatement>")
        self.write_token()  # return
        if self._input.token() != ";":
            self.compile_expression()
        self.write_token()  # ;
        self.write_tag("</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.write_tag("<ifStatement>")
        self.write_token()  # if
        self.write_token()  # open bracket
        self.compile_expression()
        self.write_token()  # close bracket
        self.write_token()  # open bracket
        self.compile_statements()
        self.write_token()  # close bracket
        if self._input.token() == "else":
            self.write_token()  # else
            self.write_token()  # open bracket
            self.compile_statements()
            self.write_token()  # close bracket
        self.write_tag("</ifStatement>")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.write_tag("<expression>")
        self.compile_term()
        while self._input.token() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.write_token()  # op
            self.compile_term()
        self.write_tag("</expression>")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.write_tag("<term>")
        if self._input.token_type() in ["integerConstant", "stringConstant"] or self._input.token() in ["true", "false",
                                                                                                        "null", "this"]:
            self.write_token()  # constant
        elif self._input.token() == "(":
            self.write_token()  # open bracket
            self.compile_expression()
            self.write_token()  # close bracket
        elif self._input.token_type() == "identifier":
            self.write_token()  # subroutineName or className or varName
            if self._input.token() == ".":
                self.write_token()  # .
                self.write_token()  # subroutineName if className or varName before
                self.write_token()  # ( bracket
                self.compile_expression_list()
                self.write_token()  # ) bracket
            elif self._input.token() == "[":
                self.write_token()  # [ bracket
                self.compile_expression()
                self.write_token()  # ] bracket
            elif self._input.token() == "(":
                self.write_token()  # ( bracket
                self.compile_expression_list()
                self.write_token()  # ) bracket
        elif self._input.token() in ['-', '~', '^', '#']:
            self.write_token()  # unaryOp
            self.compile_term()
        self.write_tag("</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.write_tag("<expressionList>")
        if self._input.token() != ")":
            self.compile_expression()
            while self._input.token() == ",":
                self.write_token()  # ,
                self.compile_expression()
        self.write_tag("</expressionList>")
