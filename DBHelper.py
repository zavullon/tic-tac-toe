import psycopg2
import os
import Field


class DBHelper:
    def __init__(self):
        self.DBNAME = os.environ.get('DATABASE')
        self.USER = os.environ.get('USER')
        self.PASSWORD = os.environ.get('PASSWORD')
        self.HOST = os.environ.get('HOST')
        self.conn = psycopg2.connect(dbname=self.DBNAME, user=self.USER, password=self.PASSWORD, host=self.HOST)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists games('
                            '   game_id serial primary key'
                            '   circle_id serial'
                            '   cross_id serial'
                            '   game_status varchar(9)'
                            ')')

    def get_last_game(self, circle_id, cross_id):
        self.cursor.execute('select game_status from games'
                            'where circle_id = %s'
                            'and cross_id = %s', str(circle_id), str(cross_id))
        return self.cursor[0] if len(self.cursor) else None

    def update_last_game(self, circle_id, cross_id, game_status):
        if self.get_last_game(circle_id, cross_id) is not None:
            self.cursor.execute('update games set game_status = %s'
                                'where circle_id = %s and cross_id = %s', str(game_status), str(circle_id), str(cross_id))
        else:
            self.cursor.execute('insert into games (circle_id, cross_id, game_status) values(%s, %s, %s)', str(circle_id), str(cross_id), str(game_status))