from functools import partial
from random import randint
from time import sleep
from turtle import Turtle, TurtleScreen, _Screen


class GamePart(Turtle):
    def __init__(self, shape: str, color: str):
        '''
        Used for interactive objects in game. Inherited by classes SnakePart, 
        ScoreCounter and Food.

        shape: valid polygon shape in turtle.
        color: valid color name in turtle. 
        '''
        super().__init__()
        self.speed(0)
        self.shape(shape)
        self.color(color)
        self.penup()


class Food(GamePart):
    def __init__(self):
        '''
        When "eaten" by a snake, teleports to a random location within x_limit 
        and y_limit of game board.
        '''
        super().__init__(shape="circle", color="red")
        self.shapesize(0.50, 0.50)
        self.goto(0, 0)

    def teleport(self, x_limit: int, y_limit: int) -> None:
        '''
        Randomly move self to location on game board.
        '''
        self.goto(randint(-(x_limit), x_limit), randint(-(y_limit), y_limit))


class ScoreCounter(GamePart):
    def __init__(self, font: str, x_pos: int, y_pos: int):
        '''
        Dummy object used to write Board.score and Board.high_score on screen.

        font: valid font in turtle.
        '''
        super().__init__(shape="square", color="black")
        self.font = font
        self.hideturtle()
        self.goto(x_pos, y_pos)
        self.score = 0

    def get_high_score(self) -> int:
        '''
        Return value of high_score according to 'high_score.txt'.
        '''
        high_score_record = open('high_score.txt', 'r')
        return int(high_score_record.read())

    def set_high_score(self, high_score: int) -> None:
        '''
        Set self.high_score to input.
        '''
        high_score_record = open('high_score.txt', 'w')
        high_score_record.write(str(high_score))

    def write_score(self) -> None:
        '''
        Write in text values of score and high_score.

        score: score of current game
        high_score: highest value of score over all previous games
        '''
        score, high_score = self.score, self.get_high_score()
        self.clear()
        self.write(f"Score: {score} High Score: {high_score}",
                   align="center", font=(self.font, 22, "normal"))

    def change_scores(self, score_change: int) -> None:
        '''
        Update score, as well as the high score if the new score is higher.

        score_change: number by which self.score will be modified
        '''
        high_score = self.get_high_score()
        self.score += score_change
        if self.score > high_score:
            self.set_high_score(self.score)
        self.write_score()


class Board(_Screen):
    def __init__(self, title: str, color: str, length: int, font: str):
        '''
        Implement game window as well as elements not controlled by the user.

        title: text to be displayed as window title
        color: valid turtle color to be used as background
        length: length of board in pixels
        font: valid font in turtle to be used for writing
        '''
        super().__init__()
        TurtleScreen.__init__(self, Board._canvas)
        Turtle._screen = self
        self.title(title)
        self.bgcolor(color)
        self.setup(width=length, height=length)
        self.tracer(0)


class SnakePart(GamePart):
    def __init__(self, x_pos: int, y_pos: int):
        '''
        Dummy object used by snake.

        x_pos, y_pos: x and y coordinates respectively.
        '''
        super().__init__(shape="square", color="black")
        self.goto(x_pos, y_pos)


class Snake(list):
    def __init__(self):
        '''
        Set of SnakePart objects that can be controlled by user. Main 
        interactive element of the game.
        '''
        super().__init__()
        self.head = SnakePart(0, 100)
        self._direction = "stop"

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, direction: str) -> None:
        is_legal = {"up": self.direction != "down",
                    "down": self.direction != "up",
                    "left": self.direction != "right",
                    "right": self.direction != "left",
                    "stop": True}
        if is_legal[direction]:
            self._direction = direction

    def move(self, step: int) -> None:
        '''
        Set movement direction of self according to self.direction.

        step: number of pixels to move
        '''
        head_x, head_y = self.head.xcor(), self.head.ycor()

        for part in range(len(self)-1, 0, -1):
            x = self[part-1].xcor()
            y = self[part-1].ycor()
            self[part].goto(x, y)
        if len(self) > 0:
            self[0].goto(head_x, head_y)

        if self.direction == "up":
            head_y += step
        elif self.direction == "down":
            head_y -= step
        elif self.direction == "right":
            head_x += step
        elif self.direction == "left":
            head_x -= step
        self.head.goto(head_x, head_y)

    def reset(self) -> None:
        '''
        Return self to default configuration.
        '''
        for part in self:
            part.hideturtle()
        self.clear()
        self.head.goto(0, 100)
        self.direction = "stop"


class SnakeGame(object):
    def __init__(self, title: str, color: str, length: int, font: str, delay: float):
        '''
        Implement main game functions and gameplay loop.

        title: text to be displayed as window title
        color: valid turtle color to be used as background
        length: how long the board should be in pixels
        font: valid font in turtle to be used for writing
        delay: time step in between actions in game
        '''
        self.length = length
        self.delay = delay
        self.score = 0
        self.board = Board(title, color, length, font)
        self.snake = Snake()
        self.food = Food()
        self.score_counter = ScoreCounter(font, 0, (length/2)-40)
        self.step = self.length // 40
        self.limit = self.length // 2

    def initialize(self) -> None:
        '''Create main game components'''
        board = self.board
        board.listen()
        board.onkey(partial(setattr, self.snake, "direction", "up"), "w")
        board.onkey(partial(setattr, self.snake, "direction", "down"), "s")
        board.onkey(partial(setattr, self.snake, "direction", "right"), "d")
        board.onkey(partial(setattr, self.snake, "direction", "left"), "a")
        self.score_counter.write_score()

    def play(self) -> None:
        '''Start game loop.'''

        def win_points() -> None:
            '''Account for food being eaten.'''
            self.score_counter.change_scores(10)
            temp_position = self.limit+self.step*2
            self.snake.append(SnakePart(temp_position, temp_position))
            self.food.teleport(self.limit, self.limit)

        def is_pos_legal() -> None:
            '''Check that snake is in bounds and is not eating itself'''
            snake, head = self.snake, self.snake.head
            step, limit = self.step, self.limit
            is_eaten = any(part.distance(head) < step for part in snake)
            is_in_bounds = all(-limit < coord < limit for coord in head.pos())
            return not is_eaten and is_in_bounds

        def game_over() -> None:
            '''Reset snake, score and food.'''
            sleep(1)
            self.snake.reset()
            self.score_counter.change_scores(-self.score_counter.score)
            self.food.goto(0, 0)

        while True:
            self.board.update()
            self.snake.move(self.step)
            if self.snake.head.distance(self.food) < self.step:
                win_points()
            if not is_pos_legal():
                game_over()
            sleep(self.delay)


if __name__ == '__main__':
    game = SnakeGame("Angus' Snake Game", "MintCream", 800, "Courier", 0.125)
    game.initialize()
    game.play()
