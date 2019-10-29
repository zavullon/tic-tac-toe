from Field import Field
from SquareValue import SquareValue


class Game:
    def __init__(self, field, circle_id, cross_id, next_move=SquareValue.CIRCLE):
        self.field = field
        self.circle_id = circle_id
        self.cross_id = cross_id
        self.next_move = next_move

    def move(self, cell):
        self.field.move(cell, self.next_move)
        self.next_move = SquareValue.CROSS if self.next_move == SquareValue.CIRCLE else SquareValue.CIRCLE
        if self.cross_id == -1:
            self.field.move(self.bot_move(), self.next_move)
            self.next_move = SquareValue.CIRCLE

    def bot_move(self):
        pass
