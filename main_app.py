"""Простая реализация шахматной игры с проверкой ходов и функцией отмены.

Этот модуль содержит классы для представления шахматной игры, включая доску, ходы
и состояние игры. Он позволяет двум игрокам играть в шахматы в консоли с поддержкой
отмены ходов.

Классы:
    Move: Представляет ход в игре.
    ChessBoard: Представляет шахматную доску и управляет перемещением фигур.
    ChessGame: Управляет процессом игры и взаимодействием с игроками.
"""


class Move:
    """Представляет ход в шахматной игре.

    Атрибуты:
        start (tuple): Начальная позиция хода в виде координат (x, y).
        end (tuple): Конечная позиция хода в виде координат (x, y).
        piece (str): Фигура, которая перемещается.
        captured_piece (str): Фигура, которая была взята, если такая есть.
    """

    def __init__(self, start, end, piece, captured_piece):
        """Инициализирует экземпляр Move.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).
            piece (str): Фигура, которая перемещается.
            captured_piece (str): Фигура, которая была взята, если такая есть.
        """
        self.start = start
        self.end = end
        self.piece = piece
        self.captured_piece = captured_piece


class ChessBoard:
    """Представляет шахматную доску и управляет перемещением фигур.

    Атрибуты:
        board (list): Двумерный список, представляющий шахматную доску.
    """

    def __init__(self):
        """Инициализирует шахматную доску стандартной начальной расстановкой."""
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def display(self):
        """Отображает текущее состояние шахматной доски."""
        print("  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print(8 - i)
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        """Перемещает фигуру на доске.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).

        Возвращает:
            Move: Объект Move, представляющий выполненный ход.
        """
        x1, y1 = start
        x2, y2 = end
        piece = self.board[y1][x1]
        captured_piece = self.board[y2][x2]
        self.board[y2][x2] = piece
        self.board[y1][x1] = ' '
        return Move(start, end, piece, captured_piece)

    def undo_move(self, move):
        """Отменяет ход на доске.

        Аргументы:
            move (Move): Объект Move, представляющий ход, который нужно отменить.
        """
        start, end = move.start, move.end
        x1, y1 = start
        x2, y2 = end
        self.board[y1][x1] = move.piece
        self.board[y2][x2] = move.captured_piece

    def is_valid_move(self, start, end, turn):
        """Проверяет, является ли ход допустимым.

        Аргументы:
            start (tuple): Начальная позиция хода в виде координат (x, y).
            end (tuple): Конечная позиция хода в виде координат (x, y).
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        piece = self.board[y1][x1]
        target = self.board[y2][x2]

        # Проверка, что игрок двигает свою фигуру
        if turn == 'white' and piece.islower():
            return False
        if turn == 'black' and piece.isupper():
            return False

        # Проверка, что игрок не бьет свою фигуру
        if target != ' ' and ((turn == 'white' and target.isupper()) or (turn == 'black' and target.islower())):
            return False

        return True


class ChessGame:
    """Управляет процессом шахматной игры и взаимодействием с игроками.

    Атрибуты:
        board (ChessBoard): Объект шахматной доски.
        turn (str): Очередь хода ('white' для белых, 'black' для черных).
        history (list): Список выполненных ходов.
    """

    def __init__(self):
        """Инициализирует шахматную игру."""
        self.board = ChessBoard()
        self.turn = 'white'
        self.history = []

    def parse_move(self, move):
        """Преобразует строку хода в координаты на доске.

        Аргументы:
            move (str): Строка, представляющая ход (например, 'e2').

        Возвращает:
            tuple: Координаты (x, y) на доске.
        """
        x = ord(move[0]) - ord('a')
        y = 8 - int(move[1])
        return x, y

    def play(self):
        """Запускает шахматную игру."""
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}")
            move = input("Введите ход (например, 'e2 e4') или 'undo' для отката: ").strip().split()

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

            if not self.board.is_valid_move(start, end, self.turn):
                print("Недопустимый ход. Попробуйте снова.")
                continue

            # Выполнение хода
            move_obj = self.board.move_piece(start, end)
            self.history.append(move_obj)
            self.turn = 'black' if self.turn == 'white' else 'white'


if __name__ == "__main__":
    game = ChessGame()
    game.play()