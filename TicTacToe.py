symbols = {0:' ', 1:'X', 4:'O'}

class Cell:
    def __init__(self):
        self.value = 0
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def is_empty(self):
        return self.value == 0
    
class Line:
    def __init__(self, cell_list):
        self.cell_list = cell_list
    
    def get_line_value(self):
        return sum([cell.get_value() for cell in self.cell_list])

    
class Game:
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

def verify_input(number):
    return number in range(3)

game = Game()
victory = False

while game.turn < 10 and not victory:
    player = 2 - game.turn % 2
    print(game)

    print(f"Player {player} turn.")

    row = int(input(f"Player {player}, please select a row: ")) - 1
    if not verify_input(row):
        print("You must enter 1,2, or 3. Please try again.")
        continue

    col = int(input(f"Player {player}, please select a column: ")) - 1
    if not verify_input(col):
        print("You must enter 1,2, or 3. Please try again.")
        continue

    if game.is_spot_full(row, col):
        print("This spot is already full! Try again.")
        continue

    game.mark_spot(row, col, player)

    victory = game.check_win()

if not victory:
    print(game)
    print("It's a tie.")
