"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self._class_symbol_table = dict()
        self._subroutine_symbol_table = dict()
        self._identifier_counter = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self._subroutine_symbol_table.clear()
        self._identifier_counter["ARG"] = 0
        self._identifier_counter["VAR"] = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind in ["STATIC", "FIELD"]:
            self._class_symbol_table[name] = [type, kind, self._identifier_counter[kind]]
        elif kind in ["ARG", "VAR"]:
            self._subroutine_symbol_table[name] = [type, kind, self._identifier_counter[kind]]
        else:
            raise TypeError("Kind exception")
        self._identifier_counter[kind] += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        return self._identifier_counter[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self._subroutine_symbol_table:
            return self._subroutine_symbol_table[name][0]
        elif name in self._class_symbol_table:
            return self._class_symbol_table[name][0]
        else:
            raise NameError("Kind Of lookup failed :Symbol doesn't exist in scope")

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self._subroutine_symbol_table:
            return self._subroutine_symbol_table[name][1]
        elif name in self._class_symbol_table:
            return self._class_symbol_table[name][1]
        else:
            raise NameError("Type lookup failed :Symbol doesn't exist in scope")

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self._subroutine_symbol_table:
            return self._subroutine_symbol_table[name][2]
        elif name in self._class_symbol_table:
            return self._class_symbol_table[name][2]
        else:
            raise NameError("Index Of lookup failed :Symbol doesn't exist in scope")
