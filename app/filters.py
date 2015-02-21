
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


class FoodFilter(Filter):
    closest_food = None
    closest_food_distance = None

    def apply(self, snake, actions):
        self.actions = actions
        logger.info("Initial actions %s" % self.actions)
        from app.models import Snake

        for food in snake.board.food:
            food_distance = food.distance(snake.head_x, snake.head_y)

            if not self.closest_food:

                self.closest_food = food
                self.closest_food_distance = food_distance

            else:

                if food_distance < self.closest_food_distance:
                    self.closest_food = food
                    self.closest_food_distance = food_distance

        logger.info("Closest food: %s, %s" % (self.closest_food.x, self.closest_food.y))
        logger.info("Snake: %s, %s" % (snake.head_x, snake.head_y))

        if self.closest_food.x > snake.head_x:
            logger.info("Removing action - left")
            self.remove_action(Snake.LEFT)

        elif self.closest_food.x < snake.head_x:
            logger.info("Removing action - right")
            self.remove_action(Snake.RIGHT)

        else:
            logger.info("Removing action same row")
            self.remove_action(Snake.LEFT)
            self.remove_action(Snake.RIGHT)

        if self.closest_food.y > snake.head_y:
            logger.info("Removing action - up")
            self.remove_action(Snake.UP)

        elif self.closest_food.y < snake.head_y:
            logger.info("Removing action - down")
            self.remove_action(Snake.DOWN)

        else:
            logger.info("Removing action - same column")
            self.remove_action(Snake.UP)
            self.remove_action(Snake.DOWN)

        logger.info("Food moves: %s" % self.actions)

        return self.actions