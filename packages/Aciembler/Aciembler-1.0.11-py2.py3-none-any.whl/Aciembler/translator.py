from Aciembler.First_pass import *
import time
from Aciembler.Error import Error

def checkNum(Opcode, Operand):
    if Operand[0] != "#" and not Operand[1:].isdecimal():
        Error('RuntimeError', Opcode, Operand)

def checkAddress(type,Opcode,Operand):
    if type == 0:
        if not Operand.isdecimal():
            Error('RuntimeError', Opcode, Operand)
        if Operand not in DataList.keys():
            Error('RuntimeError', Opcode, Operand)
    elif type == 1:
        if Operand not in Register:
            Error('RuntimeError', Opcode, Operand)
    else:
        if not Operand.isdecimal():
            Error('RuntimeError', Opcode, Operand)
        keys = [i[0] for i in CommandList]
        if Operand not in keys:
            Error('RuntimeError', Opcode, Operand)


def convertBase(add_base):
    for i in range(len(CommandList)):
        Opcode = CommandList[i][1]
        Operand = CommandList[i][2]
        try:
            if Operand != "":
                match Operand[0]:
                    case "&":
                        CommandList[i][2] = "#" + str(int(Operand[1:], base=16))
                    case "B":
                        CommandList[i][2] = "#" + str(int(Operand[1:], base=2))
                    case "#":
                        pass
                    case _:
                        if add_base == 'b':
                            CommandList[i][2] = str(int(Operand, base=2))
                        if add_base == 'h':
                            CommandList[i][2] = str(int(Operand, base=16))

            if add_base == 'b':
                CommandList[i][0] = str(int(CommandList[i][0], base=2))
            if add_base == 'h':
                CommandList[i][0] = str(int(CommandList[i][0], base=16))
        except:
            Error('RuntimeError', Opcode, Operand)

    keys = list(DataList.keys())[::]
    for i in keys:
        Operand = DataList[i]
        if Operand == "":
            continue
        match Operand[0]:
            case "&":
                DataList[i] = "#" + str(int(Operand[1:], base=16))
            case "B":
                DataList[i] = "#" + str(int(Operand[1:], base=2))
            case "#":
                pass
            case _:
                if add_base == 'b':
                    DataList[i] = str(int(Operand, base=2))
                if add_base == 'h':
                    DataList[i] = str(int(Operand, base=16))

        if add_base == 'b':
            DataList.update({str(int(i, base=2)): DataList[i]})
            del DataList[i]
        if add_base == 'h':
            DataList.update({str(int(i, base=16)): DataList[i]})
            del DataList[i]

    for i in Register.keys():
        Operand = Register[i]
        if Operand == "":
            continue
        match Operand[0]:
            case "&":
                DataList[i] = "#" + str(int(Operand[1:], base=16))
            case "B":
                DataList[i] = "#" + str(int(Operand[1:], base=2))



def forward(Startaddress):
    global CommandList, DataList, Register
    CommandList = CommandList[Startaddress - int(CommandList[0][0]):]
    Outputflag = False
    for command in CommandList:
        address = command[0]
        Opcode = command[1]
        Operand = command[2]
        match Opcode:
            case "LDM":
                checkNum(Opcode, Operand)
                Register["ACC"] = "#" + Operand[1:]
            case "LDD":
                checkAddress(0, Opcode, Operand)
                Register["ACC"] = DataList[Operand]
            case "LDI":
                checkAddress(0, Opcode, Operand)
                Operand = DataList[Operand]
                checkAddress(0, Opcode, Operand)
                Register["ACC"] = DataList[Operand]
            case "LDX":
                Operand = str(int(Operand) + int(Register['IX'][1:]))
                checkAddress(0, Opcode, Operand)
                Register["ACC"] = DataList[Operand]
            case "LDR":
                checkNum(Opcode, Operand)
                Register["IX"] = "#" + Operand[1:]
            case "MOV":
                checkAddress(1, Opcode, Operand)
                Register[Operand] = Register["ACC"]
            case "STO":
                checkAddress(0, Opcode, Operand)
                DataList[Operand] = Register["ACC"]
            case "ADD":
                if Operand[0] == '#':
                    checkNum(Opcode, Operand)
                    Register['ACC'] = '#'+str(int(Operand[1:]) + int(Register['ACC'][1:]))
                else:
                    checkAddress(0, Opcode, Operand)
                    Register['ACC'] = '#' + str(int(DataList[Operand][1:]) + int(Register['ACC'][1:]))
            case "SUB":
                if Operand[0] == '#':
                    checkNum(Opcode, Operand)
                    Register['ACC'] = '#' + str(-int(Operand[1:]) + int(Register['ACC'][1:]))
                else:
                    checkAddress(0, Opcode, Operand)
                    Register['ACC'] = '#' + str(-int(DataList[Operand][1:]) + int(Register['ACC'][1:]))
            case "INC":
                checkAddress(1, Opcode, Operand)
                Register[Operand] = '#' + str(int(Register[Operand][1:]) + 1)
            case "DEC":
                checkAddress(1, Opcode, Operand)
                Register[Operand] = '#' + str(int(Register[Operand][1:]) - 1)
            case "JMP":
                checkAddress(2, Opcode, Operand)
                forward(int(Operand))
                return
            case "JPE":
                checkAddress(2, Opcode, Operand)
                last = CommandList[(int(address) - 1 - Startaddress)]
                lastOpcode = last[1]
                lastOperand = last[2]
                if lastOpcode not in ("CMP","CMI"):
                    Error("RuntimeError", lastOpcode, lastOperand)
                if lastOpcode == "CMP":
                    if lastOperand[0] == "#":
                        checkNum(Opcode, lastOperand)
                        JUMP = Register['ACC'] == lastOperand
                    else:
                        checkAddress(0, lastOpcode, lastOperand)
                        JUMP = Register['ACC'] == DataList[lastOperand]
                else:
                    checkAddress(0, lastOpcode, lastOperand)
                    lastOperand = DataList[lastOperand]
                    checkAddress(0, lastOpcode, lastOperand)
                    JUMP = Register['ACC'] == DataList[lastOperand]
                if JUMP:
                    forward(int(Operand))
                    return
            case "JPN":
                checkAddress(2, Opcode, Operand)
                count = 1
                for count in range(1, int(address) - Startaddress):
                    this = CommandList[(int(address) - Startaddress) - count]
                    if this[1] not in ("CMP", "CMI", 'JPE', 'JPN'):
                        count -= 1
                        break
                last = CommandList[(int(address) - count - Startaddress)]
                lastOpcode = last[1]
                lastOperand = last[2]
                if lastOpcode not in ("CMP", "CMI"):
                    Error("RuntimeError", lastOpcode, lastOperand)
                if lastOpcode == "CMP":
                    if lastOperand[0] == "#":
                        checkNum(Opcode, lastOperand)
                        JUMP = Register['ACC'] != lastOperand
                    else:
                        checkAddress(0, lastOpcode, lastOperand)
                        JUMP = Register['ACC'] != DataList[lastOperand]
                else:
                    checkAddress(0, lastOpcode, lastOperand)
                    lastOperand = DataList[lastOperand]
                    checkAddress(0, lastOpcode, lastOperand)
                    JUMP = Register['ACC'] != DataList[lastOperand]
                if JUMP:
                    forward(int(Operand))
                    return
            case "LSL":
                checkNum(Opcode, Operand)
                Register['ACC'] = "#" + str(int(Register['ACC'][1:]) << int(Operand[1:]))
            case "LSR":
                checkNum(Opcode, Operand)
                Register['ACC'] = "#" + str(int(Register['ACC'][1:]) >> int(Operand[1:]))
            case "AND":
                if Operand[0] == '#':
                    checkNum(Opcode, Operand)
                    Register['ACC'] = '#' + str(int(Operand[1:]) & int(Register['ACC'][1:]))
                else:
                    checkAddress(1, Opcode, Operand)
                    Register['ACC'] = '#' + str(int(DataList[Operand][1:]) & int(Register['ACC'][1:]))
            case "OR":
                if Operand[0] == '#':
                    checkNum(Opcode, Operand)
                    Register['ACC'] = '#' + str(int(Operand[1:]) | int(Register['ACC'][1:]))
                else:
                    checkAddress(1, Opcode, Operand)
                    Register['ACC'] = '#' + str(int(DataList[Operand][1:]) | int(Register['ACC'][1:]))
            case "XOR":
                if Operand[0] == '#':
                    checkNum(Opcode, Operand)
                    Register['ACC'] = '#' + str(int(Operand[1:]) ^ int(Register['ACC'][1:]))
                else:
                    checkAddress(1, Opcode, Operand)
                    Register['ACC'] = '#' + str(int(DataList[Operand][1:]) ^ int(Register['ACC'][1:]))
            case "IN":
                Operand = input()
                if len(Operand) == 1 and 0 <= ord(Operand) <= 127:
                    Register['ACC'] = '#' + str(ord(Operand))
            case "OUT":
                if not Outputflag:
                    print('OUTPUT : ', end='')
                    Outputflag = True
                if 0<=int(Register['ACC'][1:])<=127:
                    print(chr(int(Register['ACC'][1:])))
            case "END":
                for i in DataList.items():
                    print(i[0],":",i[1])
                for i in Register.items():
                    print(i[0],":",i[1])
            case "CMP":
                pass
            case "CMI":
                pass
            case _:
                Error("RuntimeError", Opcode, Operand)

CommandList, DataList, Register = [], {}, {}

def run(add_base, path):
    global CommandList, DataList, Register
    CommandList, DataList, Register = first_pass(path=path, add_base=add_base)
    print('First pass complete, doing second pass...')
    time.sleep(0.5)
    convertBase(add_base)
    print('='*20)
    forward(int(CommandList[0][0]))
    print('='*20)

