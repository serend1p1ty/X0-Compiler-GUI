class DataType(object):
    Nul = 0
    Int = 1
    Double = 2
    Char = 3
    Bool = 4


# object stored in data stack
class StackObject:
    def __init__(self):
        self.dataType = DataType.Nul
        self.intData = 0
        self.dblData = 0.0

    @staticmethod
    def result_type(dt1, dt2):
        if dt1 == DataType.Double or dt2 == DataType.Double:
            return DataType.Double
        elif dt1 == DataType.Char or dt2 == DataType.Char:
            return DataType.Char
        else:
            return DataType.Int

    def assign(self, other):
        if self.dataType != DataType.Double:
            if other.dataType != DataType.Double:
                self.intData = other.intData
            else:
                self.intData = other.dblData
        else:
            if other.dataType != DataType.Double:
                self.dblData = other.intData
            else:
                self.dblData = other.dblData

    def __add__(self, other):
        res = StackObject()
        if self.dataType != DataType.Double and other.dataType != DataType.Double:
            res.intData = self.intData + other.intData
        else:
            res.dblData = (self.intData if(self.dataType != DataType.Double) else self.dblData) \
                          + (other.intData if(other.dataType != DataType.Double) else other.dblData)
        res.dataType = StackObject.result_type(self.dataType, other.dataType)
        return res

    def __sub__(self, other):
        res = StackObject()
        if self.dataType != DataType.Double and other.dataType != DataType.Double:
            res.intData = self.intData - other.intData
        else:
            res.dblData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                          - (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = StackObject.result_type(self.dataType, other.dataType)
        return res

    def __mul__(self, other):
        res = StackObject()
        if self.dataType != DataType.Double and other.dataType != DataType.Double:
            res.intData = self.intData * other.intData
        else:
            res.dblData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                          * (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = StackObject.result_type(self.dataType, other.dataType)
        return res

    def __truediv__(self, other):
        res = StackObject()
        if self.dataType != DataType.Double and other.dataType != DataType.Double:
            res.intData = self.intData // other.intData
        else:
            res.dblData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                          / (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = StackObject.result_type(self.dataType, other.dataType)
        return res

    def __neg__(self):
        self.intData = -self.intData
        self.dblData = -self.dblData
        return self

    def __mod__(self, other):
        if self.dataType == DataType.Double or other.dataType == DataType.Double:
            print("the operand of mod operation must be integer!")
            exit(1)
        res = StackObject()
        res.intData = self.intData % other.intData
        res.dataType = DataType.Int
        return res

    def __eq__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      == (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __ne__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      != (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __gt__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      > (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __ge__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      >= (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __lt__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      < (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __le__(self, other):
        res = StackObject()
        res.intData = (self.intData if (self.dataType != DataType.Double) else self.dblData) \
                      <= (other.intData if (other.dataType != DataType.Double) else other.dblData)
        res.dataType = DataType.Bool
        return res

    def __and__(self, other):
        if self.dataType == DataType.Double or other.dataType == DataType.Double:
            print("the operand of && operation must be integer!")
            exit(1)
        res = StackObject()
        res.intData = self.intData and other.intData
        res.dataType = DataType.Bool
        return res

    def __or__(self, other):
        if self.dataType == DataType.Double or other.dataType == DataType.Double:
            print("the operand of || operation must be integer!")
            exit(1)
        res = StackObject()
        res.intData = self.intData or other.intData
        res.dataType = DataType.Bool
        return res

    def __xor__(self, other):
        if self.dataType == DataType.Double or other.dataType == DataType.Double:
            print("the operand of xor operation must be integer!")
            exit(1)
        res = StackObject()
        res.intData = self.intData ^ other.intData
        res.dataType = DataType.Bool
        return res
