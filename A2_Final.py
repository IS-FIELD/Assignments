import turtle
import numpy as np

scr = turtle.Screen()
scr.title("Sliding Puzzle Game")

tiles_dict = {}
TILES = []
ZERO = ()


def main():
    """
    This is the main function that starts the game.
    It doesn't take any parameters and doesn't return anything.
    """
    if not game_size():
        return
    board_setup()
    scr.onclick(click_event)
    turtle.mainloop()


def game_size():
    """
    This function sets up the game size.
    It doesn't take any parameters.
    Returns:
        True if the game size is set successfully, False otherwise.
    """
    global DIM, TILE_SIZE
    size = scr.numinput(
        "Sliding Puzzle", "Enter Game Size (3, 4, 5)", minval=3, maxval=5
    )
    if size is None:
        scr.bye()
        return False
    DIM = int(size)
    TILE_SIZE = 200
    scr.setup(width=TILE_SIZE * DIM, height=TILE_SIZE * DIM)
    return True


def create_matrix(DIM):
    """
    This function creates a random initial state.
    Parameter:
        DIM: the dimension of the game board.
    Return:
        mat: the solvable game board, it's a nested list.
    """
    numbers = np.arange(1, DIM * DIM)
    numbers = np.append(numbers, 0)
    np.random.shuffle(numbers)
    mat = numbers.reshape((DIM, DIM))
    check = np.delete(numbers, np.where(numbers == 0))
    inversions = np.sum(check[:-1] > check[1:])
    while inversions % 2 != 0:
        return create_matrix(DIM)
    return mat


def board_setup():
    """
    This function sets up the game board.
    It doesn't take any parameters and doesn't return anything.
    """
    global tiles_dict, TILES, ZERO
    TILES = create_matrix(DIM)
    ZERO = tuple(*np.argwhere(TILES == 0))
    tiles_dict.clear()

    init_tile = turtle.Turtle()
    init_tile.penup()
    init_tile.shape("square")
    init_tile.shapesize(stretch_wid=TILE_SIZE / 20 - 1, stretch_len=TILE_SIZE / 20 - 1)
    init_tile.color("lightgreen")
    init_tile.speed("fastest")

    init_text = turtle.Turtle()
    init_text.penup()
    init_text.color("blue")
    init_text.hideturtle()

    for i in range(DIM):
        for j in range(DIM):
            num = TILES[i][j]
            tile, text = create_tile(i, j, num, init_tile, init_text)
            tiles_dict[(i, j)] = (tile, text)

    init_tile.hideturtle()
    init_text.hideturtle()


def create_tile(i, j, num, init_tile, init_text):
    """
    This function creates a tile at the specified position with the specified number.
    Parameters:
        i: the row index of the tile.
        j: the column index of the tile.
        num: the number to be placed on the tile.
        init_tile: the turtle object used to draw the tile.
        init_text: the turtle object used to write the number on the tile.
    Returns:
        tile, text: the turtle objects representing the tile and the number on it.
    """
    if num != 0:
        position = (
            j * TILE_SIZE - DIM / 2 * TILE_SIZE + TILE_SIZE / 2,
            -i * TILE_SIZE + DIM / 2 * TILE_SIZE - TILE_SIZE / 2,
        )

        tile = init_tile.clone()
        tile.showturtle()
        tile.goto(position)
        tile.speed(5)
        text = init_text.clone()
        text.goto(position)
        text.write(num, align="center", font=("Arial", 22, "normal"))
        return tile, text
    return None, None


MOVING = False


def set_global_moving_false():
    global MOVING
    MOVING = False


def click_event(x, y):
    """
    This function handles the mouse click event.
    Parameters:
        x: the x-coordinate of the mouse click.
        y: the y-coordinate of the mouse click.
    It doesn't return anything.
    """
    global MOVING
    if MOVING:
        return
    row, col = tile_pos(x, y)
    if row is None or col is None or (row, col) == ZERO:
        return
    if (row, col) != ZERO and adjacent((row, col), ZERO):
        swap((row, col), ZERO)


def tile_pos(x, y):
    """
    This function retrieves the position of the tile.
    Parameters:
        x: the x-coordinate of the mouse click.
        y: the y-coordinate of the mouse click.
    Returns:
        (row, col): the row and column indices of the tile.
    """
    col = int((x + DIM * TILE_SIZE / 2) // TILE_SIZE)
    row = int((-y + DIM * TILE_SIZE / 2) // TILE_SIZE)
    return (row, col) if 0 <= row < DIM and 0 <= col < DIM else (None, None)


def adjacent(pos1, pos2):
    """
    This function checks if two positions are adjacent.
    Parameters:
        pos1: the first position.
        pos2: the second position.
    Returns:
        True if the positions are adjacent, False otherwise.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1


def swap(pos1, pos2):
    """
    This function swaps two tiles.
    Parameters:
        pos1: the position of the first tile.
        pos2: the position of the second tile.
    It doesn't return anything.
    """
    global TILES, tiles_dict, ZERO, MOVING
    tile_info1 = tiles_dict.get(pos1)

    if tile_info1 is not None:
        MOVING = True
        tile1, text1 = tile_info1
        text1.clear()
        tile1.setposition(
            pos2[1] * TILE_SIZE - DIM / 2 * TILE_SIZE + TILE_SIZE / 2,
            -pos2[0] * TILE_SIZE + DIM / 2 * TILE_SIZE - TILE_SIZE / 2,
        )
        text1.goto(tile1.position())
        num = TILES[pos1]
        if num != 0:
            text1.write(num, align="center", font=("Arial", 22, "normal"))
        turtle.ontimer(lambda: set_global_moving_false(), 50)
    TILES[ZERO], TILES[pos1] = TILES[pos1], TILES[ZERO]
    ZERO = pos1
    tiles_dict[ZERO], tiles_dict[pos2] = None, tile_info1

    if np.all(TILES.flatten()[:-1] == np.arange(1, DIM**2)):
        red_tiles()


def red_tiles():
    """
    This function colors all tiles to red.
    It doesn't take any parameters and doesn't return anything.
    """
    for pos, tile_info in tiles_dict.items():
        if tile_info:
            tile, text = tile_info
            tile.color("red")
            text.clear()
            text.color("blue")
            tile_pos = tile.position()
            text.goto(tile_pos[0], tile_pos[1] - 10)
            text.write(
                TILES[pos[0]][pos[1]], align="center", font=("Arial", 22, "normal")
            )
    scr.onclick(None)


if __name__ == "__main__":
    main()
