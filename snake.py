import random
import time
import turtle

delay = 0.1

# Window Setup
window = turtle.Screen()
window.title("Angus' Snake Game")
window.bgcolor("MintCream")
window.setup(width=800, height=800)
window.tracer(0)

# Snake Head Setup
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 100)
head.direction = "stop"


def move():
    '''
    Returns: None, setting movement direction of the snake according to
    head.direction
    '''
    if head.direction == "up":
        y = head.ycor()  # y coordinate of the turtle
        head.sety(y + 20)
    elif head.direction == "down":
        y = head.ycor()  # y coordinate of the turtle
        head.sety(y - 20)
    elif head.direction == "right":
        x = head.xcor()  # y coordinate of the turtle
        head.setx(x + 20)
    elif head.direction == "left":
        x = head.xcor()  # y coordinate of the turtle
        head.setx(x - 20)


# The snake cannot immediately go from down to up or left to right, hence
# if statements
def go_up():
    '''
    Returns: None, setting head direction to "up" if it is not "down"
    '''
    if head.direction != "down":
        head.direction = "up"


def go_down():
    '''
    Returns: None, setting head direction to "down" if it is not "up"
    '''
    if head.direction != "up":
        head.direction = "down"


def go_left():
    '''
    Returns: None, setting head direction to "left" if it is not "right"
    '''
    if head.direction != "right":
        head.direction = "left"


def go_right():
    '''
    Returns: None, setting head direction to "right" if it is not "left"
    '''
    if head.direction != "left":
        head.direction = "right"


# Keyboard Bindings
window.listen()
window.onkey(go_up, "w")
window.onkey(go_down, "s")
window.onkey(go_right, "d")
window.onkey(go_left, "a")

# Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(0.50, 0.50)
food.goto(0, 0)

# High Score Counter
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 360)


def update_score(score, score_change, high_score):
    '''
    score: integer, current score in game
    score_change: integer, number by which score will be modified
    high_score: integer, highest value of score across all games
    Returns: new value of score, as well as a new high score if game score is 
    higher than the previous high score
    '''
    new_score = score + score_change
    if new_score > high_score:
        new_high_score = new_score
    else:
        new_high_score = high_score
    pen.clear()
    pen.write("Score: {} High Score: {}".format(new_score, new_high_score), 
              align="center", font=("Courier", 24, "normal"))
    return new_score, new_high_score


score, high_score = update_score(0, 0, 0)

segments = []


def game_over(segments, score, high_score):
    '''
    segments: array, current segments of snake in game loop
    Returns: New segments array, score and high score, resetting head position
    and clearing all segments
    '''
    time.sleep(1)
    head.goto(0, 100)
    head.direction = "stop"
    # Hide the segments
    for segment in segments:
        segment.goto(1000, 1000)
    # clear segment list
    new_segments = []
    new_score, new_high_score = update_score(score, -score, high_score)
    food.goto(0, 0)
    return new_segments, new_score, new_high_score


# Main Game Loop
while True:
    window.update()
    move()
    time.sleep(delay)
    if head.distance(food) < 15:
        # Move the food to a random position on screen
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        # Increase score, check for high score increase
        score, high_score = update_score(score, 10, high_score)
        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        print(len(segments))
    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    # Move the end segment in reverse order
    for index in reversed(range(len(segments))):
        if segments[index].distance(head) < 20 and index != 0:
            segments, score, high_score = game_over(segments, score, high_score)
            break
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    # Check for collision
    if head.xcor() > 390 or head.xcor() < -390 or head.ycor() > 390 or head.ycor() < -390:
        segments, score, high_score = game_over(segments, score, high_score)