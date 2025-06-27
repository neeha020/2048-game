import turtle
import random

# Set up the screen
GRID_SIZE = 5  # You can change this to 6, 7, etc.
CELL_SIZE = 60
PADDING = 30
WIDTH = GRID_SIZE * CELL_SIZE + PADDING
HEIGHT = GRID_SIZE * CELL_SIZE + PADDING

wn = turtle.Screen()
wn.title("2048 - Dynamic Grid")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)

# Score
score = 0

# Grid setup
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid_merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Pen for drawing
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.penup()
pen.hideturtle()
pen.turtlesize(stretch_wid=2, stretch_len=2, outline=2)

colors = {
    0: "white", 2: "yellow", 4: "orange", 8: "pink", 16: "red",
    32: "light green", 64: "green", 128: "light blue", 256: "blue",
    512: "purple", 1024: "silver", 2048: "gold", 4096: "brown"
}


def draw_grid():
    pen.clear()
    pen.goto(0, HEIGHT // 2 - 30)
    pen.color("white")
    pen.write(f"Score: {score}", align="center", font=("Courier", 18, "bold"))

    start_y = HEIGHT // 2 - 80
    for y in range(GRID_SIZE):
        start_x = -WIDTH // 2 + 50
        for x in range(GRID_SIZE):
            value = grid[y][x]
            pen.goto(start_x + x * CELL_SIZE, start_y - y * CELL_SIZE)
            pen.color(colors.get(value, "black"))
            pen.stamp()
            pen.color("blue")
            pen.sety(pen.ycor() - 10)
            if value != 0:
                pen.write(str(value), align="center", font=("Courier", 14, "bold"))
            pen.sety(pen.ycor() + 10)
    wn.update()


def reset_grid_merged():
    global grid_merged
    grid_merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def add_random():
    empty = [(y, x) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if grid[y][x] == 0]
    if empty:
        y, x = random.choice(empty)
        grid[y][x] = random.choice([2, 4])


def is_game_over():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                return False
            if x < GRID_SIZE - 1 and grid[y][x] == grid[y][x + 1]:
                return False
            if y < GRID_SIZE - 1 and grid[y][x] == grid[y + 1][x]:
                return False
    return True


def move_grid(dy, dx):
    global score
    moved = False
    for _ in range(GRID_SIZE - 1):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                ny, nx = y + dy, x + dx
                if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE:
                    if grid[ny][nx] == 0 and grid[y][x] != 0:
                        grid[ny][nx], grid[y][x] = grid[y][x], 0
                        moved = True
                    elif grid[ny][nx] == grid[y][x] and not grid_merged[ny][nx] and not grid_merged[y][x]:
                        grid[ny][nx] *= 2
                        grid[y][x] = 0
                        score += grid[ny][nx]
                        grid_merged[ny][nx] = True
                        moved = True
    return moved


def up():
    reset_grid_merged()
    if move_grid(-1, 0):
        add_random()
    draw_grid()
    check_end()


def down():
    reset_grid_merged()
    if move_grid(1, 0):
        add_random()
    draw_grid()
    check_end()


def left():
    reset_grid_merged()
    if move_grid(0, -1):
        add_random()
    draw_grid()
    check_end()


def right():
    reset_grid_merged()
    if move_grid(0, 1):
        add_random()
    draw_grid()
    check_end()


def restart():
    global grid, score
    score = 0
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    reset_grid_merged()
    add_random()
    add_random()
    draw_grid()


def check_end():
    if is_game_over():
        pen.goto(0, 0)
        pen.color("red")
        pen.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
        wn.update()


# Initial game setup
restart()

# Controls
wn.listen()
wn.onkeypress(up, "Up")
wn.onkeypress(down, "Down")
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(restart, "r")

# Main loop
wn.mainloop()
