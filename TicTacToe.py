symbols = {0:' ', 1:'X', 4:'O'}

class Game:
    def __init__(self):
        self.grid = [[0 for j in range(3)] for i in range(3)]
        self.turn = 1

    def __repr__(self):        
        return '\n' + '- + - + -\n'.join([' | '.join([symbols[self.grid[i][j]] for j in range(3)]) + '\n' for i in range(3)])
    
    def is_spot_full(self, row, col):
        return not self.grid[row][col] == 0
    
    def mark_spot(self, row, col, player):
        self.grid[row][col] = player ** 2
        self.turn += 1

    def check_win(self):
        results = []

        for i in range(3):
            results.append(sum(self.grid[i]))
            results.append(sum([self.grid[i][j] for j in range(3)]))
        results.append(sum([self.grid[i][i] for i in range(3)]))
        results.append(sum([self.grid[2-i][i] for i in range(3)]))

        if 3 in results:
            print(self)
            print("Player 1 won!")
            return True
        
        if 12 in results:
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
