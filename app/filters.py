

class Filter(object):

    actions = []
    priority = 0

    def __init__(self, priority=0):
        from models import Snake
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


class FoodFilter(Filter):

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


# class FoodFilter(Filter):
#
#     def apply(self, snake, actions):
#         closest_food = None
#         for food in





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




