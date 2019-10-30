from Field import Field
from SquareValue import SquareValue
import random


class Game:
    def __init__(self, field, circle_id, cross_id, next_move=SquareValue.CIRCLE):
        self.field = field
        self.circle_id = circle_id
        self.cross_id = cross_id
        self.next_move = next_move

    def check_game(self, field):
        for i in range(3):
            winner = set(field.data[i])
            if len(winner) == 1:
                if SquareValue.CIRCLE in winner:
                    return 'Circle won'
                elif SquareValue.CROSS in winner:
                    return 'Cross won'
            winner = {field.data[0][i], field.data[1][i], field.data[2][i]}
            if len(winner) == 1:
                if SquareValue.CIRCLE in winner:
                    return 'Circle won'
                elif SquareValue.CROSS in winner:
                    return 'Cross won'
        if field.data[0][0] == field.data[1][1] == field.data[2][2] or field.data[0][2] == \
                field.data[1][1] == field.data[2][0]:
            if field.data[1][1] == SquareValue.CIRCLE:
                return 'Circle won'
            elif field.data[1][1] == SquareValue.CROSS:
                return 'Cross won'
        if '0' not in field.toString():
            return 'Tie'
        return 'Continue'

    def move(self, cell):
        self.field.move(cell, self.next_move)
        game_status = self.check_game(self.field)
        self.next_move = SquareValue.CROSS if self.next_move == SquareValue.CIRCLE else SquareValue.CIRCLE

        if self.cross_id == -1 and game_status == 'Continue':
            self.field.move(self.bot_move(), self.next_move)
            game_status = self.check_game(self.field)
            self.next_move = SquareValue.CIRCLE
        return game_status

    def bot_move(self):
        field_str = self.field.toString()
        possible_moves = {}
        for i in range(len(field_str)):
            if field_str[i] == '0':
                possible_field = Field(self.field.toString())
                possible_field.move(i, SquareValue.CIRCLE)
                possible_game_status = self.check_game(possible_field)
                if possible_game_status == 'Circle won':
                    return i
                possible_moves[str(i)] = possible_game_status
        for key, value in possible_moves.items():
            if value == 'Cross won':
                return key
        for i_key in possible_moves.keys():
            for j_key in possible_moves.keys():
                if i_key != j_key:
                    possible_field = Field(self.field.toString())
                    possible_field.move(i_key, SquareValue.CIRCLE)
                    possible_field.move(j_key, SquareValue.CIRCLE)
                    possible_game_status = self.check_game(possible_field)
                    if possible_game_status == 'Cross won':
                        return i_key
        return int(random.choice(list(possible_moves.keys())))
