def print_state(game_state):
    for i in range(3):
        row_i = game_state[i]
        print(" %s | %s | %s " % (row_i[0], row_i[1], row_i[2]))
        if i != 2:
            print("-----------")
        else:
            print("\n===========\n")


def get_opponent(player):
    if player == 'x':
        return 'o'
    return 'x'


def get_player(game_state, x, y):
    return game_state[y][x]


def get_remaining_places(game_state):
    remaining = 0
    for i in range(3):
        for j in range(3):
            if game_state[i][j] == ' ':
                remaining += 1
    return remaining


# Return new state by putting player in position r, c of current state.
def get_new_state(current_state, r, c, player):
    new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    for i in range(3):
        for j in range(3):
            new_state[i][j] = current_state[i][j]

    new_state[r][c] = player
    return new_state


def get_score(new_state, player):
    remaining_places = get_remaining_places(new_state)

    winner = get_winner(new_state)
    if winner == player:
        return 1

    opponent = get_opponent(player)
    if winner == opponent:
        return -1

    if remaining_places == 0:
        return 0

    child_states = get_child_states(new_state, opponent)
    total_score = 0
    for child_state in child_states:
        score = get_score(child_state, opponent)
        # Subtract the score because we are checking for opponent
        total_score -= score
    return total_score


def get_child_states(current_state, player):
    child_states = []
    for r in range(3):
        for c in range(3):
            if current_state[r][c] == ' ':
                new_state = get_new_state(current_state, r, c, player)
                child_states.append(new_state)
    return child_states


def get_next_state(current_state, player):
    max_score = -99999
    best_state = None

    child_states = get_child_states(current_state, player)
    for child_state in child_states:
        winner = get_winner(child_state)
        if winner == player:
            return child_state

        score = get_score(child_state, player)
        if score > max_score:
            max_score = score
            best_state = child_state
    return best_state


def get_winner(game_state):
    # horizontal
    for i in range(3):
        central = get_player(game_state, i, 1)
        if central != ' ' and get_player(game_state, i, 0) == central and get_player(game_state, i, 2) == central:
            return central

    # vertical
    for i in range(3):
        central = get_player(game_state, 1, i)
        if central != ' ' and get_player(game_state, 0, i) == central and get_player(game_state, 2, i) == central:
            return central

    # diagonal
    central = get_player(game_state, 1, 1)
    if central != ' ':
        if get_player(game_state, 0, 0) == central and get_player(game_state, 2, 2) == central:
            return central
        if get_player(game_state, 0, 2) == central and get_player(game_state, 2, 0) == central:
            return central

    return ' '


def is_space_available(current_state):
    for r in range(3):
        for c in range(3):
            if current_state[r][c] == ' ':
                return True
    return False


currentPlayer = 'o'
gameState = [
    [' ', ' ', ' '],
    [' ', 'x', ' '],
    [' ', ' ', ' ']
]

print_state(gameState)
while is_space_available(gameState):
    if currentPlayer == 'o':
        print("Enter 1-9")

        index = int(input()) - 1
        row = int(index / 3)
        col = index % 3

        if gameState[row][col] != ' ':
            print("Space not available!")
            continue

        gameState[row][col] = 'o'
        print_state(gameState)

        if get_winner(gameState) == 'o':
            print("You win!")
            break
        currentPlayer = 'x'

    else:
        print("Computer's turn...")
        gameState = get_next_state(gameState, 'x')
        print_state(gameState)
        if get_winner(gameState) == 'x':
            print("Computer wins!")
            break
        currentPlayer = 'o'

if not is_space_available(gameState):
    print("Draw!")
