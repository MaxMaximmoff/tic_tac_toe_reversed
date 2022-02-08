# -*- coding: utf-8 -*-
"""
Игра 'Крестики-нолики-поддавки'.
"""

import random
PLAY_BOARD = [str(num) for num in range(1, 101)]
PLAYERS_MARKS = ['X', 'O']


def make_D2_matrix(board):
    """ Заполнение двухмерной матрицы """
    D2_matrix = []
    for i in range(10):
        item = i * 10
        start = item  # start position of slice
        stop = start + 10  # end position of slice
        slice_object = slice(start, stop)
        D2_matrix.append(board[slice_object])
    return D2_matrix


def get_submatrix(D2_matrix, begRow, begCol):
    """ Выделение матрицы 5 на 5 """
    endRow = begRow + 4
    endCol = begCol + 4
    SubMatrix = []
    for Row in D2_matrix[begRow: endRow+1]:
        SubMatrix += [Row[begCol:endCol+1]]
    return SubMatrix


def display_board(D2_matrix):
    """ Генерация игрового поля """
    for row in range(10):

        print("%-2s | %-2s | %-2s | %-2s | %-2s | %-2s | %-2s | %-2s | %-2s | %-2s" % (D2_matrix[row][0], D2_matrix[row][1], D2_matrix[row][2], D2_matrix[
              row][3], D2_matrix[row][4], D2_matrix[row][5], D2_matrix[row][6], D2_matrix[row][7], D2_matrix[row][8], D2_matrix[row][9]))

        print('-- | -- | -- | -- | -- | -- | -- | -- | -- | --')


def win_check(submatrix, mark):
    """ Проверка проиграл ли игрок с указанным маркером игру """
    return (
        (submatrix[0][0] == submatrix[0][1] == submatrix[0][2] == submatrix[0][3] == submatrix[0][4] == mark) or (
            submatrix[1][0] == submatrix[1][1] == submatrix[1][2] == submatrix[1][3] == submatrix[1][4] == mark)
        or (submatrix[2][0] == submatrix[2][1] == submatrix[2][2] == submatrix[2][3] == submatrix[2][4] == mark)
        or (submatrix[3][0] == submatrix[3][1] == submatrix[3][2] == submatrix[3][3] == submatrix[3][4] == mark)
        or (submatrix[4][0] == submatrix[4][1] == submatrix[4][2] == submatrix[4][3] == submatrix[4][4] == mark)
        or (submatrix[0][0] == submatrix[1][0] == submatrix[2][0] == submatrix[3][0] == submatrix[4][0] == mark)
        or (submatrix[0][1] == submatrix[1][1] == submatrix[2][1] == submatrix[3][1] == submatrix[4][1] == mark)
        or (submatrix[0][2] == submatrix[1][2] == submatrix[2][2] == submatrix[3][2] == submatrix[4][2] == mark)
        or (submatrix[0][3] == submatrix[1][3] == submatrix[2][3] == submatrix[3][3] == submatrix[4][3] == mark)
        or (submatrix[0][4] == submatrix[1][4] == submatrix[2][4] == submatrix[3][4] == submatrix[4][4] == mark)
        or (submatrix[0][0] == submatrix[1][1] == submatrix[2][2] == submatrix[3][3] == submatrix[4][4] == mark)
        or (submatrix[0][4] == submatrix[1][3] == submatrix[2][2] == submatrix[3][1] == submatrix[4][0] == mark)
    )


def player_input():
    """Выбор игровой роли: крестик или нолик"""

    player_first = ""
    while player_first not in ('X', 'O'):
        player_first = input('Вы хотите играть за X или O? ').upper()

    if player_first == 'X':
        player_second = 'O'
        print(f'Бот будет ходить за {player_second}')
    else:
        player_second = 'X'

    return player_first, player_second


def place_marker(board, marker, position):
    """Установка маркера игрока в указанную позицию"""
    board[position] = marker


def choose_first():
    """Определение случайным образом игрока, который будет ходить первым"""

    return PLAYERS_MARKS[random.choice((0, 1))]


def space_check(board, position):
    """Определение пуста ли ячейка в указанной позиции"""

    return board[position] not in PLAYERS_MARKS


def full_board_check(board):
    """Определяет имеется ли на игровой доске оба маркера: X и O"""

    return len(set(board)) == 2


def player_choice(board, player_mark):
    """Выбор игроком следующей ячейки для хода и проверка того можно ли поставить маркер в эту ячейку"""

    position = 0

    while position not in [num for num in range(1, 101)]:
        try:
            position = int(
                input(f'Игрок "{player_mark}", выберите ячейку с 1 по 100: '))
        except ValueError as exc:
            print(f'Неверное значение: {exc}. Пожалуйста, попробуйте снова.')

    position -= 1
    if space_check(board, position):
        return position

    return False


def bot_choice(board):
    """Выбор ботом следующей ячейки случайным образом и проверка того можно ли поставить маркер в эту ячейку"""

    position = random.randrange(0, 100)

    if space_check(board, position):
        return position

    return False


def replay():
    """Предложение игрокам начать игру заново"""

    decision = ""
    while decision not in ('y', 'n'):
        decision = input(
            'Вы бы хотели поиграть еще раз? Напишите "y" или "n" '
        ).lower()

    return decision == 'y'


def clear_screen():
    """Очищение игрового экрана добавлением пустых строк"""

    print('\n' * 100)


def switch_player(mark):
    """Переключение роли игрока для смены очереди для хода"""

    return 'O' if mark == 'X' else 'X'


def check_game_finish(D2_matrix, mark):
    """Проверка того, завершена ли игра"""

    for begRow in range(0, 6):
        for begCol in range(0, 6):
            submatrix = get_submatrix(D2_matrix, begRow, begCol)
            if win_check(submatrix, mark):
                print(f'Игрок "{mark}" проиграл!')
                return True

    if full_board_check(PLAY_BOARD):
        print('Игра завершилась вничью.')
        return True

    return False


print('Добро пожаловать в игру "Крестики-нолики-поддавки"!')

# Выбор игровой роли: крестик или нолик
PLAYER_MARKS = player_input()
# Маркер для бота
BOT_PLAYER_MARK = PLAYER_MARKS[1]
# Определение случайным образом игрока, который будет ходить первым
CURRENT_PLAYER_MARK = choose_first()

print(f'Игрок "{CURRENT_PLAYER_MARK}" ходит первым.')

while True:
    # Генерация игрового поля
    D2_matrix = make_D2_matrix(PLAY_BOARD)
    display_board(D2_matrix)

    print(
        f'Бот играет за "{BOT_PLAYER_MARK}". Очередь игрока "{CURRENT_PLAYER_MARK}":')
    # Выбор игроком следующей ячейки для хода и проверка того можно ли поставить маркер в эту ячейку
    if CURRENT_PLAYER_MARK == BOT_PLAYER_MARK:
        PLAYER_POSITION = False
        while (PLAYER_POSITION is False):
            PLAYER_POSITION = bot_choice(PLAY_BOARD)
        # Установка маркера игрока в указанную позицию
        place_marker(PLAY_BOARD, CURRENT_PLAYER_MARK, PLAYER_POSITION)
    else:
        PLAYER_POSITION = False
        while (PLAYER_POSITION is False):
            PLAYER_POSITION = player_choice(PLAY_BOARD, CURRENT_PLAYER_MARK)
        # Установка маркера игрока в указанную позицию
        place_marker(PLAY_BOARD, CURRENT_PLAYER_MARK, PLAYER_POSITION)
    D2_matrix = make_D2_matrix(PLAY_BOARD)

    # Проверка того, завершена ли игра
    if check_game_finish(D2_matrix, CURRENT_PLAYER_MARK):
        display_board(D2_matrix)
        if not replay():
            break
        else:
            PLAY_BOARD = [str(num) for num in range(1, 101)]
            PLAYER_MARKS = player_input()
            CURRENT_PLAYER_MARK = choose_first()
    else:
        CURRENT_PLAYER_MARK = switch_player(CURRENT_PLAYER_MARK)
    clear_screen()
