from cmath import inf
from random import shuffle
from piece import General, Piece
from team import Team

class GameState:
    """Lớp này đại diện cho trạng thái của trò chơi, chứa thông tin và các phương thức xử lý"""

    # Kích thước bàn cờ
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9
    # Giới hạn cho các nước đi lặp lại
    MAX_PERPETUAL = 3

    def __init__(
        self,
        board: list,
        current_team: Team,
        move_history: dict,
        value_pack: int = 0,
        number_of_red_pieces: int = 16,
        number_of_black_pieces: int = 16,
    ) -> None:
        self.board = board
        self.move_history = move_history
        self.number_of_red_pieces = number_of_red_pieces
        self.number_of_black_pieces = number_of_black_pieces

        self._value_pack = value_pack
        self._value = None
        self._current_team = current_team
        self._all_child_gamestates = None

    # Khởi tạo thuộc tính
    @property
    def value(self) -> float:
        """Hàm Getter của thuộc tính value, trả về giá trị của trạng thái game dựa trên giá trị của các quân cờ"""

        if self._value is None:
            self._value = self._get_game_state_value()

        return self._value

    @property
    def all_child_gamestates(self) -> list:
        """Hàm Getter của danh sách các trạng thái con của trò chơi"""

        if self._all_child_gamestates is None:
            self._all_child_gamestates = self.generate_all_game_states()

        return self._all_child_gamestates

    # Phương thức thể hiện
    def _get_game_state_value(self) -> float:
        """Trả về giá trị đánh giá của bàn cờ"""
        # Trả về giá trị của trạng thái trò chơi khi một đội thắng
        if self.get_team_win() is Team.RED:
            return inf

        if self.get_team_win() is Team.BLACK:
            return -inf

        current_value = 0
        # Lặp qua tất cả các vị trí trên bàn cờ
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                # Lấy ký hiệu của vị trí
                notation = self.board[i][j]
                # Nếu ký hiệu trống, bỏ qua
                if notation == "NN":
                    continue

                # Tạo một thể hiện của quân cờ và lấy giá trị của nó
                piece = Piece.create_instance(
                    (i, j),
                    notation,
                    self.board,
                    self.number_of_black_pieces + self.number_of_red_pieces,
                    self._get_number_of_team_pieces(Team[notation[0]]),
                )
                current_value += piece.piece_value(self._value_pack) * piece.team.value

        return current_value

    def _get_the_opponent_team(self) -> Team:
        """Phương thức trả về đội đối thủ trong trạng thái trò chơi"""
        if self._current_team is Team.BLACK:
            return Team.RED
        else:
            return Team.BLACK

    def _get_number_of_team_pieces(self, team) -> int:
        """Phương thức trả về số quân cờ của một đội"""
        if team is Team.BLACK:
            return self.number_of_black_pieces
        else:
            return self.number_of_red_pieces

    def generate_game_state_with_move(self, old_pos: tuple, new_pos: tuple):
        """Phương thức tạo ra một trạng thái trò chơi mới với nước đi (trả về None nếu nước đi không hợp lệ)"""
        # Tạm thời di chuyển quân cờ
        old_pos_notation = self.board[old_pos[0]][old_pos[1]]
        new_pos_notation = self.board[new_pos[0]][new_pos[1]]

        self.board[old_pos[0]][old_pos[1]] = "NN"
        self.board[new_pos[0]][new_pos[1]] = old_pos_notation

        # Lấy đội đối thủ
        opponent = self._get_the_opponent_team()

        # Kiểm tra nếu trạng thái trò chơi hợp lệ
        def _return_to_old_state():
            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
            self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # Kiểm tra nước đi lặp lại
        hash_code = self.hash_board(self.board)
        if self.move_history.get(hash_code, 0) + 1 == self.MAX_PERPETUAL:
            _return_to_old_state()
            return None

        # Nếu kiểm tra không hợp lệ, trả về None
        if General.is_general_exposed(self.board, self._current_team, opponent) is True:
            _return_to_old_state()
            return None

        # Tạo bản sao của bàn cờ đã di chuyển và trả lại bàn cờ về trạng thái cũ
        new_board = list(map(list, self.board))
        new_move_history = dict(self.move_history)
        new_move_history[hash_code] = new_move_history.get(hash_code, 0) + 1
        _return_to_old_state()

        # Tính số lượng quân cờ của trạng thái mới
        new_number_of_red_pieces = self.number_of_red_pieces
        new_number_of_black_pieces = self.number_of_black_pieces
        if self.board[new_pos[0]][new_pos[1]] != "NN":
            if self._current_team is Team.RED:
                new_number_of_black_pieces -= 1
            else:
                new_number_of_red_pieces -= 1

        return GameState(
            new_board,
            opponent,
            new_move_history,
            self._value_pack,
            new_number_of_red_pieces,
            new_number_of_black_pieces,
        ), (old_pos, new_pos)

    def generate_random_game_state(self):
        """Phương thức tạo ra trạng thái trò chơi ngẫu nhiên từ nước đi của quân cờ hiện tại"""
        # Đặt tất cả các vị trí của quân cờ của đội hiện tại vào danh sách và xáo trộn nó
        team_positions = list()
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                if Team[notation[0]] is self._current_team:
                    team_positions.append((i, j))

        shuffle(team_positions)

        # Lặp qua tất cả các quân cờ trong danh sách, tạo danh sách nước đi của quân cờ và xáo trộn
        for pos in team_positions:
            notation = self.board[pos[0]][pos[1]]
            moves_list = Piece.create_instance(
                pos,
                notation,
                self.board,
                self.number_of_black_pieces + self.number_of_red_pieces,
                self._get_number_of_team_pieces(Team[notation[0]]),
            ).admissible_moves
            shuffle(moves_list)

            for new_pos in moves_list:
                new_gamestate = self.generate_game_state_with_move(pos, new_pos)
                if new_gamestate is not None:
                    return new_gamestate

        # Nếu trạng thái trò chơi đã kết thúc, trả về None
        return None

    def generate_all_game_states(self) -> list:
        """Phương thức trả về danh sách tất cả các trạng thái có thể truy cập được từ trạng thái hiện tại bằng một nước đi"""

        # Tạo danh sách theo dõi tất cả các trạng thái trò chơi có thể được tạo ra
        game_states_available = list()

        # Lặp qua tất cả các nước đi
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                # Nếu vị trí trống, bỏ qua
                if notation == "NN":
                    continue

                # Nếu quân cờ của đội hiện tại ở vị trí đó,
                # thì tạo một thể hiện và lấy danh sách các nước đi hợp lệ
                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j),
                        notation,
                        self.board,
                        self.number_of_black_pieces + self.number_of_red_pieces,
                        self._get_number_of_team_pieces(Team[notation[0]]),
                    ).admissible_moves

                    # Lặp qua tất cả các nước đi trong danh sách nước đi
                    for new_pos in moves_list:
                        # Tạo trạng thái trò chơi mới với nước đi đó
                        game_state = self.generate_game_state_with_move((i, j), new_pos)

                        # Nếu trạng thái trò chơi hợp lệ, thêm nó vào đầu danh sách
                        if game_state is not None:
                            game_states_available.append(game_state)

        return game_states_available

    def get_team_win(self):
        """Phương thức trả về đội chiến thắng, nếu có"""

        generals_pos = dict()

        # Lặp qua tất cả các vị trí trên bàn cờ
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                # Tìm vị trí của hai tướng (General)
                if self.board[i][j][1] == "G":
                    generals_pos[Team[self.board[i][j][0]]] = (i, j)

        # Nếu tướng đen không tồn tại, đội đỏ thắng
        if Team.BLACK not in generals_pos:
            return Team.RED

        # Nếu tướng đỏ không tồn tại, đội đen thắng
        if Team.RED not in generals_pos:
            return Team.BLACK

        return None
    @staticmethod
    def hash_board(self, board: list) -> str:
        """Phương thức trả về mã hash của bàn cờ"""
        return "".join([str(piece) for row in board for piece in row])

    @classmethod
    def generate_initial_game_state(cls, value_pack: int = 0):
        """Phương thức tạo ra trạng thái trò chơi ban đầu"""
        initial_board = list(
            [
                ["BR", "BH", "BE", "BA", "BG", "BA", "BE", "BH", "BR"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["NN", "BC", "NN", "NN", "NN", "NN", "NN", "BC", "NN"],
                ["BP", "NN", "BP", "NN", "BP", "NN", "BP", "NN", "BP"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["RP", "NN", "RP", "NN", "RP", "NN", "RP", "NN", "RP"],
                ["NN", "RC", "NN", "NN", "NN", "NN", "NN", "RC", "NN"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["RR", "RH", "RE", "RA", "RG", "RA", "RE", "RH", "RR"],
            ]
        )
        initial_move_history = dict()
        hash_code = GameState.hash_board(initial_board)
        initial_move_history[hash_code] = 1
        return GameState(initial_board, Team.RED, initial_move_history, value_pack)
