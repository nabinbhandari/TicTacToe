gameState = [
    ['o', 'o', 'x'],
    ['', 'x', ''],
    ['x', 'x', 'o']
]


def get_player(game_state, x, y):
    return game_state[y][x]


def get_winner(game_state):
    # horizontal
    for i in range(3):
        central = get_player(game_state, i, 1)
        if central != '' and get_player(game_state, i, 0) == central and get_player(game_state, i, 2) == central:
            return central

    # vertical
    for i in range(3):
        central = get_player(game_state, 1, i)
        if central != '' and get_player(game_state, 0, i) == central and get_player(game_state, 2, i) == central:
            return central

    # diagonal
    central = get_player(game_state, 1, 1)
    if central != '':
        if get_player(game_state, 0, 0) == central and get_player(game_state, 2, 2) == central:
            return central
        if get_player(game_state, 0, 2) == central and get_player(game_state, 2, 0) == central:
            return central

    return ''


print("Winner is: " + get_winner(gameState))
