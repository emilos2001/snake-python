from tkinter import *
import random


WIDTH = 450
HEIGHT = 450
SPEED = 140
SIZE = 25
BODY = 1
SNAKE_COLOR = "green"
FOOD_COLOR1 = "red"
BACKGROUND_COLOR = "black"

window = Tk()
window.title("Snake game")
window.resizable(False, False)
score = 0
direction = 'down'
#but if you want start the game with random direction you need this:
#direction = random.choice(['up', 'down', 'left', 'right']) here the snake will start in random direction
label = Label(window, text="Score:{}".format(score), fg="red", font=('consolas', 20))
label.pack()
label2 = Label(window, text="Speed:{}".format(SPEED), fg="red", font=('consolas', 15))
label2.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()


class Snake:

    def __init__(self):
        self.body_size = BODY
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food1:

    def __init__(self):
        x = random.randint(0, (WIDTH // SIZE) - 1) * SIZE
        y = random.randint(0, (HEIGHT // SIZE) - 1) * SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SIZE, y + SIZE, fill=FOOD_COLOR1, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SIZE
    elif direction == "down":
        y += SIZE
    elif direction == "left":
        x -= SIZE
    elif direction == "right":
        x += SIZE
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        label2.config(text="Speed:{}".format(SPEED))
        canvas.delete("food")
        food = Food1()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
    elif new_direction == 'left':
        if direction != 'right':
            direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 35), text="GAME OVER", fill="red")


window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
snake = Snake()
food = Food1()
next_turn(snake, food)
window.mainloop()
