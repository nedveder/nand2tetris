"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter







CONSTANT_KEYWORDS: list[str]  = ["true", "false", "null", "this"]
CONSTANTS: list[str]  = ["integerConstant", "stringConstant"]


NEG: str  = "neg"
NOT : str = "not"
ADD : str = "add"
OPERATORS: dict[str, str] = {'+': "add", '-': "sub", '*': "call Math.multiply 2", '/': "call Math.divide 2", '&': "and", '|': "or",
             '<': "lt", '>': "gt", '=': "eq"}
UNARY_OPERATORS: dict[str, str] = {'-': "neg", '~': "not", '^': "shiftleft", '#': "shiftright"}
CLOSE_ROUND_BRACKET : str = ")"

# Statements
RETURN_STATEMENT : str = "return"
DO_STATEMENT : str = "do"
WHILE_STATEMENT: str  = "while"
IF_STATEMENT : str = "if"
LET_STATEMENT : str = "let"
ELSE_STATEMENT : str = "else"

# UNCLASSIFIED
VOID : str = "void"
IDENTIFIER: str  = "identifier"
MEMORY_ALLOC: str  = "Memory.alloc"
APPEND_CHAR : str = "String.appendChar"
STRING_NEW: str  = "String.new"
VAR_TYPES: list[str]  = ["int", "char", "boolean"]
EXP: str  = "expression"

# SEGMENTS
CONSTANT: str  = "constant"
POINTER: str  = "pointer"
ARG: str  = "argument"
THIS: str  = "this"
THAT : str = "that"
LOCAL: str  = "local"
TEMP: str  = "temp"

# CLASSIFICATION
FIELD: str  = "field"
STATIC: str  = "static"
VAR: str  = "var"
CONSTRUCTOR : str = "constructor"
FUNCTION : str = "function"
METHOD: str  = "method"
CLASS_METHODS: list[str]  = [CONSTRUCTOR, FUNCTION, METHOD]
CLASS_VARIABLES: list[str]  = [STATIC, FIELD]

# EXTRA CONSTANTS
COMMA_SEPERATOR: str  = ","
BACK_SLASH: str  = "/"
DOT: str  = "."
OPEN_SQUARE_BRACKET : str = "["
OPEN_ROUND_BRACKET: str  = "("
SEMICOLON : str = ";"


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    token written after any advance command is the current token before advancing.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self._conditional_suffix :dict[str,int]= dict()
        self._class_name:str = ""
        self._input: JackTokenizer = input_stream
        self._output: VMWriter = VMWriter(output_stream)
        self._symbol_table: SymbolTable = SymbolTable()
        self.reset_condition()

    def reset_condition(self) -> None:
        self._conditional_suffix = {WHILE_STATEMENT: 0, IF_STATEMENT: 0}

    @staticmethod
    def segment_specifier(var_kind:str)->str:
        if var_kind == FIELD:
           var_kind = THIS
        return var_kind if var_kind != VAR else LOCAL

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._input.advance()  # class
        self._class_name = self._input.token()
        self._input.advance()  # class name
        self._input.advance()  # open bracket
        while self._input.token() in CLASS_VARIABLES:
            self.compile_class_var_dec()
        while self._input.token() in CLASS_METHODS:
            self.compile_subroutine()
        self._input.advance()  # close bracket

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        var_kind = self._input.token()
        self._input.advance()  # var kind
        self.variable_declaration(var_kind)
        self._input.advance()  # ;

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        """
        # Init symbol table
        self._symbol_table.start_subroutine()
        self.reset_condition()
        
        # Get function declaration data
        subroutine_type = self._input.token()
        self._input.advance()  # subroutine type
        if subroutine_type == METHOD:
            self._symbol_table.define(THIS, self._class_name, ARG)
        self._input.advance()  # subroutine return type
        subroutine_name = self._input.token()
        self._input.advance()  # subroutine name
        self._input.advance()  # open bracket
        self.compile_parameter_list()
        self._input.advance()  # close bracket

        self._input.advance()  # body open bracket
        # Add local variables to symbol table
        n_vars = 0
        while self._input.token() == VAR:
            n_vars += self.compile_var_dec()

        # Write function declaration and specific subroutine actions
        self._output.write_function(f"{self._class_name}.{subroutine_name}", n_vars)
        if subroutine_type == METHOD:
            self._output.write_push(ARG, 0)
            self._output.write_pop(POINTER, 0)
        elif subroutine_type == CONSTRUCTOR:
            self._output.write_push(CONSTANT, self._symbol_table.var_count(FIELD))
            self._output.write_call(MEMORY_ALLOC, 1)
            self._output.write_pop(POINTER, 0)

        self.compile_statements()
        self._input.advance()  # body close bracket

    def compile_parameter_list(self) -> int:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        n_args = 0
        # Checks whether next token is valid variable type -  primitive type or class obj.
        non_empty_list = self._input.token() in VAR_TYPES or self._input.token_type() == IDENTIFIER
        while non_empty_list or self._input.token() == COMMA_SEPERATOR:
            if non_empty_list:
                non_empty_list = False
            else:
                self._input.advance()  # ,
            var_type = self._input.token()
            self._input.advance()  # var type
            var_name = self._input.token()
            self._input.advance()  # var name
            self._symbol_table.define(var_name, var_type, ARG)
            n_args += 1
        return n_args

    def variable_declaration(self, var_kind) -> int:
        """
        Args:
            var_kind: kind of variable to add into symbol table
        Returns: total number of variables added
        """
        n_vars = 0
        var_type = self._input.token()
        self._input.advance()  # var type
        var_name = self._input.token()
        self._input.advance()  # var name
        self._symbol_table.define(var_name, var_type, var_kind)
        n_vars += 1
        while self._input.token() == COMMA_SEPERATOR:
            self._input.advance()  # ,
            var_name = self._input.token()
            self._input.advance()  # var name
            self._symbol_table.define(var_name, var_type, var_kind)
            n_vars += 1
        return n_vars

    def compile_var_dec(self) -> int:
        """Compiles a var declaration."""
        self._input.advance()  # var
        n_vars = self.variable_declaration(VAR)
        self._input.advance()  # ;
        return n_vars

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        STATEMENTS = {LET_STATEMENT: self.compile_let, IF_STATEMENT: self.compile_if,
                      WHILE_STATEMENT: self.compile_while, DO_STATEMENT: self.compile_do,
                      RETURN_STATEMENT: self.compile_return}
        while self._input.token() in STATEMENTS:
            STATEMENTS[self._input.token()]()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._input.advance()  # do
        first_name, second_name = self._input.token(), None
        self._input.advance()  # subroutineName or className or varName
        if self._input.token() == DOT:
            self._input.advance()  # .
            second_name = f".{self._input.token()}"
            self._input.advance()  # subroutineName or className or varName
        self.compile_subroutine_call(first_name, second_name)
        self._output.write_pop(TEMP, 0)
        self._input.advance()  # ;

    def compile_subroutine_call(self, first_name, second_name) -> None:
        n_args = 0
        # Push correct data for methods
        if self._symbol_table.contains(first_name):
            var_index = self._symbol_table.index_of(first_name)
            var_kind = self.segment_specifier(self._symbol_table.kind_of(first_name))
            self._output.write_push(var_kind, var_index)
            n_args += 1
            first_name = self._symbol_table.type_of(first_name)
        elif second_name is None:  # if there doesn't exist a dot
            self._output.write_push(POINTER, 0)
            second_name = f".{first_name}"
            first_name = self._class_name
            n_args += 1
        # elif first_name
        self._input.advance()  # open bracket
        n_args += self.compile_expression_list()
        self._input.advance()  # close bracket
        self._output.write_call(f"{first_name}{second_name}", n_args)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._input.advance()  # let
        var_name = self._input.token()
        self._input.advance()  # varName
        var_index = self._symbol_table.index_of(var_name)
        var_kind = self.segment_specifier(self._symbol_table.kind_of(var_name))
        is_array = self._input.token() == OPEN_SQUARE_BRACKET
        if is_array:
            self.compile_array(var_index, var_kind)
            self._input.advance()  # =
            self.compile_expression()
            self._output.write_pop(TEMP, 0)
            self._output.write_pop(POINTER, 1)
            self._output.write_push(TEMP, 0)
            self._output.write_pop(THAT, 0)
            self._input.advance()  # ;
        else:
            self._input.advance()  # =
            self.compile_expression()
            self._output.write_pop(var_kind, var_index)
            self._input.advance()  # ;

    def compile_array(self, var_index, var_kind):
        var_kind = self.segment_specifier(var_kind)
        self._input.advance()  # [ bracket
        self.compile_expression()
        self._output.write_push(var_kind, var_index)
        self._output.write_arithmetic(ADD)
        self._input.advance()  # ] bracket

    def compile_while(self) -> None:
        """Compiles a while statement."""
        label = f"WHILE_EXP{self._conditional_suffix[WHILE_STATEMENT]}"
        end_label = f"WHILE_END{self._conditional_suffix[WHILE_STATEMENT]}"
        self._output.write_label(label)
        self._conditional_suffix[WHILE_STATEMENT] += 1
        self._input.advance()  # while
        self._input.advance()  # open bracket
        self.compile_expression()
        self._output.write_arithmetic(NOT)
        self._output.write_if(end_label)
        self._input.advance()  # close bracket
        self._input.advance()  # open bracket
        self.compile_statements()
        self._output.write_goto(label)
        self._input.advance()  # close bracket
        self._output.write_label(end_label)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._input.advance()  # return
        if self._input.token() != SEMICOLON:
            self.compile_expression()
        else:
            self._output.write_push(CONSTANT, 0)
        self._output.write_return()
        self._input.advance()  # ;

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        if_label = f"IF_TRUE{self._conditional_suffix[IF_STATEMENT]}"
        else_label = f"IF_FALSE{self._conditional_suffix[IF_STATEMENT]}"
        end_label = f"IF_END{self._conditional_suffix[IF_STATEMENT]}"
        self._conditional_suffix[IF_STATEMENT] += 1
        self._input.advance()  # if
        self._input.advance()  # open bracket
        self.compile_expression()
        self._output.write_if(if_label)
        self._output.write_goto(else_label)
        self._output.write_label(if_label)
        self._input.advance()  # close bracket
        self._input.advance()  # open bracket
        self.compile_statements()
        self._input.advance()  # close bracket
        if self._input.token() == ELSE_STATEMENT:
            self._output.write_goto(end_label)
            self._output.write_label(else_label)
            self._input.advance()  # else
            self._input.advance()  # open bracket
            self.compile_statements()
            self._input.advance()  # close bracket
            self._output.write_label(end_label)
        else:
            self._output.write_label(else_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        if self._input.token() in OPERATORS:
            op = OPERATORS[self._input.token()]
            self._input.advance()  # op
            self.compile_expression()
            self._output.write_arithmetic(op)

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        if self._input.token_type() in CONSTANTS or self._input.token() in CONSTANT_KEYWORDS:
            self.compile_const_term()
        elif self._input.token() == OPEN_ROUND_BRACKET:
            self._input.advance()  # open bracket
            self.compile_expression()
            self._input.advance()  # close bracket

        elif self._input.token_type() == IDENTIFIER:
            first_name, second_name = self._input.token(), None
            self._input.advance()  # subroutineName or className or varName

            if self._input.token() == OPEN_SQUARE_BRACKET:  # is an array
                var_kind, var_index = self._symbol_table.kind_of(first_name), self._symbol_table.index_of(first_name)
                self.compile_array(var_index, var_kind)
                self._output.write_pop(POINTER, 1)
                self._output.write_push(THAT, 0)

            elif self._input.token() in [DOT, OPEN_ROUND_BRACKET]:  # is a subroutine call
                if self._input.token() == DOT:
                    self._input.advance()  # .
                    second_name = f".{self._input.token()}"
                    self._input.advance()  # subroutineName if className or varName before
                self.compile_subroutine_call(first_name, second_name)

            else:  # is a variable
                var_index = self._symbol_table.index_of(first_name)
                var_kind = self.segment_specifier(self._symbol_table.kind_of(first_name))
                self._output.write_push(var_kind, var_index)

        elif self._input.token() in UNARY_OPERATORS:
            op = UNARY_OPERATORS[self._input.token()]
            self._input.advance()  # op
            self.compile_term()
            self._output.write_arithmetic(op)

    def compile_const_term(self):
        if self._input.token_type() == CONSTANTS[0]:  # integerConstant
            self.compile_int_const()
        elif self._input.token_type() == CONSTANTS[1]:  # stringConstant
            self.compile_str_const()
        elif self._input.token() == CONSTANT_KEYWORDS[0]:  # true
            self._output.write_push(CONSTANT, 0)
            self._output.write_arithmetic(NOT)
        elif self._input.token() == CONSTANT_KEYWORDS[1] or self._input.token() == CONSTANT_KEYWORDS[2]:  # null/false
            self._output.write_push(CONSTANT, 0)
        elif self._input.token() == CONSTANT_KEYWORDS[3]:  # this
            self._output.write_push(POINTER, 0)
        self._input.advance()  # constant

    def compile_str_const(self):
        str_len = len(self._input.token())
        self._output.write_push(CONSTANT, str_len)
        self._output.write_call(STRING_NEW, 1)
        for i in range(str_len):
            self._output.write_push(CONSTANT, ord(self._input.token()[i]))
            self._output.write_call(APPEND_CHAR, 2)

    def compile_int_const(self):
        self._output.write_push(CONSTANT, int(self._input.token()))

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        n_expressions = 0
        non_empty_list = self._input.token() != CLOSE_ROUND_BRACKET
        while non_empty_list or self._input.token() == COMMA_SEPERATOR:
            if non_empty_list:
                non_empty_list = False
            else:
                self._input.advance()  # ,
            self.compile_expression()
            n_expressions += 1
        return n_expressions
