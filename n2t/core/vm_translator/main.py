from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from n2t.core.vm_translator.code_writer import CodeWriter
from n2t.core.vm_translator.parser import Parser
from n2t.infra.io import FileFormat


@dataclass
class VMTranslator:
    @classmethod
    def create(cls) -> VMTranslator:
        return cls()

    def translate(self, file_path: str) -> None:
        self.out_file = FileFormat.asm.convert(Path(file_path))
        if ".vm" not in file_path:
            n1 = file_path.split("/")
            n2 = file_path.split("\\")
            if len(n1) > len(n2):
                self.out_file = FileFormat.asm.convert(Path(file_path + "/" + n1[-1]))
            else:
                self.out_file = FileFormat.asm.convert(Path(file_path + "\\" + n2[-1]))
        self.file_names: List[str] = []
        flag: bool = False
        if ".vm" in file_path:
            self.file_names.append(file_path)
        else:
            iterator = Path(file_path).iterdir()
            for e in iterator:
                str_e = str(e)
                if ".vm" in str_e:
                    self.file_names.append(str_e)
                if "Sys.vm" in str_e:
                    flag = True

        self.code_writer = CodeWriter(self.out_file)
        if flag:
            self.code_writer.write_init()
        for file_name in self.file_names:
            self.code_writer.set_file_name(file_name)
            parser = Parser(Path(file_name))
            while parser.has_more_commands():
                parser.advance()
                self._get_code(parser)

    def _get_code(self, parser: Parser) -> None:
        command_type = parser.command_type()
        if command_type == "C_ARITHMETIC":
            self.code_writer.write_arithmetic(parser.arg1())
        if command_type in ["C_POP", "C_PUSH"]:
            self.code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
        if command_type == "C_CALL":
            self.code_writer.write_call(parser.arg1(), parser.arg2())
        if command_type == "C_FUNCTION":
            self.code_writer.write_function(parser.arg1(), parser.arg2())
        if command_type == "C_RETURN":
            self.code_writer.write_return()
        if command_type == "C_GOTO":
            self.code_writer.write_goto(parser.arg1())
        if command_type == "C_IF":
            self.code_writer.write_if(parser.arg1())
        if command_type == "C_LABEL":
            self.code_writer.write_label(parser.arg1())
