"""
This Python program implements a sliding puzzle game called "8 Puzzle". The goal of the game is to arrange the numbers 1 to 8 in order from left to right, top to bottom, by moving the blank space.

The running logic of the program is as follows:

1. First, the program will print out the welcome message and rules of the game.

2. Then, the program will call the `prompt` function, prompting the user to input four letters, representing moving left, right, up, and down respectively. This function will check whether the letters input by the user are valid (whether they are letters, whether there are duplicates, whether there are more than four), and return the four letters.

3. Next, the program will call the `create` function to create a random initial state. This function will generate a 3x3 matrix containing numbers 1 to 8 and a blank space, and ensure that this matrix is solvable (i.e., the inversion number of the matrix is even).

4. Then, the program will enter a loop until the user completes the game. In each loop, the program will first call the `detach` function to print out the directions in which the blank space can move. Then, the program will prompt the user to input a direction to move, and call the `move` function to move the blank space according to the user's input. If the user's input is invalid (for example, trying to move the blank space out of the matrix), the `move` function will print out an error message.

5. When the user completes the game (i.e., the numbers in the matrix are arranged in order from left to right, top to bottom), the program will print out the victory message and the number of moves made by the user, and then ask the user whether to start a new game. If the user inputs "n", the program will restart the game; if the user inputs "q", the program will end.

6. Finally, the program will call the `game` function to start the game.

Note: This program uses a global variable `step` to record the number of moves made by the user.
"""

import random

print(
    """
    Welcome to the 8 Puzzle game!

    The 8 Puzzle is a sliding puzzle that consists of a frame of numbered square tiles in random order, with one tile missing. The puzzle also exists in other sizes, particularly the smaller 8 Puzzle. The object of the puzzle is to place the tiles in order by making sliding moves that use the empty space.

    The game board is a 3x3 grid, which should be filled with numbers from 1 to 8. The last cell is the empty one. The player can move the numbers from the cell next to the empty one into this cell.

    The goal of the game is to arrange the numbers in ascending order from left to right, with the empty cell in the last cell of the grid:

    1 2 3
    4 5 6
    7 8 

    You can move the tiles in four directions: up, down, left, and right. Enjoy the game!
    """
)

step = 0


def prompt():
    """
    This function prompts the user for the keys to use for moving the blank space.
    If the user inputs more than 4 letters or duplicate letter or the letter out of a-z, it will ask user to input again
    """
    valid_letters = []
    while len(valid_letters) < 4:
        # Get the input letters from the user
        if len(valid_letters) == 0:
            letters = (
                input(
                    "Please enter the four letters used for left, right, up, and down move: "
                )
                .strip()
                .replace(" ", "")
            )
        else:
            letters = input(
                "Too few letters ,keep enter the rest letters used for left, right, up and down move > "
            )
        # Validate the input letters
        for letter in letters:
            if letter.isalpha():
                if letter.lower() in valid_letters:
                    print("Duplicate letter found, please enter unique letters.")
                    return prompt()
                valid_letters.append(letter.lower())
            else:
                print("Please enter letters (a-z) only")
                return prompt()

        if len(valid_letters) > 4:
            print("Too many letters, please enter exactly four letters.")
            return prompt()

    l, r, u, d = valid_letters
    return l, r, u, d


def count_inversions(mat):
    """
    This function counts the number of inversions in a given state.
    Parameter:
        mat: the matrix is the  nested list returned by the function Create
    Return:
        the integer number of inversions
    """
    flat_mat = [num for row in mat for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_mat)):
        for j in range(i + 1, len(flat_mat)):
            if flat_mat[i] > flat_mat[j]:
                inversions += 1
    return inversions


def create(target):
    """
    This function creates a random initial state
    Parameter:
        target: the nested list returned by the fuction Game, the goal of the game
    Return:
        mat: the solvable 8-puzzle game, it's a nested list
    """
    mat = [num for row in target for num in row]
    random.shuffle(mat)
    mat = [mat[i * 3 : (i + 1) * 3] for i in range(3)]
    while count_inversions(mat) % 2 != 0:
        return create(target)
    print_matrix(mat)
    return mat


def print_matrix(mat):
    """
    This function prints the game board.
    Parameter:
        mat: the matrix is the  nested list returned by the function Create
    Return:
        print the chessboard to the user after every steps
    """
    for row in mat:
        for num in row:
            if num == 0:
                print(" ", end=" ")
            else:
                print(num, end=" ")
        print()


def get_num(mat):
    """
    This function returns the position of a given number in the matrix
    Parameter:
        mat: the matrix is the  nested list returned by the Create function
    Return:
        the position of 0
    """
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 0:
                return i, j


def detach(mat, l, r, u, d):
    """
    This function returns the possible moves for the blank space
    Parameters:
        mat: the matrix is the  nested list returned by the Create function
        l, r, u, d: the moves define by the user, which returned by Prompt fuction
    Return:
        print the possible moves for user
    """
    i, j = get_num(mat)
    moves = []
    L = f"left-{l}"
    R = f"right-{r}"
    U = f"up-{u}"
    D = f"down-{d}"

    if j < 2:
        moves.append(L)
    if j > 0:
        moves.append(R)
    if i < 2:
        moves.append(U)
    if i > 0:
        moves.append(D)
    return f"Please enter your move {moves}>"


def move(mat, dx, dy):
    """
    This function moves the blank space in the given direction
    Parameters:
        mat: the matrix is the  nested list returned by the Create function
        dx,dy: the move direction in the move_map
    Return:
        mat: the refreshed nested list
        or print "Invalid move! " if the move is out of the chessboard
    """
    i, j = get_num(mat)
    global step
    if 0 <= i + dx < 3 and 0 <= j + dy < 3:
        mat[i][j], mat[i + dx][j + dy] = mat[i + dx][j + dy], mat[i][j]
        step += 1

    else:
        print("Invalid move! ")
    print_matrix(mat)
    return mat


def game():
    """
    This main function controls the game flow
    """
    global step
    target = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    l, r, u, d = prompt()
    mat = create(target)
    move_map = {l: (0, 1), r: (0, -1), u: (1, 0), d: (-1, 0)}
    while mat != target:
        move_letter = input(str(detach(mat, l, r, u, d)))
        if move_letter.lower() in move_map:
            mat = move(mat, *move_map[move_letter.lower()])

        else:
            print(f"Invalid move! ")
    print("You win!")
    print(f"You solved the puzzle in {step} moves!")
    user_input = input("Enter 'n' for another game, or 'q' to end the game > ")

    if user_input.lower() == "n":
        print("Starting a new game...")
        step = 0
        return game()

    elif user_input.lower() == "q":
        print("Ending the game. Thank you for playing!")

    else:
        print("Invalid input. Please enter 'n' for a new game or 'q' to quit.")


game()
