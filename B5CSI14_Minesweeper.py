import random
import re


class Board:
    def __init__(self, boardSize, boardBombs):
        self.boardSize = boardSize
        self.boardBombs = boardBombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_new_board(self):

        board = [[None for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        bombsPlanted = 0
        while bombsPlanted < self.boardBombs:
            loc = random.randint(0, self.boardSize ** 2 - 1)
            row = loc // self.boardSize
            col = loc % self.boardSize

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombsPlanted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.boardSize):
            for c in range(self.boardSize):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):

        num_neighbouring_bombs = 0
        for r in range(max(0, row - 1), min(self.boardSize - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.boardSize - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs

    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.boardSize - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.boardSize - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):

        visible_board = [[None for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

                # This code is for format
        string_rep = ''

        widths = []
        for idx in range(self.boardSize):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                        max(columns, key=len)
                    )
            )

        indices = [i for i in range(self.boardSize)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.boardSize)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


# Code for game functionality
def play(boardSize=10, boardBombs=10):
    board = Board(boardSize, boardBombs)

    safe = True

    while len(board.dug) < board.boardSize ** 2 - boardBombs:
        print(board)
        user_input = re.split(',(\\s)*', 
        input("Where would you like to dig ? Input as row,column: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.boardSize or col < 0 or col >= boardSize:
            print("Invalid location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("\nCONGRATULAIONS!!! You avoided every single landmine!")
    else:
        board.dug = [(r, c) for r in range(board.boardSize) for c in range(board.boardSize)]
        print(board)
        print("\t|| GAME OVER ||")

# Added instructions 11/9/21
def rules():
    print('''\t\t|| MINESWEEPER ||\n
    - Your objective is to clear the board in front of you
      without triggering any landmines(*) with the help from
      clues about the number of neighbouring mines in each field.

    - For example if a tile shows the number "2", it means that
      tile is in contact with two landmines (in 3x3 field around the tile).

    - Play the game yourselves to get the hang of it''')

    userInput = input("\tPress |S| to Start the game or |Q| to Quit\n")
    if userInput == "S":
          play()
    elif userInput == "Q":
          print("Thankyou !")
    else:
          print("Invalid choice, press only |P| or |Q|")        


print("1. Start Game\n2. What exactly are you supposed to do ?\n3. Quit Game\n")

userInput = int(input("Enter your choice below\n"))

if userInput == 1:
    play()
elif userInput == 2:
    rules()
elif userInput == 3:
    print("Thankyou !")
else:
    print("Enter a valid option")