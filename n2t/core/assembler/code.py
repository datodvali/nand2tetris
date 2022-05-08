class Code:
    def __init__(self) -> None:
        pass

    def dest(self, dest_command: str) -> str:
        if len(dest_command) == 0:
            return "000"
        if dest_command == "M":
            return "001"
        if dest_command == "D":
            return "010"
        if dest_command == "MD":
            return "011"
        if dest_command == "A":
            return "100"
        if dest_command == "AM":
            return "101"
        if dest_command == "AD":
            return "110"
        if dest_command == "AMD":
            return "111"
        else:
            return "Error"

    def jump(self, jump_command: str) -> str:
        if len(jump_command) == 0:
            return "000"
        if jump_command == "JGT":
            return "001"
        if jump_command == "JEQ":
            return "010"
        if jump_command == "JGE":
            return "011"
        if jump_command == "JLT":
            return "100"
        if jump_command == "JNE":
            return "101"
        if jump_command == "JLE":
            return "110"
        if jump_command == "JMP":
            return "111"
        else:
            return "Error"

    def comp(self, comp_command: str) -> str:
        if comp_command == "0":
            return "0101010"
        if comp_command == "1":
            return "0111111"
        if comp_command == "-1":
            return "0111010"
        if comp_command == "D":
            return "0001100"
        if comp_command == "A":
            return "0110000"
        if comp_command == "!D":
            return "0001101"
        if comp_command == "!A":
            return "0110001"
        if comp_command == "-D":
            return "0001111"
        if comp_command == "-A":
            return "0110011"
        if comp_command == "D+1":
            return "0011111"
        if comp_command == "A+1":
            return "0110111"
        if comp_command == "D-1":
            return "0001110"
        if comp_command == "A-1":
            return "0110010"
        if comp_command == "D+A":
            return "0000010"
        if comp_command == "D-A":
            return "0010011"
        if comp_command == "A-D":
            return "0000111"
        if comp_command == "D&A":
            return "0000000"
        if comp_command == "D|A":
            return "0010101"
        if comp_command == "M":
            return "1110000"
        if comp_command == "!M":
            return "1110001"
        if comp_command == "-M":
            return "1110011"
        if comp_command == "M+1":
            return "1110111"
        if comp_command == "M-1":
            return "1110010"
        if comp_command == "D+M":
            return "1000010"
        if comp_command == "D-M":
            return "1010011"
        if comp_command == "M-D":
            return "1000111"
        if comp_command == "D&M":
            return "1000000"
        if comp_command == "D|M":
            return "1010101"
        return "Error"
