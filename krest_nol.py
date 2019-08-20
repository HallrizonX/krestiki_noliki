import numpy as np
import copy
import os
from random import randint


class GameField:
    matrix: np.array
    storage: dict = {
        'user1': [],
        'user2': []
    }
    win_user = ''

    def __init__(self, row, column):
        self.matrix = GameField.__create_matrix(row, column)
        self.row = row
        self.column = column
        self.win_combination = np.zeros(int(self.row), int)

    def add_to_storage(self, user, row, column):
        self.storage[user].append([row, column])
        self.matrix[row][column] = int(user[-1])

    def __random_value(self):
        """ For testing """
        tmp = False
        for i, row in enumerate(self.matrix):
            for j, column in enumerate(row):
                self.add_to_storage('user1', i, j) if j % 2 else self.add_to_storage('user2', i, j)
                tmp = not tmp

    def show_matrix(self):
        syphols = {
            '1': '0',
            '2': 'X',
            '3': 'Y',
        }

        matrix_str = ''

        for row in self.matrix:
            row_str = ''

            for val in row:
                val = '-' if val == 0 else syphols[str(val)]

                row_str += f'|{val}|'
            matrix_str += f'{row_str}\n'

        print(matrix_str)

    @staticmethod
    def __create_matrix(row, column) -> np.array:
        return np.zeros((row, column), np.int)


class GameController(GameField):
    VERTICAL: str = 'vertical'
    HORIZONTAL: str = 'horizontal'

    def __init__(self, row: np.int8 = 3, column: np.int8 = 3):
        super().__init__(row, column)

    def verify_horizontal(self):
        self.check(position=self.HORIZONTAL)

    def verify_vertical(self):
        self.check(position=self.VERTICAL)

    def check(self, position):
        for user in self.storage:
            vectors = self.storage[user]
            for i, row in enumerate(self.matrix):
                win_combination = copy.copy(self.win_combination)
                for j, column in enumerate(row):

                    if position == 'vertical':
                        if [j, i] in vectors:
                            win_combination[j] = 1
                        else:
                            break
                    elif position == 'horizontal':
                        if [i, j] in vectors:
                            win_combination[j] = 1
                        else:
                            break

                if np.sum(win_combination) == self.row:
                    self.win_user = user

                    break

    def verify_left_diagonal(self):
        for user in self.storage:
            vectors = self.storage[user]
            win_combination = copy.copy(self.win_combination)

            for key, row in enumerate(self.matrix):
                if [key, key] in vectors:
                    win_combination[key] = 1
                else:
                    continue

            if np.sum(win_combination) == self.row:
                print(f'{user} win left diagonal')
                self.win_user = user
                break

    def verify_right_diagonal(self):
        for user in self.storage:
            vectors = self.storage[user]
            win_combination = copy.copy(self.win_combination)

            for key, row in enumerate(self.matrix):
                column_index = (len(self.matrix) - 1) - key
                if [key, column_index] in vectors:
                    win_combination[key] = 1
                else:
                    continue

            if np.sum(win_combination) == self.row:
                self.win_user = user
                break


class Game(GameController):
    def run(self):

        arr_fnc_check = [
            self.verify_horizontal,
            self.verify_left_diagonal,
            self.verify_right_diagonal,
            self.verify_vertical,
        ]

        while True:
            for user in self.storage:
                row = int(input('Enter row: ')) - 1
                column = int(input('Enter column: ')) - 1
                self.add_to_storage(user=user,
                                    row=row,
                                    column=column)

                os.system('cls' if os.name == 'nt' else 'clear')
                game.show_matrix()

                for fnc in arr_fnc_check:
                    fnc()
                    if len(self.win_user) > 0:
                        print(fnc.__name__)
                        print(self.win_user)
                        break
                if len(self.win_user) > 0:
                    break
            if len(self.win_user) > 0:
                break


if __name__ == "__main__":
    game = Game()
    game.run()
