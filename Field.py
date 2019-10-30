from SquareValue import SquareValue
from telegram import InlineKeyboardButton


class Field:
    def __init__(self, str_field='000000000'):
        self.data = [[SquareValue(int(i)) for i in str_field[j:j + 3]] for j in range(0, 9, 3)]

    def toField(self, str_field):
        self.data = [[SquareValue(int(i)) for i in str_field[j:j + 3]] for j in range(0, 9, 3)]

    def toString(self):
        res = ''

        for i in self.data:
            for j in i:
                res += str(j.value)
        return res

    def move(self, cell, move_type):
        self.data[cell // 3][cell % 3] = move_type

    def toLetter(self, state):
        return 'X' if state == 2 else '0'

    def isEmpty(self, cell):
        return self.data[cell // 3][cell % 3] == SquareValue.BLANK

    def toPrint(self):
        res = []
        count = 0

        for i in self.data:
            tmp = []
            for j in i:
                tmp.append(
                    InlineKeyboardButton(
                        self.toLetter(j.value) if j == SquareValue.CIRCLE or j == SquareValue.CROSS else '_',
                        callback_data=str(count)))
                count += 1
            res.append(tmp)
        return res
