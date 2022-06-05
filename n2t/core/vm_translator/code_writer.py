from pathlib import Path


class CodeWriter:
    def __init__(self, out_path: Path) -> None:
        self.file_name = ""
        self.output_file = open(out_path, "w")
        self.label_number = 0
        self.curr_label = ""
        self.address_space = {
            "this": "THIS",
            "that": "THAT",
            "pointer": 3,
            "argument": "ARG",
            "temp": 5,
            "local": "LCL",
            "static": 16,
        }
        self.num_call = 0

    def next_label(self) -> str:
        self.label_number += 1
        self.curr_label = "LABEL" + str(self.label_number)
        return self.curr_label

    def set_file_name(self, name: str) -> None:
        temp_arr = name.split("\\")
        if len(temp_arr) <= 1:
            temp_arr = name.split("/")
        if len(temp_arr) == 0:
            self.file_name = ""
        self.file_name = temp_arr[-1].replace(".vm", "").replace(".asm", "")

    def is_binary(self, name: str) -> bool:
        return name in ["sub", "and", "or", "add", "gt", "lt", "eq"]

    def write_arithmetic(self, command: str) -> None:
        if self.is_binary(command):
            self._save_stack_to_d()

        self._change_stack_val("-")
        self._dereference_sp()
        # binary arithmetic operators
        if command == "add":
            self.write("M=M+D")
        elif command == "sub":
            self.write("M=M-D")
        elif command == "and":
            self.write("M=M&D")
        elif command == "or":
            self.write("M=M|D")
        # unary arithmetic operators
        elif command == "not":
            self.write("M=!M")
        elif command == "neg":
            self.write("M=-M")
        # binary comparison operators
        if command in ["eq", "gt", "lt"]:
            self.write("D=M-D")
            self.write("@" + self.next_label())
            self.write("D;" + "J" + command.upper())
            temp_label = self.curr_label
            self._dereference_sp()
            self.write("M=0")  # false
            self.write("@" + self.next_label())
            self.write("0;JMP")
            self.write(f"({temp_label})")
            self._dereference_sp()
            self.write("M=-1")  # true
            self.write(f"({self.curr_label})")

        self._change_stack_val("+")

    def _save_stack_to_d(self) -> None:
        self._change_stack_val("-")
        self.write("A=M")
        self.write("D=M")

    def _save_d_to_stack(self) -> None:
        self._dereference_sp()
        self.write("M=D")
        self._change_stack_val("+")

    def _dereference_sp(self) -> None:
        self.write("@SP")
        self.write("A=M")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        self._get_address(segment, index)
        match (command):
            case "C_PUSH":
                self._push_command(segment)
            case _:
                self._pop_command(segment)

    def _push_command(self, segment: str) -> None:
        if segment == "constant":
            self.write("D=A")
        else:
            self.write("D=M")
        self._save_d_to_stack()

    def _pop_command(self, segment: str) -> None:
        self.write("D=A")
        self.write("@R13")
        self.write("M=D")
        self._save_stack_to_d()
        self.write("@R13")
        self.write("A=M")
        self.write("M=D")

    def _get_address(self, segment: str, index: int) -> None:
        if segment == "constant":
            self.write("@" + str(index))
            return
        address = self.address_space[segment]
        if segment == "static":
            self.write("@" + self.file_name + "." + str(index))
        elif segment == "pointer":
            self.write(f"@R{str(3 + index)}")
        elif segment == "temp":
            self.write(f"@R{str(5 + index)}")
        elif segment in ["local", "argument", "this", "that"]:
            self.write("@" + str(address))
            self.write("D=M")
            self.write("@" + str(index))
            self.write("A=D+A")

    def _change_stack_val(self, operator: str) -> None:
        self.write("@SP")
        self.write("M=M" + operator + "1")

    def write(self, line: str) -> None:
        self.output_file.write(line + "\n")

    def write_init(self) -> None:
        # make sp equal to 256
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write_call("Sys.init", 0)

    def write_label(self, label: str) -> None:
        self.write("(" + self.file_name + "$" + label + ")")

    def write_goto(self, label: str) -> None:
        self.write("@" + self.file_name + "$" + label)
        self.write("0;JMP")

    def write_if(self, label: str) -> None:
        self._save_stack_to_d()
        self.write("@" + self.file_name + "$" + label)
        self.write("D;JNE")

    def write_call(self, function_name: str, num_args: int) -> None:
        # push return_address to stack
        return_address = self.next_label()
        self.write("@" + return_address)
        self.write("D=A")
        self._save_d_to_stack()

        # push LCL, ARG, THIS and THAT segment addresses to stack
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self._write_address_to_stack(segment)

        # ARG = SP - n - 5
        self.write("@SP")
        self.write("D=M")
        self.write("@" + str(num_args))
        self.write("D=D-A")
        self.write("@5")
        self.write("D=D-A")
        self.write("@ARG")
        self.write("M=D")

        # LCL = SP
        self.write("@SP")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")

        # goto function_name
        self.write("@" + function_name)
        self.write("0;JMP")

        # (return_address)
        self.write(f"({return_address})")

    def write_return(self) -> None:
        frame = "R13"
        ret = "R14"

        # FRAME = LCL
        self.write("@LCL")
        self.write("D=M")
        self.write("@" + frame)
        self.write("M=D")

        # RET = *(FRAME - 5)
        self._dereference_with_offset(frame, 5)
        self.write("@" + ret)
        self.write("M=D")

        # *ARG = POP()
        self._save_stack_to_d()
        self.write("@ARG")
        self.write("A=M")
        self.write("M=D")

        # SP = ARG + 1
        self.write("@ARG")
        self.write("D=M")
        self.write("@1")
        self.write("D=D+A")
        self.write("@SP")
        self.write("M=D")

        # THAT = *(FRAME - 1)
        # THIS = *(FRAME - 2)
        # ARG = *(FRAME - 3)
        # LCL = *(FRAME - 4)
        for e in [("@THAT", 1), ("@THIS", 2), ("@ARG", 3), ("@LCL", 4)]:
            offset = e[1]
            var = e[0]
            self._dereference_with_offset(frame, offset)
            self.write(var)
            self.write("M=D")

        # goto RET
        self.write(f"@{ret}")
        self.write("A=M")
        self.write("0;JMP")

    def _dereference_with_offset(self, address: str, offset: int) -> None:
        self.write(f"@{address}")
        self.write("D=M")
        self.write(f"@{str(offset)}")
        self.write("D=D-A")
        self.write("A=D")
        self.write("D=M")

    def write_function(self, function_name: str, num_locals: int) -> None:
        self.write("(" + function_name + ")")

        for x in range(num_locals):
            self.write_push_pop("C_PUSH", "constant", 0)

    def _write_address_to_stack(self, address: str) -> None:
        self.write("@" + address)
        self.write("D=M")
        self._save_d_to_stack()
