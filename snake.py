import random
import time
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
        del self[index]

    def move(self):
        '''
        Returns: None, setting movement direction of the snake according to
        self.direction
        '''
        y_pos = self[0].ycor()  # y coordinate of the turtle
        x_pos = self[0].xcor()  # x coordinate of the turtle
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


class Food(GamePart):
    def __init__(self):
        '''
        Dummy object used by Board. When "eaten" by a snake, teleports to a
        random location within X_LIMIT and Y_LIMIT of game board.
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
        x_pos = random.randint(-(x_limit), x_limit)
        y_pos = random.randint(-(y_limit), y_limit)
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

    def write_score(self, score, high_score):
        '''
        score: integer, score of current game
        high_score: highest value of score over all previous games
        Returns: None, writing in text on board values of score and high_score
        '''
        self.clear()
        self.write("Score: {} High Score: {}".format(score, high_score),
                   align="center", font=(self.font, 22, "normal"))


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
        self.score = 0
        self.high_score = 0
        self.score_counter = ScoreCounter(font, 0, (height / 2) - 40)

    def change_score(self, score_change):
        '''
        score_change: integer, number by which self.score will be modified
        Returns: new value of score, as well as a new high score if new score is 
        higher than the previous high score
        '''
        self.score += score_change
        if self.score > self.high_score:
            self.high_score = self.score


DELAY = 0.125

# Window Setup
board = Board("Angus' Snake Game", "MintCream", 800, 800, "Courier")
X_LIMIT = (board.window_width() / 2) - 10
Y_LIMIT = (board.window_height() / 2) - 10
food = board.food
score_counter = board.score_counter

# Snake Setup
snake = Snake()

# Keyboard Bindings
board.listen()
board.onkey(snake.go_up, "w")
board.onkey(snake.go_down, "s")
board.onkey(snake.go_right, "d")
board.onkey(snake.go_left, "a")


def game_over():
    '''
    Returns: None, resetting snake, score and food.
    '''
    time.sleep(1)
    snake.reset()
    board.change_score(-(board.score))
    food.goto(0, 0)


def main():
    '''
    Returns: None, setting up main game loop
    '''
    while True:
        board.update()
        score_counter.write_score(board.score, board.high_score)
        snake.move()
        time.sleep(DELAY)
        head = snake[0]
        if head.distance(food) < 15:
            # Increase score, check for high score increase
            board.change_score(10)
            # Add a segment
            food_x, food_y = food.xcor(), food.ycor()
            snake.add_part(food_x, food_y)
            # Move food
            food.teleport(X_LIMIT - 20, Y_LIMIT - 20)
        for part in range(3, len(snake)):
            if snake[part].distance(head) < 25:
                game_over()
        head_x, head_y = head.xcor(), head.ycor()
        has_snake_collided = (head_x > X_LIMIT or head_x < -X_LIMIT or
                              head_y > Y_LIMIT or head_y < -Y_LIMIT)
        if has_snake_collided:
            game_over()


main()
