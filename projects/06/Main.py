"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    parser: Parser = Parser(input_file)
    symbol_table: SymbolTable = SymbolTable()
    assembled_lines: list[str] = []
    first_pass(parser, symbol_table)
    parser.reset()
    second_pass(parser, symbol_table, assembled_lines)
    output_file.writelines(assembled_lines)


def first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    line_num: int = 0  # Line numbers start at 0
    while parser.has_more_commands():
        parser.advance()
        line_num += 0 if parser.command_type() == "L_COMMAND" else 1
        if parser.command_type() == "L_COMMAND":
            symbol_table.add_entry(parser.symbol(), line_num)


def second_pass(parser: Parser, symbol_table: SymbolTable, assembled_lines: list[str]) -> None:
    address: int = 16  # Variable address starts with RAM[16]
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            address += proccess_A(parser, symbol_table,assembled_lines, address)
        elif parser.command_type() == "C_COMMAND":
            proccess_C(parser, assembled_lines)


def proccess_C(parser: Parser, assembled_lines) -> None:
    dest, comp, jump = Code.dest(parser.dest()), Code.comp(
            parser.comp()), Code.jump(parser.jump())
    shift: str = "0" if "<" in parser.comp() or ">" in parser.comp() else "1"
    assembled_lines.append("1"+shift+"1"+comp+dest+jump+"\n")


def proccess_A(parser: Parser, symbol_table, assembled_lines, address) -> int:
    symbol: str = parser.symbol()
    # If symbol is a Jump reference or declared variable
    if symbol_table.contains(symbol):
        assembled_lines.append(
            f'{int(symbol_table.get_address(symbol)):016b}\n')
        return 0
    elif not symbol.isnumeric():  # Symbol is a new variable
        # print(symbol,address)
        assembled_lines.append(f'{address:016b}\n')
        symbol_table.add_entry(symbol, address)
        return 1
    assembled_lines.append(f'{int(symbol):016b}\n')
    return 0


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path: str = os.path.abspath(sys.argv[1])
    files_to_assemble: list[str] = []
    if os.path.isdir(argument_path):
        files_to_assemble = [os.path.join(
            argument_path, filename) for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path: str = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
