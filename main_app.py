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


class Wizard:
    """Фигура Волшебник."""

    def __init__(self, color):
        self.color = color

    def get_symbol(self):
        return 'W' if self.color == 'white' else 'w'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        target = board[y2][x2]

        #Волшебник может перемещаться на одну клетку в любом направлении
        if dx <= 1 and dy <= 1:
            return True

        #Волшебник может телепортироваться на любую свободную клетку
        if target == ' ':
            return True

        return False


class Hunter:
    """Фигура Ловец."""

    def __init__(self, color):
        self.color = color

    def get_symbol(self):
        return 'H' if self.color == 'white' else 'h'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        #Ловец может перемещаться на две клетки по горизонтали или вертикали
        if (dx == 2 and dy == 0) or (dx == 0 and dy == 2):
            return True

        return False


class Archer:
    """Фигура Стрелок."""

    def __init__(self, color):
        self.color = color

    def get_symbol(self):
        return 'A' if self.color == 'white' else 'a'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        #Стрелок может стрелять на три клетки по горизонтали или вертикали
        if (dx == 3 and dy == 0) or (dx == 0 and dy == 3):
            target = board[y2][x2]
            if target != ' ' and target.islower() != self.color == 'white':
                return True

        return False


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
        #Добавляем новые фигуры
        self.board[0][2] = 'w'  #Черный волшебник
        self.board[7][2] = 'W'  #Белый волшебник
        self.board[0][5] = 'h'  #Черный ловец
        self.board[7][5] = 'H'  #Белый ловец
        self.board[0][3] = 'a'  #Черный стрелок
        self.board[7][3] = 'A'  #Белый стрелок

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

        #Проверка, что игрок двигает свою фигуру
        if turn == 'white' and piece.islower():
            return False
        if turn == 'black' and piece.isupper():
            return False

        #Проверка, что игрок не бьет свою фигуру
        if target != ' ' and ((turn == 'white' and target.isupper()) or (turn == 'black' and target.islower())):
            return False

        #Проверка допустимости хода для новых фигур
        if piece.lower() == 'w':
            wizard = Wizard('white' if piece.isupper() else 'black')
            return wizard.is_valid_move(start, end, self.board)
        elif piece.lower() == 'h':
            hunter = Hunter('white' if piece.isupper() else 'black')
            return hunter.is_valid_move(start, end, self.board)
        elif piece.lower() == 'a':
            archer = Archer('white' if piece.isupper() else 'black')
            return archer.is_valid_move(start, end, self.board)

        #Стандартные правила для остальных фигур
        return True

    def get_available_moves(self, start, turn):
        """Возвращает список доступных ходов для выбранной фигуры.

        Аргументы:
            start (tuple): Начальная позиция фигуры в виде координат (x, y).
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            list: Список доступных ходов в виде координат (x, y).
        """
        x1, y1 = start
        piece = self.board[y1][x1]
        available_moves = []

        #Проверка, что игрок двигает свою фигуру
        if turn == 'white' and piece.islower():
            return available_moves
        if turn == 'black' and piece.isupper():
            return available_moves

        #Перебор всех клеток на доске
        for y2 in range(8):
            for x2 in range(8):
                end = (x2, y2)
                if self.is_valid_move(start, end, turn):
                    available_moves.append(end)

        return available_moves

    def is_under_attack(self, position, turn):
        """Проверяет, находится ли клетка под атакой фигур противника.

        Аргументы:
            position (tuple): Координаты клетки (x, y).
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            bool: True, если клетка под атакой, иначе False.
        """
        x, y = position
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != ' ' and ((turn == 'white' and piece.islower()) or (turn == 'black' and piece.isupper())):
                    if self.is_valid_move((j, i), (x, y), 'black' if turn == 'white' else 'white'):
                        return True
        return False

    def get_threatened_pieces(self, turn):
        """Возвращает список фигур, находящихся под угрозой.

        Аргументы:
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            list: Список координат фигур, находящихся под угрозой.
        """
        threatened_pieces = []
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece != ' ' and ((turn == 'white' and piece.isupper()) or (turn == 'black' and piece.islower())):
                    if self.is_under_attack((x, y), turn):
                        threatened_pieces.append((x, y))
        return threatened_pieces

    def is_in_check(self, turn):
        """Проверяет, находится ли король под шахом.

        Аргументы:
            turn (str): Очередь хода ('white' для белых, 'black' для черных).

        Возвращает:
            bool: True, если король под шахом, иначе False.
        """
        king_symbol = 'K' if turn == 'white' else 'k'
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == king_symbol:
                    return self.is_under_attack((x, y), turn)
        return False


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

    def show_available_moves(self, start):
        """Отображает доступные ходы для выбранной фигуры.

        Аргументы:
            start (tuple): Начальная позиция фигуры в виде координат (x, y).
        """
        available_moves = self.board.get_available_moves(start, self.turn)
        temp_board = [row.copy() for row in self.board.board]

        #Отметка доступных ходов на временной доске
        for x, y in available_moves:
            if temp_board[y][x] == ' ':
                temp_board[y][x] = '*'
            else:
                temp_board[y][x] = temp_board[y][x].upper()  # Подсветка фигур, которые можно взять

        #Отображение временной доски
        print("  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=" ")
            for j in range(8):
                print(temp_board[i][j], end=" ")
            print(8 - i)
        print("  a b c d e f g h")

    def show_threatened_pieces(self):
        """Отображает фигуры, находящиеся под угрозой, и проверяет наличие шаха."""
        threatened_pieces = self.board.get_threatened_pieces(self.turn)
        in_check = self.board.is_in_check(self.turn)

        temp_board = [row.copy() for row in self.board.board]

        #Отметка угрожаемых фигур на временной доске
        for x, y in threatened_pieces:
            temp_board[y][x] = temp_board[y][x].upper()  # Подсветка фигур, находящихся под угрозой

        #Отображение временной доски
        print("  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=" ")
            for j in range(8):
                print(temp_board[i][j], end=" ")
            print(8 - i)
        print("  a b c d e f g h")

        #Вывод информации о шахе
        if in_check:
            print(f"Король {'белых' if self.turn == 'white' else 'черных'} под шахом!")

    def play(self):
        """Запускает шахматную игру."""
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}")
            move = input("Введите ход (например, 'e2 e4'), 'undo' для отката, 'hint' для подсказки или 'threat' для угроз: ").strip().split()

            #Обработка отмены хода
            if move[0] == 'undo':
                if not self.history:
                    print("Нет ходов для отката.")
                else:
                    last_move = self.history.pop()
                    self.board.undo_move(last_move)
                    self.turn = 'black' if self.turn == 'white' else 'white'
                continue

            #Обработка подсказки
            if move[0] == 'hint':
                if len(move) != 2:
                    print("Некорректный ввод. Введите, например, 'hint e2'.")
                    continue
                start = self.parse_move(move[1])
                self.show_available_moves(start)
                continue

            #Обработка показа угроз
            if move[0] == 'threat':
                self.show_threatened_pieces()
                continue

            #Проверка корректности ввода
            if len(move) != 2:
                print("Некорректный ввод. Попробуйте снова.")
                continue

            #Преобразование и проверка хода
            start = self.parse_move(move[0])
            end = self.parse_move(move[1])

            if not self.board.is_valid_move(start, end, self.turn):
                print("Недопустимый ход. Попробуйте снова.")
                continue

            #Выполнение хода
            move_obj = self.board.move_piece(start, end)
            self.history.append(move_obj)
            self.turn = 'black' if self.turn == 'white' else 'white'


if __name__ == "__main__":
    game = ChessGame()
    game.play()
