from pathlib import Path
from typing import List

from n2t.infra.io import File


class Parser:
    def __init__(self, path: Path) -> None:
        self.arithmetic_commands = [
            "neg",
            "add",
            "sub",
            "eq",
            "gt",
            "lt",
            "and",
            "or",
            "not",
        ]
        self.lines = File(path).load()
        self.iterator = File(path).load().__iter__()
        self.num_lines = 0
        for line in self.lines:
            self.num_lines += 1
        self.curr_line = 0
        self.curr_command: List[str] = []
        return

    def has_more_commands(self) -> bool:
        return self.curr_line < self.num_lines

    def command_type(self) -> str:
        if len(self.curr_command) == 0:
            return "NOT_A_COMMAND"
        if self.curr_command[0] == "label":
            return "C_LABEL"
        if self.curr_command[0] == "push":
            return "C_PUSH"
        if self.curr_command[0] == "pop":
            return "C_POP"
        if self.curr_command[0] in self.arithmetic_commands:
            return "C_ARITHMETIC"
        if self.curr_command[0] == "goto":
            return "C_GOTO"
        if self.curr_command[0] == "label":
            return "C_LABEL"
        if self.curr_command[0] == "call":
            return "C_CALL"
        if self.curr_command[0] == "return":
            return "C_RETURN"
        if self.curr_command[0] == "if-goto":
            return "C_IF"
        if self.curr_command[0] == "function":
            return "C_FUNCTION"
        return "error"

    def advance(self) -> None:
        line = next(self.iterator)
        self.curr_line += 1
        self.curr_command = []
        if len(line) == 0:
            return
        words = line.split()
        if words[0][0:2:1] == "//":
            return
        command = ""
        for i in range(len(words) - 1):
            command += words[i] + " "
        command += words[len(words) - 1]
        command_parts = command.split("//")
        if len(command_parts) == 0:
            return
        command = command_parts[0]
        self.curr_command = command.split(" ")

    def arg1(self) -> str:
        if self.command_type() == "C_ARITHMETIC":
            return self.curr_command[0]
        else:
            return self.curr_command[1]

    def arg2(self) -> int:
        return int(self.curr_command[2])
