from random import randint
from time import sleep
from turtle import Turtle, TurtleScreen, _Screen


class GamePart(Turtle):
    def __init__(self, shape, color):
        '''
        Used for interactive objects in game. Inherited by classes SnakePart, 
        ScoreCounter and Food.
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

    def teleport(self, x_limit, y_limit):
        '''
        x_limit, y_limit: integers, maximum distance food can travel in x and y 
        axes respectively.
        Returns: None, randomly moving Food object to location on game board.
        '''
        x_pos = randint(-(x_limit), x_limit)
        y_pos = randint(-(y_limit), y_limit)
        self.goto(x_pos, y_pos)


class ScoreCounter(GamePart):
    def __init__(self, font, x_pos, y_pos):
        '''
        Dummy object used by Board. Used to write Board.score and 
        Board.high_score on screen.

        font: string, valid font in turtle.
        '''
        super().__init__(shape="square", color="black")
        self.font = font
        self.hideturtle()
        self.goto(x_pos, y_pos)
        self.score = 0

    def get_high_score(self):
        '''
        Returns: integer, value of high_score according to 'high_score.txt'.
        '''
        high_score_record = open('high_score.txt', 'r')
        return int(float(high_score_record.read()))

    def set_high_score(self, high_score):
        '''
        high_score: integer, new value of self.high_score
        Returns: None, overwriting self.high_score with high_score.
        '''
        high_score_record = open('high_score.txt', 'w')
        high_score_record.write(str(high_score))

    def change_score(self, score_change):
        '''
        score_change: integer, number by which self.score will be modified
        Returns: new value of score, as well as a new high score if new score is 
        higher than the previous high score
        '''
        high_score = self.get_high_score()
        self.score += score_change
        if self.score > high_score:
            self.set_high_score(self.score)

    def write_score(self):
        '''
        score: integer, score of current game
        high_score: highest value of score over all previous games
        Returns: None, writing in text on board values of score and high_score
        '''
        score, high_score = self.score, self.get_high_score()
        self.clear()
        self.write("Score: {} High Score: {}".format(score, high_score),
                   align="center", font=(self.font, 22, "normal"))


class SnakePart(GamePart):
    def __init__(self, x_pos, y_pos):
        '''
        Dummy object used by snake.

        x_pos, y_pos: integers, x and y coordinates respectively.
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
        self.insert(0, SnakePart(0, 100))
        self.direction = "stop"

    def add_part(self, x_pos, y_pos):
        '''
        x_pos, y_pos: x and y coordinates of the Food object eaten by snake
        Returns: None, appending to self a new SnakePart at x_pos and y_pos
        '''
        self.insert(0, SnakePart(x_pos, y_pos))

    def delete_part(self, index):
        '''
        index: integer, index of part in snake to be deleted
        Returns: None, hiding self[index] before deleting it from structure
        '''
        self[index].hideturtle()
        self.pop(index)

    def reset(self):
        '''
        Returns: None, deleting every part of the snake besides self[0], 
        resetting position and setting direction to "stop".
        '''
        for part in range(1, len(self)):
            try:
                self.delete_part(part)
            except IndexError:
                pass
        self[0].goto(0, 100)
        self.direction = "stop"

    def move(self):
        '''
        Returns: None, setting movement direction of the snake according to
        self.direction
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
        self.delete_part(-1)

    def go_up(self):
        '''
        Returns: None, setting direction of the head to "up" if not currently 
        "down"
        '''
        if self.direction != "down":
            self.direction = "up"

    def go_down(self):
        '''
        Returns: None, setting direction of the head to "down" if not currently 
        "up"
        '''
        if self.direction != "up":
            self.direction = "down"

    def go_right(self):
        '''
        Returns: None, setting direction of the head to "right" if not currently 
        "left"
        '''
        if self.direction != "left":
            self.direction = "right"

    def go_left(self):
        '''
        Returns: None, setting direction of the head to "left" if not currently 
        "right"
        '''
        if self.direction != "right":
            self.direction = "left"


class Board(_Screen):
    def __init__(self, title, color, width, height, font):
        '''
        Implements game window as well as elements not controlled by the user.

        title: string, text to be displayed as window title
        color: string, valid turtle color to be used as background
        width, height: integers, width and height in pixels respectively
        font: string, valid font in turtle to be used for writing
        '''
        super().__init__()
        TurtleScreen.__init__(self, Board._canvas)
        if Turtle._screen is None:
            Turtle._screen = self
        self.title(title)
        self.bgcolor(color)
        self.setup(width=width, height=height)
        self.tracer(0)
        self.food = Food()
        self.score_counter = ScoreCounter(font, 0, (height / 2) - 40)


class Game(object):
    def __init__(self, title, color, width, height, font):
        '''
        Used to implement main game functions, such as main loop and game over
        conditions.

        title: string, text to be displayed as window title
        color: string, valid turtle color to be used as background
        width, height: integers, width and height in pixels respectively
        font: string, valid font in turtle to be used for writing
        '''
        self.board = Board(title, color, width, height, font)
        self.snake = Snake()
        self.score = 0

    def game_over(self):
        '''
        Returns: None, resetting snake, score and food.
        '''
        sleep(1)
        self.snake.reset()
        self.board.score_counter.change_score(-(self.board.score))
        self.board.food.goto(0, 0)

    def run(self, delay):
        '''
        Returns: None, setting up main game loop.
        '''
        board = self.board
        snake = self.snake
        x_limit = (board.window_width() / 2) - 10
        y_limit = (board.window_height() / 2) - 10
        board.listen()
        board.onkey(snake.go_up, "w")
        board.onkey(snake.go_down, "s")
        board.onkey(snake.go_right, "d")
        board.onkey(snake.go_left, "a")
        score_counter = board.score_counter
        food = board.food
        while True:
            board.update()
            score_counter.write_score()
            snake.move()
            sleep(delay)
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


game = Game("Angus' Snake Game", "MintCream", 800, 800, "Courier")

game.run(0.125)
