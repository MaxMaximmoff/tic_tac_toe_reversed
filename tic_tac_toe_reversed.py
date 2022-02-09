# -*- coding: utf-8 -*-
"""
Игра 'Крестики-нолики-поддавки'.
"""

import random
play_board = [str(num) for num in range(1, 101)]
player_marks = ['X', 'O']


def make_matrix(board):
    """ Заполнение двухмерной матрицы """

    matrix = []
    for i in range(10):
        item = i * 10
        start = item  # start position of slice
        stop = start + 10  # end position of slice
        slice_object = slice(start, stop)
        matrix.append(board[slice_object])

    for i in range(10):
        for j in range(10):
            if matrix[i][j] not in ('X', 'O'):
                matrix[i][j] = ''

    return matrix


def get_submatrix(matrix, beg_row, beg_col):
    """ Выделение матрицы 5 на 5 """

    end_row = beg_row + 4
    end_col = beg_col + 4
    submatrix = []
    for row in matrix[beg_row: end_row+1]:
        submatrix += [row[beg_col:end_col+1]]
    return submatrix


def display_board(matrix):
    """ Генерация игрового поля """

    print('     1    2    3    4    5    6    7    8    9    10 ')
    print('   |----|----|----|----|----|----|----|----|----|----|')
    for row in range(10):
        row_num = str(row + 1)
        print("%2s | %-3s| %-3s| %-3s| %-3s| %-3s| %-3s| %-3s| %-3s| %-3s| %-3s|" % (row_num, matrix[row][0], matrix[row][1], matrix[row][2], matrix[
              row][3], matrix[row][4], matrix[row][5], matrix[row][6], matrix[row][7], matrix[row][8], matrix[row][9]))

        print('   |----|----|----|----|----|----|----|----|----|----|')


def win_check(submatrix, mark):
    """ Проверка проиграл ли игрок с указанным маркером игру """

    l = len(submatrix[0])
    filled_line = [mark, mark, mark, mark, mark]
    # Проверка заполнености по рядам, столбцам и двум главным диагоналям
    for i in range(l):
        if ((submatrix[:][i] == filled_line)
            or ([x[i] for x in submatrix] == filled_line)
            or ([submatrix[i][i] for i in range(l)] == filled_line)
                or ([submatrix[l-1-i][i] for i in range(l-1, -1, -1)] == filled_line)):
            return True
    return False


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

    return player_marks[random.choice((0, 1))]


def space_check(board, position):
    """Определение пуста ли ячейка в указанной позиции"""

    return board[position] not in player_marks


def full_board_check(board):
    """Определяет имеется ли на игровой доске оба маркера: X и O"""

    return len(set(board)) == 2


def player_choice(board):
    """Выбор игроком следующей ячейки для хода и проверка того можно ли поставить маркер в эту ячейку"""

    position = 0

    while True:
        coordinates = input(
            "Введите координаты x и y через пробел: ").split()
        try:
            x = int(coordinates[0])
            y = int(coordinates[1])
        except ValueError:
            print("Вы должны вводить числа!")
            continue
        except IndexError:
            print("Должно быть два числа с пробелом между ними!")
            continue
        if 0 < x < 11 and 0 < y < 11:
            position = (y - 1) * 10 + x - 1
            if space_check(board, position):
                return position
            print("Эта ячейка занята! Выберите другую!")
        else:
            print("Координаты должны быть от 1 до 10!")

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


def check_game_finish(matrix, mark):
    """Проверка того, завершена ли игра"""

    for beg_row in range(0, 6):
        for beg_col in range(0, 6):
            submatrix = get_submatrix(matrix, beg_row, beg_col)
            if win_check(submatrix, mark):
                print(f'Игрок "{mark}" проиграл!')
                return True

    if full_board_check(play_board):
        print('Игра завершилась вничью.')
        return True

    return False


# matrix = make_matrix(play_board)
# display_board(matrix)

print('Добро пожаловать в игру "Крестики-нолики-поддавки"!')

# Выбор игровой роли: крестик или нолик
player_marks = player_input()
# Маркер для бота
bot_player_mark = player_marks[1]
# Определение случайным образом игрока, который будет ходить первым
current_player_mark = choose_first()

print(f'Игрок "{current_player_mark}" ходит первым.')

while True:
    # Генерация игрового поля
    matrix = make_matrix(play_board)
    display_board(matrix)

    print(
        f'Бот играет за "{bot_player_mark}". Очередь игрока "{current_player_mark}":')

    if current_player_mark == bot_player_mark:
        player_position = False
        while (player_position is False):
            player_position = bot_choice(play_board)
        # Установка маркера бота в указанную позицию
        place_marker(play_board, current_player_mark, player_position)
    else:
        player_position = False
        while (player_position is False):
            player_position = player_choice(play_board)
        # Установка маркера игрока в указанную позицию
        place_marker(play_board, current_player_mark, player_position)
    matrix = make_matrix(play_board)

    # Проверка того, завершена ли игра
    if check_game_finish(matrix, current_player_mark):
        display_board(matrix)
        if not replay():
            break
        else:
            play_board = [str(num) for num in range(1, 101)]
            player_marks = player_input()
            bot_player_mark = player_marks[1]
            current_player_mark = choose_first()
    else:
        current_player_mark = switch_player(current_player_mark)
    clear_screen()
