import random
import bottle
import json
import logging

from app.models import Snake, Board, Tile, Game

SNAKE_NAME = 'snakeoil'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


TAUNTS = [
    "We're no strangers to love",
    "You know the rules and so do I",
    "A full commitment's what I'm thinking of",
    "You wouldn't get this from any other guy",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "We've known each other for so long",
    "Your heart's been aching, but",
    "You're too shy to say it",
    "Inside, we both know what's been going on",
    "We know the game and we're gonna play it",
    "And if you ask me how I'm feeling",
    "Don't tell me you're too blind to see",
    "Never gonna give, never gonna give",
    "Never gonna give, never gonna give",
    "We've known each other for so long",
    "Your heart's been aching, but",
    "You're too shy to say it",
    "Inside, we both know what's been going on",
    "We know the game and we're gonna play it",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
]

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
        'color': '#ff69b4',
        'head_url': 'http://www.zoom-comics.com/wp-content/uploads/sites/36/2011/12/pinky-pie-pony.jpg',
        'taunt': random.choice(TAUNTS)
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
        'taunt': random.choice(TAUNTS)
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
