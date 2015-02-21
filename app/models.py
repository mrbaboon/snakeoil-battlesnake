import random

__author__ = 'awhite'


class Game(object):

    name = None
    snakes = None
    board = None
    turn = None

    def __init__(self, name, turn, snakes, board):
        self.name = name
        self.turn = turn
        self.snakes = snakes
        self.board = board


class Snake(object):

    name = None
    state = None
    coords = None
    health = None
    head = None
    board = None

    left = False

    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

    directions = None

    def __init__(self, name, state, coords, board=None, enemies=None, last_eaten=None):
        self.name = name
        self.state = state
        self.board = board
        self.coords = coords
        self.head_x = coords[0][0]
        self.head_y = coords[0][1]
        self.directions = [
            self.LEFT,
            self.RIGHT,
            self.UP,
            self.DOWN,
        ]

    @property
    def is_alive(self):
        return self.state == 'alive'

    def move(self):
        self.filter_walls()
        self.filter_self()
        self.filter_enemies()

        return random.choice(self.directions)

    def filter_self(self):
        for x, y in self.coords:

            if self.head_x + 1 == x and self.head_y == y:
                self.directions.remove(self.RIGHT)

            if self.head_x - 1 == x and self.head_y == y:
                self.directions.remove(self.LEFT)

            if self.head_x == x:

                if self.head_y + 1 == y:
                    self.directions.remove(self.DOWN)

                if self.head_y - 1 == y:
                    self.directions.remove(self.UP)


    def filter_walls(self):
        pass

    def filter_enemies(self):

        if self.head_x == 0:
            self.directions.remove(self.LEFT)

        if self.head_x == self.board.width - 1:
            self.directions.remove(self.RIGHT)

        if self.head_y == 0:
            self.directions.remove(self.UP)

        if self.head_y == self.board.height - 1:
            self.directions.remove(self.DOWN)

    def __str__(self):
        return '<Snake: %s>' % self.name


class Tile(object):

    state = None
    x = None
    y = None

    STATE_CHOICES = ('head', 'body', 'food', 'empty')

    def __init__(self, state, x, y):

        if state not in self.STATE_CHOICES:
            raise Exception("WTF is this state: %s" % state)

        self.state = state
        self.x = x
        self.y = y


class Board(object):

    tile_array = None
    food = None

    def __init__(self, board):
        self.tile_array = board
        self.food = []

        for x, row in enumerate(board):
            for y, tile in enumerate(row):
                if tile['state'] == 'food':
                    self.food.append((x, y))


    @property
    def height(self):
        return len(self.tile_array[0])

    @property
    def width(self):
        return len(self.tile_array)