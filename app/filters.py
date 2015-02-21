

class Filter(object):

    actions = []
    priority = 0

    def __init__(self, priority=0):
        from models import Snake
        self.priority = priority

    def apply(self, snake, actions):
        raise NotImplementedError('implement this in the child object!')


class WallFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions
        if snake.head_x == 0:
            try:
                self.actions.remove(Snake.LEFT)
            except Exception:
                pass

        if snake.head_x == snake.board.width - 1:
            try:
                self.actions.remove(Snake.RIGHT)
            except Exception:
                pass

        if snake.head_y == 0:
            try:
                self.actions.remove(Snake.UP)
            except Exception:
                pass

        if snake.head_y == snake.board.height - 1:
            try:
                self.actions.remove(Snake.DOWN)
            except Exception:
                pass


class SelfFilter(Filter):

    def apply(self, snake, actions):
        from models import Snake

        self.actions = actions
        for x, y in snake.coords:

            if snake.head_x + 1 == x and snake.head_y == y:
                try:
                    self.actions.remove(Snake.RIGHT)
                except Exception:
                    pass

            if snake.head_x - 1 == x and snake.head_y == y:
                try:
                    self.actions.remove(Snake.LEFT)
                except Exception:
                    pass

            if snake.head_x == x:

                if snake.head_y + 1 == y:
                    try:
                        self.actions.remove(Snake.DOWN)
                    except Exception:
                        pass

                if snake.head_y - 1 == y:
                    try:
                        self.actions.remove(Snake.UP)
                    except Exception:
                        pass









