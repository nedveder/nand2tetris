"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import typing

# The regex matches all whitespaces, all comments starting with // and all comments starting with /* and ending with */.
COMMENTS_WHITESPACES_REGEX = re.compile(r'(\s+|//[^\n]*|/\*.*?\*/)+', re.DOTALL)
# Each item contains regex pattern for specific type of token being parsed
TOKEN_PATTEN_DICT = {
    "stringConstant": r'"(.*?)"'
    , "integerConstant": r'([0-9]+)'
    , "symbol": r'([{}()[\]\.,;+\-\*/&|<>=~^#])'
    , "keyword": r'\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this'
                 r'|let|do|if|else|while|return)\b'
    , "identifier": r'([a-zA-Z_][a-zA-Z_0-9]*)'
}


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """It receives a file and reads it into a string.
        It also initializes the position pointer to 0.
        """
        self._input = input_stream.read()
        self._position: int = 0
        self.skip_comment_whitespaces()
        self._token = ""
        self._token_type = ""

    def has_more_tokens(self) -> bool:
        """
        Returns True if there are more tokens in the input.
        """
        return self._position < len(self._input)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called only if has_more_tokens() is true.
        Initially there is no current token.
        """
        if not self.has_more_tokens():
            return
        for token, pattern in TOKEN_PATTEN_DICT.items():
            match = re.match(re.compile(pattern), self._input[self._position:])
            if match:
                self.tokenize(match, token)
                return

    def tokenize(self, match, token):
        """
        Tokenizes the current match string and the selected token
        """
        self._token = match.group(0)
        self._token_type = token
        self._position += len(self._token)
        if token == "stringConstant":
            self._token = self._token[1:-1]
        self.skip_comment_whitespaces()

    def skip_comment_whitespaces(self):
        """
        The program progresses the position pointer for the input so it doesn't read comments or whitespaces.
        The regex matches all whitespaces and comments up to the index where somthing else appears,
        then progresses position accordingly - group(0) is first match of the pattern.
        """
        # Regex matches all whitespaces and comments up to the index where somthing else appears,
        comments_whitespaces = re.match(COMMENTS_WHITESPACES_REGEX, self._input[self._position:])
        # then progresses position accordingly - group(0) is first match of the pattern
        self._position += len(comments_whitespaces.group(0)) if comments_whitespaces else 0

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "keyword", "symbol", "identifier", "integerConst", "stringConst"
        """
        return self._token_type

    def token_output_xml(self) -> str:
        """
        Returns:
            str: the type of the current token in proper xml format, can be
            "keyword", "symbol", "identifier", "integerConst", "stringConst"
        """
        return f"<{self._token_type}> {self._token} </{self._token_type}>"

    def token(self) -> str:
        return self._token
