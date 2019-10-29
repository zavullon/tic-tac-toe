import SquareValue


class Field:
    def init(self):
        self.data = [[SquareValue(0), SquareValue(0), SquareValue(0)],
                     [SquareValue(0), SquareValue(0), SquareValue(0)],
                     [SquareValue(0), SquareValue(0), SquareValue(0)]]

    def toField(self, str_field):
        self.data = [[SquareValue(int(i)) for i in str_field[j:j + 3]] for j in range(0, 9, 3)]

    def fromField(self, reg_field):
        res = ''
        for i in reg_field:
            for j in i:
                res += str(j.value)
        return res
