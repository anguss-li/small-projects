from random import randint
from time import sleep
from tkinter.constants import NO, N
from turtle import Turtle, TurtleScreen, _Screen


class GamePart(Turtle):
    def __init__(self, shape, color):
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
        Dummy object used by Board. When "eaten" by a snake, teleports to a
        random location within x_limit and y_limit of game board.
        '''
        super().__init__(shape="circle", color="red")
        self.shapesize(0.50, 0.50)
        self.goto(0, 0)

    def teleport(self, x_limit, y_limit) -> None:
        '''
        Randomly moves self to location on game board.
        '''
        x_pos = randint(-(x_limit), x_limit)
        y_pos = randint(-(y_limit), y_limit)
        self.goto(x_pos, y_pos)


class ScoreCounter(GamePart):
    def __init__(self, font, x_pos, y_pos):
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
        Returns value of high_score according to 'high_score.txt'.
        '''
        high_score_record = open('high_score.txt', 'r')
        return int(high_score_record.read())

    def set_high_score(self, high_score) -> None:
        '''
        Sets self.high_score to input.
        '''
        high_score_record = open('high_score.txt', 'w')
        high_score_record.write(str(high_score))

    def change_score(self, score_change) -> int:
        '''
        Returns new value of score, as well as a new high score if new score is 
        higher than the previous high score.

        score_change: number by which self.score will be modified
        '''
        high_score = self.get_high_score()
        self.score += score_change
        if self.score > high_score:
            self.set_high_score(self.score)

    def write_score(self) -> None:
        '''
        Writes in text on board values of score and high_score.

        score: score of current game
        high_score: highest value of score over all previous games
        '''
        score, high_score = self.score, self.get_high_score()
        self.clear()
        self.write("Score: {} High Score: {}".format(score, high_score),
                   align="center", font=(self.font, 22, "normal"))


class Board(_Screen):
    def __init__(self, title, color, length, font):
        '''
        Implements game window as well as elements not controlled by the user.

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
        self.food = Food()
        self.score_counter = ScoreCounter(font, 0, (length / 2) - 40)


class SnakePart(GamePart):
    def __init__(self, x_pos, y_pos):
        '''
        Dummy object used by snake.

        x_pos, y_pos: x and y coordinates respectively.
        '''
        super().__init__(shape="square", color="black")
        self.goto(x_pos, y_pos)
        self.direction = "stop"


class Snake(list):
    def __init__(self):
        '''
        List of SnakePart objects that can be controlled by user. Main 
        interactive element of the game.
        '''
        super().__init__()
        self.append(SnakePart(0, 100))
        self.direction = "stop"

    def add_part(self, x_pos, y_pos) -> None:
        '''
        Appends a new SnakePart at x_pos and y_pos.

        x_pos, y_pos: x and y coordinates of the Food object eaten by snake
        '''
        self.insert(0, SnakePart(x_pos, y_pos))

    def delete_part(self, part: SnakePart) -> None:
        '''
        Hides part before deleting it from structure.

        part: part in snake to be deleted
        '''
        part.hideturtle()
        self.remove(part)

    def reset(self) -> None:
        '''
        Return self to default configuration.
        '''
        snake_ref = self.copy()
        for part in snake_ref:
            if snake_ref.index(part) != 0:
                self.delete_part(part)
        self[0].goto(0, 100)
        self.direction = "stop"

    def move(self) -> None:
        '''
        Sets movement direction of self according to self.direction.
        '''
        x_pos = self[0].xcor()  # x coordinate of the turtle
        y_pos = self[0].ycor()  # y coordinate of the turtle
        if self.direction == "up":
            y_pos += 20
        elif self.direction == "down":
            y_pos -= 20
        elif self.direction == "right":
            x_pos += 20
        elif self.direction == "left":
            x_pos -= 20
        self.add_part(x_pos, y_pos)
        self.delete_part(self[-1])

    def go_up(self) -> None:
        '''
        Sets direction of the head to "up" if not currently "down".
        '''
        if self.direction != "down":
            self.direction = "up"

    def go_down(self) -> None:
        '''
        Sets direction of the head to "down" if not currently "up".
        '''
        if self.direction != "up":
            self.direction = "down"

    def go_right(self) -> None:
        '''
        Sets direction of the head to "right" if not currently "left".
        '''
        if self.direction != "left":
            self.direction = "right"

    def go_left(self) -> None:
        '''
        Sets direction of the head to "left" if not currently "right".
        '''
        if self.direction != "right":
            self.direction = "left"


class Game(object):
    def __init__(self, title: str, color: str, length: int, font: str, delay: float):
        '''
        Used to implement main game functions, such as main loop and game over
        conditions.

        title: text to be displayed as window title
        color: valid turtle color to be used as background
        length: how long the board should be in pixels
        font: valid font in turtle to be used for writing
        delay: time step in between actions in game
        '''
        self.board = Board(title, color, length, font)
        self.snake = Snake()
        self.delay = delay
        self.score = 0

    def game_over(self) -> None:
        '''
        Resets snake, score and food.
        '''
        sleep(1)
        self.snake.reset()
        score_counter = self.board.score_counter
        food = self.board.food
        score_counter.change_score(-(score_counter.score))
        food.goto(0, 0)

    def run(self) -> None:
        '''
        Sets up main game loop.
        '''
        board = self.board
        snake = self.snake
        board.listen()
        board.onkey(snake.go_up, "w")
        board.onkey(snake.go_down, "s")
        board.onkey(snake.go_right, "d")
        board.onkey(snake.go_left, "a")
        x_limit = (board.window_width() / 2) - 10
        y_limit = (board.window_height() / 2) - 10
        score_counter = board.score_counter
        food = board.food
        while True:
            board.update()
            score_counter.write_score()
            snake.move()
            # print(snake)
            sleep(self.delay)
            head = snake[0]
            if head.distance(food) < 15:
                # Increase score, check for high score increase
                score_counter.change_score(10)
                # Add a segment
                food_x, food_y = food.xcor(), food.ycor()
                snake.add_part(food_x, food_y)
                # Move food
                food.teleport(x_limit - 20, y_limit - 20)
            for part in range(3, len(snake)):
                try:
                    if snake[part].distance(head) < 25:
                        self.game_over()
                except IndexError:
                    pass
            head_x, head_y = head.xcor(), head.ycor()
            has_snake_collided = (head_x > x_limit or head_x < -x_limit or
                                  head_y > y_limit or head_y < -y_limit)
            if has_snake_collided:
                self.game_over()


if __name__ == '__main__':
    game = Game("Angus' Snake Game", "MintCream", 800, "Courier", 0.125)
    game.run()
