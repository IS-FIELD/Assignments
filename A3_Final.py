import turtle
import random
import time
from functools import partial


current_key = None
ending = None
game_screen = None
game_monsters = []
game_food = {}
game_intro = None
game_status_display = None
game_time = -1
hit_count = 0
init_body = 5
is_game_active = True
last_size = 5
last_direction = None
player_snake = None
snake_body = []
touch_count = None


end_game_font = ("Arial", 24, "bold")
food_text_font = ("Arial", 12, "bold")
start_screen_font = ("Arial", 16, "normal")
status_text_font = ("Arial", 18, "normal")
snake_body_color = ("blue", "black")
snake_head_color = "red"
monster_color = "purple"

snake_timer = 250
grid_size = 20
GAME_SIZE = 500
status_bar_height = 40
screen_margin = 30
collision_tolerance = 10

direction_keys = {
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "pause": "space",
}
direction_angles = {
    direction_keys["up"]: 90,
    direction_keys["down"]: 270,
    direction_keys["left"]: 180,
    direction_keys["right"]: 0,
}
food_movement_distance = 40


def init_screen():
    s = turtle.Screen()
    s.tracer(0)
    width = GAME_SIZE + screen_margin * 2
    height = GAME_SIZE + screen_margin * 2 + status_bar_height
    s.setup(width, height)
    s.title("Louis Snake Game")
    s.mode("standard")
    return s


def setup_game_area():
    border = spawn_turtle(0, 0, "", "black")
    area_size = GAME_SIZE // grid_size
    border.shapesize(area_size, area_size, 3)
    border.goto(0, status_bar_height // 2)
    status_bar = spawn_turtle(0, 0, "", "black")
    status_width, status_height = status_bar_height // grid_size, GAME_SIZE // grid_size
    status_bar.shapesize(status_width, status_height, 3)
    status_bar.goto(0, GAME_SIZE // 2)
    intro_message = spawn_turtle(-200, 0)
    intro_message.hideturtle()
    intro_message.write("Click To Start \n\n Let's Go!", font=start_screen_font)
    intro_message.color("")
    intro_message.stamp()
    status_message = spawn_turtle(0, 0, "", "black")
    status_message.hideturtle()
    status_message.goto(-200, status_bar.ycor() - 10)
    return intro_message, status_message


def refresh_status():
    global game_time, hit_count, touch_count
    if is_game_active is False:
        return None
    game_status_display.clear()
    if game_time == -1:
        total_time = 0
    else:
        total_time = time.time() - game_time
    touch_count = hit_count // 2
    elapsed_time = int(total_time)
    status_text = f"contact-{touch_count} time-{elapsed_time}  movement-{current_key}"
    game_status_display.write(status_text, font=status_text_font)
    game_screen.ontimer(refresh_status, 500)
    game_screen.update()


def process_key_press(key):
    global current_key
    current_key = key
    refresh_status()


def spawn_turtle(x, y, color="red", outline="black"):
    turtle_obj = turtle.Turtle("square")
    turtle_obj.color(outline, color)
    turtle_obj.up()
    turtle_obj.goto(x, y)
    return turtle_obj


def spawn_monsters():
    global game_monsters
    for i in range(4):
        x, y = monter_pos()
        monster = spawn_turtle(x, y, monster_color, "black")
        game_monsters.append(monster)


def spawn_food():
    global game_food
    food_id = 1
    while len(game_food) < 5:
        x = random.randint(-GAME_SIZE // 2, GAME_SIZE // 2) // grid_size * grid_size
        y = (
            random.randint(-GAME_SIZE // 2 + 20, GAME_SIZE // 2 - 60)
            // grid_size
            * grid_size
        )
        if boundary_out(x, y) is not True:
            continue
        food_location = spawn_turtle(x, y, "", "black")
        TEXT = spawn_turtle(x + 1, y - 10, "black", "black")
        TEXT.write(str(food_id), align="center", font=food_text_font)
        TEXT.hideturtle()
        food_location.hideturtle()
        game_food[food_id] = (food_location, TEXT)
        food_id += 1


def snake_movement_timer():
    global snake_body, game_monsters, ending
    consume_game_food()
    if is_game_active is not True:
        return None
    if check_game_stop():
        return None
    player_snake.color(*snake_body_color)
    player_snake.stamp()
    snake_body.append(player_snake.pos())
    player_snake.color(snake_head_color)
    player_snake.setheading(direction_angles[current_key])
    player_snake.forward(grid_size)
    if len(player_snake.stampItems) == 21:
        ending = "win "
        win_lose()

    if len(player_snake.stampItems) > init_body:
        player_snake.clearstamps(1)
        snake_body.pop(0)
    for monster in game_monsters:
        if monster.distance(player_snake) < grid_size:
            ending = "lose "
            win_lose()

    game_screen.update()
    speed_adjustment = adjust_speed()
    game_screen.ontimer(snake_movement_timer, snake_timer + speed_adjustment)
    game_screen.update()


def monster_movement_timer(monster):
    global game_monsters, snake_body, hit_count, ending
    if is_game_active is not True:
        return None
    monster_direction = monster.towards(player_snake)
    direction_quarter = monster_direction // 45
    monster_heading = (
        direction_quarter * 45
        if direction_quarter % 2 == 0
        else (direction_quarter + 1) * 45
    )
    monster.setheading(monster_heading)
    monster.forward(grid_size)
    game_screen.update()
    if monster.distance(player_snake) < grid_size:
        ending = "lose "
        win_lose()
    for tail_segment in snake_body:
        if monster.distance(tail_segment) < (grid_size // 2 + collision_tolerance // 2):
            hit_count += 1
    movement_delay = random.randint(snake_timer - 50, snake_timer + 500)
    game_screen.ontimer(lambda: monster_movement_timer(monster), movement_delay)


def monter_pos():
    while True:
        m = random.randint(
            -(GAME_SIZE - screen_margin) // 2 // grid_size + 1,
            (GAME_SIZE - screen_margin) // 2 // grid_size - 1,
        )
        n = random.randint(
            -(GAME_SIZE - screen_margin) // 2 // grid_size + 2,
            (GAME_SIZE - status_bar_height - screen_margin) // 2 // grid_size - 1,
        )
        x, y = (m - 0.5) * grid_size, (n - 0.5) * grid_size
        if x**2 + y**2 >= 40000:
            break
        if boundary_out(x, y) is not True:
            break
    return x, y


def food_movement_timer(food_location, food_item, food_number):
    global game_screen, is_game_active
    movement_delay = random.randint(1000, 10000)
    move_direction = random.randint(0, 1)
    if is_game_active is not True:
        return None
    if (food_location, food_item) not in game_food.values():
        return None
    current_position = food_location.pos()
    move_angle = random.randint(0, 3) * 90
    new_x, new_y = compass(current_position[0], current_position[1], move_angle)
    within_boundary_1 = boundary_out(
        new_x + collision_tolerance + 1, new_y + collision_tolerance + 1
    )
    within_boundary_2 = boundary_out(
        new_x - collision_tolerance - 1, new_y - collision_tolerance - 1
    )
    if within_boundary_1 is not True or within_boundary_2 is not True:
        move_direction = 0
    food_location.setheading(move_angle)
    food_item.setheading(move_angle)
    food_location.forward(food_movement_distance * move_direction)
    food_item.forward(food_movement_distance * move_direction)
    food_item.clear()
    food_item.write(food_number, align="center", font=food_text_font)
    food_item.hideturtle()
    game_screen.update()
    game_screen.ontimer(
        lambda: food_movement_timer(food_location, food_item, food_number),
        movement_delay,
    )


def consume_game_food():
    global init_body
    for food_key, food_value in game_food.items():
        if player_snake.distance(food_value[0]) < grid_size - 5:
            init_body += food_key
            food_value[0].clear()
            food_value[1].clear()
            game_food.pop(food_key)
            break


def adjust_speed():
    global last_size, player_snake
    if len(player_snake.stampItems) > last_size:
        last_size = len(player_snake.stampItems)
        return 80
    else:
        return 0


def check_game_stop():
    if current_key is None or current_key == "pause":
        game_screen.ontimer(snake_movement_timer, snake_timer)
        return True
    next_x, next_y = compass(
        player_snake.xcor(), player_snake.ycor(), direction_angles[current_key]
    )
    if boundary_out(next_x, next_y) is not True:
        game_screen.ontimer(snake_movement_timer, snake_timer)
        return True


def compass(x, y, heading):
    next_x, next_y = x, y
    if heading == 0:
        next_x += grid_size
    elif heading == 90:
        next_y += grid_size
    elif heading == 180:
        next_x -= grid_size
    elif heading == 270:
        next_y -= grid_size
    return next_x, next_y


def boundary_out(x, y):
    left_boundary = -GAME_SIZE // 2
    right_boundary = GAME_SIZE // 2
    top_boundary = (GAME_SIZE - status_bar_height) // 2
    bottom_boundary = -GAME_SIZE // 2 + grid_size
    if left_boundary <= x <= right_boundary and bottom_boundary <= y <= top_boundary:
        return True


def win_lose():
    global is_game_active, game_screen
    is_game_active = False
    for key in direction_keys.values():
        game_screen.onkey(None, key)
    game_over_message = spawn_turtle(0, 0, "red", "")
    game_over_message.goto(-100, 0)
    game_over_message.color("red")
    if ending == "lose ":
        game_over_message.write("Game Over !!", font=end_game_font)
    if ending == "win ":
        game_over_message.write("Victory !!", font=end_game_font)
    game_over_message.color("")
    game_over_message.hideturtle()
    game_over_message.stamp()
    game_screen.onclick(lambda x, y: game_screen.bye())


def start_game(x, y):
    global game_food, game_time
    game_screen.onscreenclick(None)
    game_time = time.time()
    spawn_food()
    game_intro.clear()
    for key in (
        direction_keys["up"],
        direction_keys["down"],
        direction_keys["left"],
        direction_keys["right"],
    ):
        game_screen.onkey(partial(process_key_press, key), key)
    game_screen.onkey(
        partial(pause_game, direction_keys["pause"]), direction_keys["pause"]
    )
    for n in range(1, 6):
        game_screen.onkey(partial(consume_food, n), str(n))
    snake_movement_timer()
    for monster in game_monsters:
        monster_movement_timer(monster)
    for n in range(len(game_food)):
        food_movement_timer(game_food[n + 1][0], game_food[n + 1][1], n + 1)


def consume_food(num):
    global init_body
    init_body += num
    refresh_status()


def pause_game(direction_keys):
    global current_key, last_direction
    if current_key == "pause":
        current_key = last_direction
    else:
        last_direction = current_key
        current_key = "pause"
    refresh_status()


if __name__ == "__main__":
    game_screen = init_screen()
    game_intro, game_status_display = setup_game_area()
    refresh_status()
    spawn_monsters()
    player_snake = spawn_turtle(0, 0, snake_head_color, "black")
    game_screen.onscreenclick(start_game)
    game_screen.update()
    game_screen.listen()
    game_screen.mainloop()
