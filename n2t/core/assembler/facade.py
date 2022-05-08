from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from n2t.core.assembler.code import Code
from n2t.core.assembler.parser import Parser
from n2t.core.assembler.symbol_table import SymbolTable


@dataclass
class Assembler:
    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        parser = Parser(assembly)
        self.symbol_table = SymbolTable()
        self.first_pass(assembly)
        ram_address = 16
        code_translator = Code()
        lines = []
        while parser.has_more_commands():
            parser.advance()
            line = ""
            command_type = parser.command_type()
            if command_type in ["comment", "empty_line", "pseudo_command"]:
                continue
            if command_type in ["A_COMMAND", "C_COMMAND"]:
                if command_type == "C_COMMAND":
                    line = "111"
                    line += code_translator.comp(parser.comp())
                    line += code_translator.dest(parser.dest())
                    line += code_translator.jump(parser.jump())
                else:
                    line = "0"
                    is_number = False
                    num = 0
                    try:
                        num = int(parser.value())
                        is_number = True
                    except ValueError:
                        pass

                    if is_number:
                        line = bin(num).replace("0b", "")
                        line = line.rjust(16, "0")
                    else:
                        symbol = parser.value()
                        if self.symbol_table.contains(symbol):
                            num = int(self.symbol_table.get_address(symbol))
                            line = bin(num).replace("0b", "")
                            line = line.rjust(16, "0")
                        else:
                            self.symbol_table.add_entry(symbol, ram_address)
                            ram_address += 1
                            num = int(self.symbol_table.get_address(symbol))
                            line = bin(num).replace("0b", "")
                            line = line.rjust(16, "0")
            lines.append(line)
        return lines

    def first_pass(self, assembly: Iterable[str]) -> None:
        counter = 0
        parser = Parser(assembly)
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() in ["A_COMMAND", "C_COMMAND"]:
                counter += 1
            if parser.command_type() == "pseudo_command":
                self.symbol_table.add_entry(parser.symbol(), counter)
