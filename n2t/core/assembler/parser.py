import re
from typing import Iterable


class Parser:
    def __init__(self, assembly: Iterable[str]):
        temp = assembly.__iter__()
        self.line_count = 0
        print(temp)
        for line in assembly:
            self.line_count += 1
        self.asm_prog = temp
        self.curr_count = 0
        pass

    def has_more_commands(self) -> bool:
        if self.curr_count >= self.line_count:
            return False
        return True

    def advance(self) -> None:
        self.curr_count += 1
        self.curr_command = ""
        temp = next(self.asm_prog)
        temp_words = temp.split()
        temp = ""
        for word in temp_words:
            temp += word
        if len(temp) > 1 and temp[0:2:1] == "//":
            self.curr_command = "//"
            return
        parts = temp.split("//")
        if len(temp) > 0:
            self.curr_command = parts[0]
        self.c_command_words = re.split("=|;", self.curr_command)

    def command_type(self) -> str:
        words = self.curr_command.split()
        if len(words) == 0:
            return "empty_line"
        first_word = words[0]
        if len(first_word) >= 2 and first_word[0:2:1] == "//":
            return "comment"
        if first_word[0] == "@":
            return "A_COMMAND"
        if first_word[0] == "(":
            return "pseudo_command"
        return "C_COMMAND"

    def symbol(self) -> str:
        return self.substr(self.curr_command, 1, len(self.curr_command) - 1)

    def dest(self) -> str:
        command = ""
        if "=" in self.curr_command:
            parts_of_command: list[str] = self.c_command_words[0].split()
            for elem in parts_of_command:
                command += elem
            return command
        return ""

    def comp(self) -> str:
        parts_of_comp: list[str] = []
        if "=" in self.curr_command:
            parts_of_comp = self.c_command_words[1].split()
        else:
            parts_of_comp = self.c_command_words[0].split()
        comp_command = ""
        for elem in parts_of_comp:
            comp_command += elem
        return comp_command

    def jump(self) -> str:
        command = ""
        if ";" in self.curr_command:
            parts_of_command = self.c_command_words[
                len(self.c_command_words) - 1
            ].split()
            for elem in parts_of_command:
                command += elem
            return command
        return ""

    def value(self) -> str:
        return self.substr(self.curr_command, 1, len(self.curr_command))
        # return self.curr_command[1 : len(self.curr_command) : 1]

    def substr(self, string: str, start: int, end: int) -> str:
        count: int = 0
        substring: str = ""
        for symbol in string:
            if count >= start and count < end:
                substring += symbol
            if count > end:
                break
            count += 1
        return substring
