"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import re
import typing
from re import Match, Pattern

COMMENT_WHITESPACE_REGEX: Pattern[str] = re.compile(r'\/[\/]+.*|[^\S+]+')
A_COMMAND_REGEX: Pattern[str] = re.compile(r'@.+')
C_COMMAND_REGEX: Pattern[str] = re.compile(r'(\S+[;].*)|(\S+[=].*)')
L_COMMAND_REGEX: Pattern[str] = re.compile(r'[(][a-zA-Z0-9.$_:]+[)]')
SYMBOL_REGEX: Pattern[str] = re.compile(r'(?<=[(])[a-zA-Z0-9.$_:]+(?<![)])|(?<=@).+')


class Parser:
    """Encapsulates access to the input code. Reads an assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.
        Args:
            input_file (typing.TextIO): input file.
        """
        self._formated_lines: list = []
        input_lines: list[str] = input_file.read().splitlines()
        # Remove all comment lines and comments and all whitespace letters in line
        for line in input_lines:
            formatted_line: str = re.sub(COMMENT_WHITESPACE_REGEX, "", line)
            if formatted_line:
                self._formated_lines.append(formatted_line)
        self._line_num: int = len(self._formated_lines)
        self._current_line: int = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._current_line < self._line_num

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self._current_command: str = self._formated_lines[self._current_line]
        self._current_line += 1

    def reset(self) -> None:
        """Resets current pass back to the beginning of the file
        """
        self._current_line = 0
        self._current_command = self._formated_lines[self._current_line]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if re.match(L_COMMAND_REGEX, self._current_command):
            return "L_COMMAND"
        if re.match(A_COMMAND_REGEX, self._current_command):
            return "A_COMMAND"
        if re.match(C_COMMAND_REGEX, self._current_command):
            return "C_COMMAND"
        return ""

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        match: typing.Optional[Match[str]] = re.search(
            SYMBOL_REGEX, self._current_command)
        return match.group() if match else ""

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self._current_command.split('=')[0] if '=' in self._current_command else ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        parts: list[str] = self._current_command.split('=')
        location:int = 1 if len(parts) > 1 else 0
        return parts[location].split(';')[0] if ';' in self._current_command else parts[location]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self._current_command.split(';')[-1] if ';' in self._current_command else ""
