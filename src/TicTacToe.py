import random


class GameState:

    def __init__(self):
        self.state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def print_state(self):
        for i in range(3):
            row_i = self.state[i]
            print(" %s | %s | %s " % (row_i[0], row_i[1], row_i[2]))
            if i != 2:
                print("-----------")
            else:
                print("\n===========\n")

    @staticmethod
    def get_opponent(player):
        if player == 'x':
            return 'o'
        return 'x'

    def get_player(self, x, y):
        return self.state[x][y]

    def set_player(self, x, y, player):
        self.state[x][y] = player

    # Return new state by putting player in position r, c of current state.
    def get_new_state(self, r, c, player):
        new_state = GameState()
        for i in range(3):
            for j in range(3):
                new_state.set_player(i, j, self.get_player(i, j))
        new_state.set_player(r, c, player)
        return new_state

    def get_score(self, player):
        winner = self.get_winner()
        if winner == player:
            return 1

        opponent = GameState.get_opponent(player)
        if winner == opponent:
            return -1

        if not self.is_space_available():
            return 0

        child_states = self.get_child_states(opponent)
        total_score = 0
        for child_state in child_states:
            score = child_state.get_score(opponent)
            # Subtract the score because we are checking for opponent
            total_score -= score
        return total_score

    def get_child_states(self, player):
        child_states = []
        for r in range(3):
            for c in range(3):
                if self.get_player(r, c) == ' ':
                    new_state = self.get_new_state(r, c, player)
                    child_states.append(new_state)
        return child_states

    def get_next_state(self, player):
        max_score = -99999

        child_states = self.get_child_states(player)
        best_state = child_states[0]

        opponent = GameState.get_opponent(player)

        for child_state in child_states:
            winner = child_state.get_winner()
            if winner == player:
                return child_state

            grand_child_states = child_state.get_child_states(opponent)

            try:
                for grand_child_state in grand_child_states:
                    if grand_child_state.get_winner() == opponent:
                        # https://stackoverflow.com/a/40957772/5137352
                        raise IndexError
            except IndexError:
                continue

            score = child_state.get_score(player)
            if score > max_score:
                max_score = score
                best_state = child_state
        return best_state

    def get_winner(self):
        # horizontal
        for i in range(3):
            central = self.get_player(i, 1)
            if central != ' ' and self.get_player(i, 0) == central and self.get_player(i, 2) == central:
                return central

        # vertical
        for i in range(3):
            central = self.get_player(1, i)
            if central != ' ' and self.get_player(0, i) == central and self.get_player(2, i) == central:
                return central

        # diagonal
        central = self.get_player(1, 1)
        if central != ' ':
            if self.get_player(0, 0) == central and self.get_player(2, 2) == central:
                return central
            if self.get_player(0, 2) == central and self.get_player(2, 0) == central:
                return central

        return ' '

    def is_space_available(self):
        for r in range(3):
            for c in range(3):
                if self.state[r][c] == ' ':
                    return True
        return False


currentPlayer = random.choice(['x', 'o'])
gameState = GameState()

# If computer plays first, it goes in the middle,
# so doing it manually to save some time.
if currentPlayer == 'x':
    gameState.set_player(1, 1, 'x')
    currentPlayer = 'o'

gameState.print_state()
while gameState.is_space_available():
    if currentPlayer == 'o':
        print("Enter 1-9")

        index = int(input()) - 1
        row = int(index / 3)
        col = index % 3

        if gameState.get_player(row, col) != ' ':
            print("Space not available!")
            continue

        gameState.set_player(row, col, 'o')
        gameState.print_state()

        if gameState.get_winner() == 'o':
            print("You win!")
            exit(0)
        currentPlayer = 'x'

    else:
        print("Computer's turn...")
        gameState = gameState.get_next_state('x')
        gameState.print_state()
        if gameState.get_winner() == 'x':
            print("Computer wins!")
            exit(0)
        currentPlayer = 'o'

if not gameState.is_space_available():
    print("Draw!")
