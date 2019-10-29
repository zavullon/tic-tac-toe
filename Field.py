import SquareValue


class Field:
    def init(self, str_field='000000000'):
        self.data = [[SquareValue(int(i)) for i in str_field[j:j + 3]] for j in range(0, 9, 3)]

    def toField(self, str_field):
        self.data = [[SquareValue(int(i)) for i in str_field[j:j + 3]] for j in range(0, 9, 3)]

    def toString(self, reg_field):
        res = ''
        for i in reg_field:
            for j in i:
                res += str(j.value)
        return res

    def move(self, cell, move_type):
        self.data[cell // 3][cell % 3] = move_type

    def toPrint(self):
        return [[str(i.value) for i in j] for j in self.data]
