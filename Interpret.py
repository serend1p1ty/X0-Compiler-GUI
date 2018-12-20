from ctypes import *
from stackobj import *
from copy import deepcopy


MAX_LEN_IDENT = 20
MAX_DIMENSION = 10
MAX_SIZE_TABLE = 100
MAX_NUM_FUNCTION = 100
MAX_NUM_CODE = 1000
MAX_SIZE_STACK = 10000


class ObjectKind(object):
    intVar = 0
    constIntVar = 1
    intArray = 2
    doubleVar = 3
    constDoubleVar = 4
    doubleArray = 5
    charVar = 6
    constCharVar = 7
    charArray = 8
    boolVar = 9
    constBoolVar = 10
    boolArray = 11


class RetType(object):
    retVoid = 0
    retInt = 1
    retDouble = 2
    retChar = 3
    retBool = 4


class FctCode(object):
    lit = 0
    opr = 1
    lod = 2
    sto = 3
    cal = 4
    ini = 5
    jmp = 6
    jpc = 7
    add = 8
    sub = 9
    tad = 10


class Instruction(Structure):
    _fields_ = [('fct', c_int),
                ('opr1', c_int),
                ('opr2', c_double)]


class TableObject(Structure):
    _fields_ = [('name', c_char * (MAX_LEN_IDENT + 1)),
                ('kind', c_int),
                ('offset', c_int),
                ('size', c_int * MAX_DIMENSION),
                ('d', c_int),
                ('value', c_double)]


class FunctionInfo(Structure):
    _fields_ = [('name', c_char * (MAX_LEN_IDENT + 1)),
                ('symTable', TableObject * MAX_SIZE_TABLE),
                ('tableSize', c_int),
                ('paraNum', c_int),
                ('startINTCode', c_int),
                ('retType', c_int)]


p = 0
b = 1
t = 0
fctInfo = (FunctionInfo * MAX_NUM_FUNCTION)()
fctNum = 0
code = (Instruction * MAX_NUM_CODE)()
codeNum = 0
s = [StackObject() for i in range(MAX_SIZE_STACK)]
stype = [str() for i in range(MAX_SIZE_STACK)]


def FindPosition(offset, pos):
    for i in range(fctInfo[pos].tableSize):
        if fctInfo[pos].symTable[i].offset == offset:
            return i
    return -1

def init():
    global p, b, t, fctNum, codeNum, s
    p = 0
    b = 1
    t = 0
    fctNum = 0
    codeNum = 0
    s = [StackObject() for i in range(MAX_SIZE_STACK)]

def loadData():
    global fctNum, codeNum
    init()

    with open('./data/fctInfo.bin', 'rb') as file:
        x = FunctionInfo()
        while file.readinto(x) == sizeof(x):
            fctInfo[fctNum] = x
            fctNum = fctNum + 1
    with open('./data/code.bin', 'rb') as file:
        x = Instruction()
        while file.readinto(x) == sizeof(x):
            code[codeNum] = x
            codeNum = codeNum + 1


def ConvertToInt(num):
    if num > 0:
        temp = 0.5
    else:
        temp = -0.5
    return int(num + temp)


def interpretOneStep(output):
    global p, b, t

    s[1].dataType = DataType.Int
    s[1].intData = 0
    stype[1] = "null"
    s[2].dataType = DataType.Int
    s[2].intData = 1
    stype[2] = "DL"
    s[3].dataType = DataType.Int
    s[3].intData = 0
    stype[3] = "RA"

    inst = code[p]
    p = p + 1
    fct = inst.fct
    if fct == FctCode.lit:
        t = t + 1
        if inst.opr2 == 0:
            s[t].dataType = DataType.Int
            s[t].intData = inst.opr1
        else:
            s[t].dataType = DataType.Double
            s[t].dblData = inst.opr2
        stype[t] = "null"
    elif fct == FctCode.opr:
        if inst.opr1 == 0:
            fctIndex = ConvertToInt(inst.opr2)
            paraNum = fctInfo[fctIndex].paraNum
            retType = fctInfo[fctIndex].retType
            intTmp = t
            t = b - 1
            p = s[t + 3].intData
            b = s[t + 2].intData
            t = t - paraNum
            if retType != RetType.retVoid:
                t = t + 1
                s[t] = deepcopy(s[intTmp])
        elif inst.opr1 == 1:
            s[t] = -s[t]
        elif inst.opr1 == 2:
            t = t - 1
            s[t] = s[t] + s[t + 1]
        elif inst.opr1 == 3:
            t = t - 1
            s[t] = s[t] - s[t + 1]
        elif inst.opr1 == 4:
            t = t - 1
            s[t] = s[t] * s[t + 1]
        elif inst.opr1 == 5:
            t = t - 1
            s[t] = s[t] / s[t + 1]
        elif inst.opr1 == 6:
            t = t - 1
            s[t] = s[t] % s[t + 1]
        elif inst.opr1 == 7:
            t = t - 1
            if s[t + 1].dataType == DataType.Double:
                print("the parameter of exit function must be integer!")
                exit(1)
            exit(s[t + 1].intData)
        elif inst.opr1 == 8:
            t = t - 1
            s[t] = (s[t] == s[t + 1])
        elif inst.opr1 == 9:
            t = t - 1
            s[t] = (s[t] != s[t + 1])
        elif inst.opr1 == 10:
            t = t - 1
            s[t] = (s[t] < s[t + 1])
        elif inst.opr1 == 11:
            t = t - 1
            s[t] = (s[t] >= s[t + 1])
        elif inst.opr1 == 12:
            t = t - 1
            s[t] = (s[t] > s[t + 1])
        elif inst.opr1 == 13:
            t = t - 1
            s[t] = (s[t] <= s[t + 1])
        elif inst.opr1 == 14:
            t = t + 1
            stype[t] = "null"
            s[t].dataType = ConvertToInt(inst.opr2)
            if s[t].dataType == DataType.Int or s[t].dataType == DataType.Bool:
                s[t].intData = int(input())
            elif s[t].dataType == DataType.Char:
                s[t].intData = input()
            else:
                s[t].dblData = float(input())
        elif inst.opr1 == 15:
            if s[t].dataType == DataType.Int or s[t].dataType == DataType.Bool:
                output.appendPlainText("%s" % s[t].intData)
                # print(s[t].intData)
            elif s[t].dataType == DataType.Double:
                output.appendPlainText("%s" % round(s[t].dblData, 2))
                # print(round(s[t].dblData, 2))
            elif s[t].dataType == DataType.Char:
                output.appendPlainText("%s" % chr(s[t].intData))
                # print(chr(s[t].intData))
            t = t - 1
        elif inst.opr1 == 16:
            t = t - 1
            s[t] = s[t] and s[t + 1]
        elif inst.opr1 == 17:
            t = t - 1
            s[t] = s[t] or s[t + 1]
        elif inst.opr1 == 18:
            s[t].dataType = DataType.Bool
            s[t].intData = not s[t].intData
        elif inst.opr1 == 19:
            t = t - 1
            s[t] = s[t] ^ s[t + 1]
        elif inst.opr1 == 20:
            if s[t].dataType == DataType.Double:
                print("the operand of odd must be integer!")
                exit(1)
            s[t].intData = s[t].intData % 2
            s[t].dataType = DataType.Bool
        elif inst.opr1 == 21:
            s[t] = (s[t - 1] == s[t])
        else:
            print("illegal operand of 'opr' instruction")
            exit(1)
    elif fct == FctCode.lod:
        fctIndex = ConvertToInt(inst.opr2)
        pos = FindPosition(inst.opr1, fctIndex)
        d = fctInfo[fctIndex].symTable[pos].d
        offset = 0
        for i in range(d):
            if s[t + 1 - d + i].dataType == DataType.Double:
                print("the subscript of array must be integer!")
                exit(1)
            offset = offset * fctInfo[fctIndex].symTable[pos].size[i] + s[t + 1 - d + i].intData
        s[t + 1 - d] = deepcopy(s[b + inst.opr1 + offset])
        t = t + 1 - d
        stype[t] = "null"
    elif fct == FctCode.sto:
        fctIndex = ConvertToInt(inst.opr2)
        pos = FindPosition(inst.opr1, fctIndex)
        d = fctInfo[fctIndex].symTable[pos].d
        offset = 0
        for i in range(d):
            if s[t - d + i].dataType == DataType.Double:
                print("the subscript of array must be integer!")
                exit(1)
            offset = offset * fctInfo[fctIndex].symTable[pos].size[i] + s[t - d + i].intData
        s[b + inst.opr1 + offset].assign(s[t])
        s[t - d] = deepcopy(s[t])
        t = t - d
    elif fct == FctCode.add:
        fctIndex = ConvertToInt(inst.opr2)
        pos = FindPosition(inst.opr1, fctIndex)
        d = fctInfo[fctIndex].symTable[pos].d
        offset = 0
        for i in range(d):
            if s[t + 1 - d + i].dataType == DataType.Double:
                print("the subscript of array must be integer!")
                exit(1)
            offset = offset * fctInfo[fctIndex].symTable[pos].size[i] + s[t + 1 - d + i].intData
        s[b + inst.opr1 + offset].intData += 1
    elif fct == FctCode.sub:
        fctIndex = ConvertToInt(inst.opr2)
        pos = FindPosition(inst.opr1, fctIndex)
        d = fctInfo[fctIndex].symTable[pos].d
        offset = 0
        for i in range(d):
            if s[t + 1 - d + i].dataType == DataType.Double:
                print("the subscript of array must be integer!")
                exit(1)
            offset = offset * fctInfo[fctIndex].symTable[pos].size[i] + s[t + 1 - d + i].intData
        s[b + inst.opr1 + offset].intData -= 1
    elif fct == FctCode.tad:
        if s[t].dataType == DataType.Double:
            print("top element isn't integer, 'tad' instruction can't work!")
            exit(1)
        s[t].intData += inst.opr1
    elif fct == FctCode.cal:
        s[t + 1].dataType = DataType.Int
        s[t + 1].intData = 0
        stype[t + 1] = "null"
        s[t + 2].dataType = DataType.Int
        s[t + 2].intData = b
        stype[t + 2] = "DL"
        s[t + 3].dataType = DataType.Int
        s[t + 3].intData = p
        stype[t + 3] = "RA"
        b = t + 1
        p = inst.opr1
    elif fct == FctCode.ini:
        t = b + 2
        paraNum = fctInfo[inst.opr1].paraNum
        for i in range(fctInfo[inst.opr1].tableSize):
            to = fctInfo[inst.opr1].symTable[i]
            totalSize = 1
            for j in range(to.d):
                totalSize *= to.size[j]
            for j in range(1, totalSize + 1):
                # remove redundent 'b' and two single quotes.
                name = str(to.name)[2:]
                name = name[:len(name) - 1]
                if totalSize > 1:
                    stype[t + 1] = name + '[' + str(j - 1) + ']'
                else:
                    stype[t + 1] = name

                if to.kind == ObjectKind.intArray or to.kind == ObjectKind.intVar:
                    t = t + 1
                    s[t].dataType = DataType.Int
                elif to.kind == ObjectKind.constIntVar:
                    t = t + 1
                    s[t].dataType = DataType.Int
                    s[t].intData = ConvertToInt(to.value)
                elif to.kind == ObjectKind.doubleArray or to.kind == ObjectKind.doubleVar:
                    t = t + 1
                    s[t].dataType = DataType.Double
                elif to.kind == ObjectKind.constDoubleVar:
                    t = t + 1
                    s[t].dataType = DataType.Double
                    s[t].dblData = to.value
                elif to.kind == ObjectKind.charArray or to.kind == ObjectKind.charVar:
                    t = t + 1
                    s[t].dataType = DataType.Char
                elif to.kind == ObjectKind.constCharVar:
                    t = t + 1
                    s[t].dataType = DataType.Char
                    s[t].intData = ConvertToInt(to.value)
                elif to.kind == ObjectKind.boolArray or to.kind == ObjectKind.boolVar:
                    t = t + 1
                    s[t].dataType = DataType.Bool
                elif to.kind == ObjectKind.constBoolVar:
                    t = t + 1
                    s[t].dataType = DataType.Bool
                    s[t].intData = ConvertToInt(to.value)
        for i in range(paraNum):
            s[b + 3 + i].assign(s[b - paraNum + i])
    elif fct == FctCode.jmp:
        p = inst.opr1
    elif fct == FctCode.jpc:
        if s[t].intData == 0:
            p = inst.opr1
        t = t - 1
    else:
        print("illegal function code!")
        exit(1)


def interpretAllStep(output):
    # initStack()
    while 1:
        interpretOneStep(output)
        if p == 0:
            break