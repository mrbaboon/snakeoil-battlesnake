import bottle
import json
import logging

from app.models import Snake, Board, Tile, Game

SNAKE_NAME = 'snakeoil2'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': SNAKE_NAME,
        'color': '#00ff00',
        'head_url': 'http://battlesnake-python.herokuapp.com',
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    name = data['game_id']
    turn = data['turn']
    snakes = data['snakes']
    board_data = data['board']

    game = Game(name, turn, snakes, board_data)
    board = Board(board_data)

    logger.info("Board: %s x %s" % (board.width, board.height))
    logger.info("Food: %s" % board.food)

    our_snake = None
    enemy_snakes = []

    for snake_data in snakes:

        logger.info(snake_data)

        if snake_data.get('name') == SNAKE_NAME:
            our_snake_data = snake_data

        else:

            enemy_snakes.append(
                Snake(name=snake_data.get('name'),
                      state=snake_data.get('state'),
                      coords=snake_data.get('coords'),
                      turn=game.turn,
                      last_eaten=snake_data.get('last_eaten'))
            )

    our_snake = Snake(name=our_snake_data.get('name'),
                      state=our_snake_data.get('state'),
                      coords=our_snake_data.get('coords'),
                      turn=game.turn,
                      last_eaten=our_snake_data.get('last_eaten'),
                      board=board,
                      enemies=enemy_snakes)

    direction = our_snake.move()


    return json.dumps({
        'move': direction,
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
