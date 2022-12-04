"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import typing
from re import Pattern

COMMENT_REGEX: Pattern[str] = re.compile(r'\/[\/]+.*')


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self._formated_lines: list = []
        input_lines: list[str] = input_file.read().splitlines()
        # Remove all comment lines and comments and all whitespace letters in line
        for line in input_lines:
            formatted_line: str = re.sub(COMMENT_REGEX, "", line)
            if formatted_line:
                self._formated_lines.append(formatted_line)
        self._line_num: int = len(self._formated_lines)
        self._current_line: int = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self._current_line < self._line_num

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        self._current_command: str = self._formated_lines[self._current_line]
        self._current_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        commands = {"return": "C_RETURN", "call": "C_CALL", "function": "C_FUNCTION",
                    "if-goto": "C_IF", "goto": "C_GOTO", "label": "C_LABEL", "pop": "C_POP", "push": "C_PUSH"}
        command=self._current_command.split()[0]
        return commands[command] if command in commands else "C_ARITHMETIC"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        parts = self._current_command.split()
        return parts[0] if len(parts) == 1 else parts[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        return int(self._current_command.split()[2])
