"""Простая реализация игры в шашки с проверкой ходов и функцией отмены.

Этот модуль содержит классы для представления игры в шашки, включая доску, ходы
и состояние игры. Он позволяет двум игрокам играть в шашки в консоли с поддержкой
отмены ходов.

Классы:
    Move: Представляет ход в игре.
    CheckersBoard: Представляет доску для шашек и управляет перемещением шашек.
    CheckersGame: Управляет процессом игры и взаимодействием с игроками.
"""


class Move:
    """Представляет ход в игре в шашки.

    Атрибуты:
        start (tuple): Начальная позиция хода в виде координат (x, y).
        end (tuple): Конечная позиция хода в виде координат (x, y).
        piece (str): Шашка, которая перемещается.
        captured_piece (str): Шашка, которая была взята, если такая есть.
        captured_position (tuple): Позиция съеденной шашки, если такая есть.
    """

    def __init__(self, start, end, piece, captured_piece, captured_position=None):
        """Инициализирует экземпляр Move.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).
            piece (str): Шашка, которая перемещается.
            captured_piece (str): Шашка, которая была взята, если такая есть.
            captured_position (tuple): Позиция съеденной шашки, если такая есть.
        """
        self.start = start
        self.end = end
        self.piece = piece
        self.captured_piece = captured_piece
        self.captured_position = captured_position


class CheckersBoard:
    """Представляет доску для шашек и управляет перемещением шашек.

    Атрибуты:
        board (list): Двумерный список, представляющий доску для шашек.
    """

    def __init__(self):
        """Инициализирует доску для шашек стандартной начальной расстановкой."""
        self.board = [
            [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
            ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
            [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['w', ' ', 'w', ' ', 'w', ' ', 'w', ' '],
            [' ', 'w', ' ', 'w', ' ', 'w', ' ', 'w'],
            ['w', ' ', 'w', ' ', 'w', ' ', 'w', ' ']
        ]

    def display(self):
        """Отображает текущее состояние доски для шашек."""
        print("  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print(8 - i)
        print("  a b c d e f g h")

    def move_piece(self, start, end, captured_position=None):
        """Перемещает шашку на доске.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).
            captured_position (tuple): Позиция съеденной шашки, если такая есть.

        Возвращает:
            Move: Объект Move, представляющий выполненный ход.
        """
        x1, y1 = start
        x2, y2 = end
        piece = self.board[y1][x1]
        captured_piece = self.board[y2][x2] if not captured_position else self.board[captured_position[1]][captured_position[0]]

        self.board[y2][x2] = piece
        self.board[y1][x1] = ' '

        if captured_position:
            self.board[captured_position[1]][captured_position[0]] = ' '

        return Move(start, end, piece, captured_piece, captured_position)

    def undo_move(self, move):
        """Отменяет ход на доске.

        Аргументы:
            move (Move): Объект Move, представляющий ход, который нужно отменить.
        """
        start, end = move.start, move.end
        x1, y1 = start
        x2, y2 = end
        self.board[y1][x1] = move.piece
        self.board[y2][x2] = ' '

        if move.captured_position:
            cx, cy = move.captured_position
            self.board[cy][cx] = move.captured_piece

    def is_valid_move(self, start, end, turn):
        """Проверяет, является ли ход допустимым.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            tuple: (bool, tuple), где:
                - bool: True, если ход допустим, иначе False.
                - tuple: Позиция съеденной шашки, если такая есть, иначе None.
        """
        x1, y1 = start
        x2, y2 = end
        piece = self.board[y1][x1]
        target = self.board[y2][x2]

        # Проверка, что игрок двигает свою шашку
        if turn == 'white' and piece != 'w':
            return False, None
        if turn == 'black' and piece != 'b':
            return False, None

        # Проверка, что целевая клетка пуста
        if target != ' ':
            return False, None

        # Проверка, что движение по диагонали
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if dx != dy:
            return False, None

        # Обычные шашки могут двигаться только вперед
        if piece == 'w' and y2 >= y1:
            return False, None
        if piece == 'b' and y2 <= y1:
            return False, None

        # Проверка на прыжок через шашку
        if dx == 2:
            jump_x = (x1 + x2) // 2
            jump_y = (y1 + y2) // 2
            jumped_piece = self.board[jump_y][jump_x]

            if jumped_piece == ' ':
                return False, None
            if (turn == 'white' and jumped_piece != 'b') or (turn == 'black' and jumped_piece != 'w'):
                return False, None

            return True, (jump_x, jump_y)  # Возвращаем True и позицию съеденной шашки

        return True, None  # Обычный ход без съедания

    def get_possible_moves(self, turn):
        """Возвращает все возможные ходы для текущего игрока.

        Аргументы:
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            list: Список возможных ходов в формате ((x1, y1), (x2, y2)).
        """
        moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if (turn == 'white' and piece == 'w') or (turn == 'black' and piece == 'b'):
                    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            if self.board[new_y][new_x] == ' ':
                                moves.append(((x, y), (new_x, new_y)))
                            elif abs(new_x - x) == 1 and abs(new_y - y) == 1:
                                jump_x, jump_y = new_x + dx, new_y + dy
                                if 0 <= jump_x < 8 and 0 <= jump_y < 8 and self.board[jump_y][jump_x] == ' ':
                                    moves.append(((x, y), (jump_x, jump_y)))
        return moves


class CheckersGame:
    """Управляет процессом игры в шашки и взаимодействием с игроками.

    Атрибуты:
        board (CheckersBoard): Объект доски для шашек.
        turn (str): Очередь хода ('white' для белых, 'black' для черных).
        history (list): Список выполненных ходов.
    """

    def __init__(self):
        """Инициализирует игру в шашки."""
        self.board = CheckersBoard()
        self.turn = 'white'
        self.history = []

    def parse_move(self, move):
        """Преобразует строку хода в координаты на доске.

        Аргументы:
            move (str): Строка, представляющая ход (например, 'e3').

        Возвращает:
            tuple: Координаты (x, y) на доске.
        """
        x = ord(move[0]) - ord('a')
        y = 8 - int(move[1])
        return x, y

    def play(self):
        """Запускает игру в шашки."""
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}")
            move = input("Введите ход (например, 'e3 f4') или 'undo' для отката: ").strip().split()

            # Обработка отмены хода
            if move[0] == 'undo':
                if not self.history:
                    print("Нет ходов для отката.")
                else:
                    last_move = self.history.pop()
                    self.board.undo_move(last_move)
                    self.turn = 'black' if self.turn == 'white' else 'white'
                continue

            # Проверка корректности ввода
            if len(move) != 2:
                print("Некорректный ввод. Попробуйте снова.")
                continue

            # Преобразование и проверка хода
            start = self.parse_move(move[0])
            end = self.parse_move(move[1])

            is_valid, captured_position = self.board.is_valid_move(start, end, self.turn)
            if not is_valid:
                print("Недопустимый ход. Попробуйте снова.")
                continue

            # Выполнение хода
            move_obj = self.board.move_piece(start, end, captured_position)
            self.history.append(move_obj)
            self.turn = 'black' if self.turn == 'white' else 'white'


if __name__ == "__main__":
    game = CheckersGame()
    game.play()