import psycopg2
import os
from Field import Field
from Game import Game
from SquareValue import SquareValue


class DBHelper:
    def __init__(self):
        self.DBNAME = 'd9adc8komarmp8'  # os.environ.get('DATABASE')
        self.USER = 'gvchedvapftewe'  # os.environ.get('USER')
        self.PASSWORD = 'f6f2b3c30707fac2804ab04aba7025654c2c0747bd4b7c2275714d08dba9af9f'  # os.environ.get('PASSWORD')
        self.HOST = 'ec2-174-129-252-228.compute-1.amazonaws.com'  # os.environ.get('HOST')
        self.conn = psycopg2.connect(dbname=self.DBNAME, user=self.USER, password=self.PASSWORD, host=self.HOST)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists games('
                            '   game_id serial primary key,'
                            '   circle_id serial,'
                            '   cross_id serial,'
                            '   game_status varchar(9),'
                            '   next_move serial'
                            ');')
        self.conn.commit()

    def get_last_game(self, circle_id, cross_id):
        self.cursor.execute("select game_status, circle_id, cross_id, next_move from games "
                            "where (circle_id = {} "
                            "and cross_id = {}) "
                            "or (cross_id = {} "
                            "and circle_id = {})".format(circle_id, cross_id, circle_id, cross_id))
        rows = self.cursor.fetchall()
        return Game(Field(rows[0][0]), int(rows[0][1]), int(rows[0][2]), SquareValue(rows[0][3])) if len(rows) != 0 else None

    def update_last_game(self, game):
        if self.get_last_game(game.circle_id, game.cross_id) is not None:
            self.cursor.execute("update games set game_status = '{}', "
                                "next_move = {} "
                                "where circle_id = {} and cross_id = {}".format(game.field.toString(),
                                                                                game.next_move.value,
                                                                                game.circle_id, game.cross_id))
            self.conn.commit()
        else:
            self.cursor.execute("select max(game_id) from games")
            rows = self.cursor.fetchall()
            max_id = 0
            if rows[0][0] is not None:
                max_id = rows[0][0]
            self.cursor.execute(
                "insert into games (game_id, circle_id, cross_id, game_status, next_move) values({}, {}, {}, '{}', {})".
                    format(max_id + 1, game.circle_id, game.cross_id, game.field.toString(), game.next_move.value))
            self.conn.commit()
