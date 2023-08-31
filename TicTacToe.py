# This program is a simple TicTacToe game.
# You can play against the computer or against another player.

symbols = {0:' ', 1:'X', 4:'O'}
conditionals = {"1 To Win": 2, "2 To Win": 8, "1 To Build": 1, "2 To Build": 4, "Empty": 0}

class Cell:
    # This class represents a cell in the grid.
    # It is here to be able to pass by reference the grid location and its integer value.
    def __init__(self):
        self.value = 0
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def is_empty(self):
        return self.value == 0
    
class Line:
    # This class represents a possible winning line in the grid.
    # It can return the sum of the cells value in grid line.
    # It can also return an empty cell in itself.
    def __init__(self, cell_list):
        self.cell_list = cell_list
    
    def get_line_value(self):
        return sum([cell.get_value() for cell in self.cell_list])
    
    def get_empty_cell(self):
        for cell in self.cell_list:
            if cell.is_empty():
                return cell

    
class Game:
    # This class represnts the game grid.
    # It can check and change the spots in the grid, print the grid, and check if the game has been won.
    def __init__(self):
        self.grid = [[Cell() for j in range(3)] for i in range(3)]
        self.turn = 1

        self.lines = [Line(self.grid[i]) for i in range(3)]
        self.lines += [Line([self.grid[i][j] for i in range(3)]) for j in range(3)]
        self.lines.append(Line([self.grid[i][i] for i in range(3)]))
        self.lines.append(Line([self.grid[i][2-i] for i in range(3)]))

    def __repr__(self):        
        return '\n' + '- + - + -\n'.join([' | '.join([symbols[self.grid[i][j].get_value()] for j in range(3)]) + '\n' for i in range(3)])
    
    def is_spot_full(self, row, col):
        return not self.grid[row][col].is_empty()
    
    def mark_spot(self, row, col, player):
        self.grid[row][col].set_value(player ** 2)
        self.turn += 1

    def mark_cell(self, cell, player):
        cell.set_value(player ** 2)
        self.turn += 1

    def check_win(self):
        for line in self.lines:
            if line.get_line_value() == 3:
                print(self)
                print("Player 1 won!")
                return True
            
            if line.get_line_value() == 12:
                print(self)
                print("Player 2 won!")
                return True

        return False 

class AutoPlayer:
    # This class has the logic for the computer player.
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def select_cell(self):
        for line in self.game.lines:
            if line.get_line_value() == conditionals[str(self.player) + " To Win"]:
                self.game.mark_cell(line.get_empty_cell(), self.player)
                return
        
        for line in self.game.lines:
            if line.get_line_value() == conditionals[str(2-self.player//2) + " To Win"]:
                self.game.mark_cell(line.get_empty_cell(), self.player)
                return
            
        for line in self.game.lines:
            if line.get_line_value() == conditionals[str(self.player) + " To Build"]:
                self.game.mark_cell(line.get_empty_cell(), self.player)
                return
            
        for line in self.game.lines:
            if line.get_line_value() == conditionals["Empty"]:
                self.game.mark_cell(line.get_empty_cell(), self.player)
                return
            
        for line in self.game.lines:
            cell = line.get_empty_cell()
            if cell is not None:
                self.game.mark_cell(cell, self.player)
                return

def get_player_choice(game, player):
    # This function get the input from a human player.
    print(f"Player {player} turn.")

    row = int(input(f"Player {player}, please select a row: ")) - 1
    if not verify_input(row):
        print("You must enter 1,2, or 3. Please try again.")
        get_player_choice(player)
        return

    col = int(input(f"Player {player}, please select a column: ")) - 1
    if not verify_input(col):
        print("You must enter 1,2, or 3. Please try again.")
        get_player_choice(player)
        return

    if game.is_spot_full(row, col):
        print("This spot is already full! Try again.")
        get_player_choice(player)
        return

    game.mark_spot(row, col, player)

def verify_input(number):
    return number in range(3)

def assign_player(player):
    # This function assign human or computer player to a player at the beginning of the program.
    user_input = input(f"Is player {player} human? Press y/n: ")
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    else:
        print("You need to enter y or n. Please try again.")
        return assign_player(player)

game = Game()
victory = False
human_players = {}

print("Welcome to TicTacToe!")
human_players[1] = assign_player(1)
human_players[2] = assign_player(2)

computer_players = {key:AutoPlayer(game, key) for key in human_players if not human_players[key]}

while game.turn < 10 and not victory:
    player = 2 - game.turn % 2
    print(game)

    if human_players[player]:
        get_player_choice(game, player)
    else:
        computer_players[player].select_cell()
    
    victory = game.check_win()

if not victory:
    print(game)
    print("It's a tie.")
