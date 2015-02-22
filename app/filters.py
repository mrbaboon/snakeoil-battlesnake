
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class Filter(object):

    actions = None
    priority = 0

    def __init__(self, priority=0):
        from models import Snake
        self.actions = []
        self.priority = priority

    def apply(self, snake, actions):
        raise NotImplementedError('implement this in the child object!')

    def remove_action(self, action):
        from models import Snake

        try:
            self.actions.remove(action)
        except Exception:
            pass


class WallFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions
        if snake.head_x == 0:
            self.remove_action(Snake.LEFT)

        if snake.head_x == snake.board.width - 1:
            self.remove_action(Snake.RIGHT)

        if snake.head_y == 0:
            self.remove_action(Snake.UP)

        if snake.head_y == snake.board.height - 1:
            self.remove_action(Snake.DOWN)

        return self.actions


class SelfFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions
        for x, y in snake.coords:

            if snake.head_y == y:
                if snake.head_x + 1 == x:
                    self.remove_action(Snake.RIGHT)

                if snake.head_x - 1 == x:
                    self.remove_action(Snake.LEFT)

            if snake.head_x == x:

                if snake.head_y + 1 == y:
                    self.remove_action(Snake.DOWN)

                if snake.head_y - 1 == y:
                    self.remove_action(Snake.UP)

        return self.actions


class EnemyFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions

        snakes = snake.enemies

        for this_snake in snakes:

            # skip if this is me...
            if this_snake.name == snake.name:
                continue

            for x, y in this_snake.coords:
                if snake.head_y == y:
                    if snake.head_x + 1 == x:
                        self.remove_action(Snake.RIGHT)

                    if snake.head_x - 1 == x:
                        self.remove_action(Snake.LEFT)

                if snake.head_x == x:

                    if snake.head_y + 1 == y:
                        self.remove_action(Snake.DOWN)

                    if snake.head_y - 1 == y:
                        self.remove_action(Snake.UP)

        return self.actions


class FoodFilter(Filter):
    closest_food = None
    closest_food_distance = None

    def apply(self, snake, actions):
        self.actions = actions
        from app.models import Snake

        for food in snake.board.food:
            food_distance = food.distance(snake.head_x, snake.head_y)

            if not self.closest_food:

                self.closest_food = food
                self.closest_food_distance = food_distance

            else:

                if food_distance < self.closest_food_distance:

                    for enemy in snake.enemies:

                        # If no other snake is closer to this food, get it!
                        if food.distance(enemy.head_x, enemy.head_y) < self.closest_food_distance:
                            self.closest_food = food
                            self.closest_food_distance = food_distance

        if self.closest_food.x > snake.head_x:

            self.remove_action(Snake.LEFT)

        elif self.closest_food.x < snake.head_x:

            self.remove_action(Snake.RIGHT)

        else:

            self.remove_action(Snake.LEFT)
            self.remove_action(Snake.RIGHT)

        if self.closest_food.y > snake.head_y:

            self.remove_action(Snake.UP)

        elif self.closest_food.y < snake.head_y:

            self.remove_action(Snake.DOWN)

        else:

            self.remove_action(Snake.UP)
            self.remove_action(Snake.DOWN)

        logger.info("Food moves: %s" % self.actions)

        return self.actions


class HeadOnLookAheadFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions
        snakes = snake.enemies

        for this_snake in snakes:

            # skip if this is me...
            if this_snake.name == snake.name:
                continue

            # get the lengths of us and the current enemy
            this_snake_len = len(this_snake.coords)
            snake_len = len(snake.coords)

            # Only attack if we are bigger
            i_am_bigger = snake_len > this_snake_len

            if i_am_bigger:
                # lock x, deal with y +-1
                if this_snake.head_x == snake.head_x:
                    if this_snake.head_y == snake.head_y-1:
                        self.actions = [Snake.UP]
                    if this_snake.head_y == snake.head_y+1:
                        self.actions = [Snake.DOWN]

                # lock y, deal with x +-1
                if this_snake.head_y == snake.head_y:
                    if this_snake.head_x == snake.head_x-1:
                        self.actions = [Snake.LEFT]
                    if this_snake.head_x == snake.head_x+1:
                        self.actions = [Snake.RIGHT]

                # deal with top diagonals +-1
                if this_snake.head_y == snake.head_y-1:
                    if this_snake.head_x == snake.head_x-1:
                        if len(self.actions) > 1:
                            self.remove_action(Snake.DOWN)
                        if len(self.actions) > 1:
                            self.remove_action(Snake.RIGHT)

                    if this_snake.head_x == snake.head_x+1:
                        if len(self.actions) > 1:
                            self.remove_action(Snake.DOWN)
                        if len(self.actions) > 1:
                            self.remove_action(Snake.LEFT)

                # deal with bottom diagonals +-1
                if this_snake.head_y == snake.head_y+1:
                    if this_snake.head_x == snake.head_x-1:
                        if len(self.actions) > 1:
                            self.remove_action(Snake.UP)
                        if len(self.actions) > 1:
                            self.remove_action(Snake.RIGHT)

                    if this_snake.head_x == snake.head_x+1:
                        if len(self.actions) > 1:
                            self.remove_action(Snake.UP)
                        if len(self.actions) > 1:
                            self.remove_action(Snake.LEFT)

            # deal with top +-2 spaces
            if this_snake.head_y == snake.head_y-2:

                if this_snake.head_x == snake.head_x:
                    if i_am_bigger and Snake.UP in self.actions:
                        self.actions = [Snake.UP]

                if this_snake.head_x < snake.head_x:
                    if i_am_bigger:
                        if Snake.UP in self.actions:
                            self.actions = [Snake.UP]
                        elif Snake.LEFT in self.actions:
                            self.actions = [Snake.LEFT]
                    else:
                        self.remove_action(Snake.UP)
                        self.remove_action(Snake.LEFT)

                if this_snake.head_x > snake.head_x:
                    if i_am_bigger:
                        if Snake.UP in self.actions:
                            self.actions = [Snake.UP]
                        elif Snake.RIGHT in self.actions:
                            self.actions = [Snake.RIGHT]
                    else:
                        self.remove_action(Snake.UP)
                        self.remove_action(Snake.RIGHT)

            # deal with the outer top +1 space
            if this_snake.head_y == snake.head_y-1:
                if this_snake.head_x == snake.head_x-2:
                    if i_am_bigger:
                        if Snake.UP in self.actions:
                            self.actions = [Snake.UP]
                        elif Snake.LEFT in self.actions:
                            self.actions = [Snake.LEFT]
                    else:
                        self.remove_action(Snake.UP)
                        self.remove_action(Snake.LEFT)
                if this_snake.head_x == snake.head_x+2:
                    if i_am_bigger:
                        if Snake.UP in self.actions:
                            self.actions = [Snake.UP]
                        elif Snake.RIGHT in self.actions:
                            self.actions = [Snake.RIGHT]
                    else:
                        self.remove_action(Snake.UP)
                        self.remove_action(Snake.RIGHT)

            # deal with the outer middle spaces (x+-2)
            if this_snake.head_y == snake.head_y:
                if this_snake.head_x == snake.head_x-2:
                    if i_am_bigger:
                        if Snake.LEFT in self.actions:
                            self.actions = [Snake.LEFT]
                    else:
                        self.remove_action(Snake.LEFT)

                if this_snake.head_x == snake.head_x+2:
                    if i_am_bigger:
                        if Snake.RIGHT in self.actions:
                            self.actions = [Snake.RIGHT]
                    else:
                        self.remove_action(Snake.RIGHT)

            # deal with the bottom outer y+1
            if this_snake.head_y == snake.head_y+1:
                if this_snake.head_x == snake.head_x-2:
                    if i_am_bigger:
                        if Snake.DOWN in self.actions:
                            self.actions = [Snake.DOWN]
                        elif Snake.LEFT in self.actions:
                            self.actions = [Snake.LEFT]
                    else:
                        self.remove_action(Snake.DOWN)
                        self.remove_action(Snake.LEFT)

                if this_snake.head_x == snake.head_x+2:
                    if i_am_bigger:
                        if Snake.DOWN in self.actions:
                            self.actions = [Snake.DOWN]
                        elif Snake.RIGHT in self.actions:
                            self.actions = [Snake.RIGHT]
                    else:
                        self.remove_action(Snake.DOWN)
                        self.remove_action(Snake.RIGHT)

            # deal with the bottom y+2
            if this_snake.head_y == snake.head_y+2:
                if this_snake.head_x < snake.head_x:
                    if i_am_bigger:
                        if Snake.DOWN in self.actions:
                            self.actions = [Snake.DOWN]
                        elif Snake.LEFT in self.actions:
                            self.actions = [Snake.LEFT]
                    else:
                        self.remove_action(Snake.DOWN)
                        self.remove_action(Snake.LEFT)

                if this_snake.head_x == snake.head_x:
                    if i_am_bigger:
                        if Snake.DOWN in self.actions:
                            self.actions = [Snake.DOWN]
                    else:
                        self.remove_action(Snake.DOWN)

                if this_snake.head_x > snake.head_x:
                    if i_am_bigger:
                        if Snake.DOWN in self.actions:
                            self.actions = [Snake.DOWN]
                        elif Snake.RIGHT in self.actions:
                            self.actions = [Snake.RIGHT]
                    else:
                        self.remove_action(Snake.DOWN)
                        self.remove_action(Snake.RIGHT)

        return self.actions
