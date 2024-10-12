"""Mô-đun cung cấp thuộc tính của lớp trừu tượng và các thành viên trong nhóm"""
from abc import ABC, abstractmethod
from team import Team
class Piece(ABC):
    """Lớp đại diện cho một quân cờ"""
    # Thuộc tính

    _piece_value = None
    _piece_type = None

    # Kích thước bàn cờ
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # Kích thước cung điện
    BOUND_PALACE_X_RED = tuple((7, 9))
    BOUND_PALACE_X_BLACK = tuple((0, 2))
    BOUND_PALACE_Y = tuple((3, 5))

    # Khởi tạo
    def __init__(
        self,
        position: tuple,
        team: Team,
        board: list,
        number_of_pieces: int,
        nummber_of_team_pieces: int,
    ) -> None:
        # Khởi tạo các thuộc tính
        self.position = position
        self.team = team

        self._admissible_moves = None
        self.board = board
        self.number_of_pieces = number_of_pieces
        self.number_of_team_pieces = nummber_of_team_pieces

    def __str__(self) -> str:
        return str(self.team) + "_" + self._piece_type

    # Khởi tạo thuộc tính và các phương thức getter và setter
    @property
    def position(self) -> tuple:
        # Trả về vị trí của quân cờ
        return self._position

    @position.setter
    def position(self, new_position: tuple) -> None:
        # Kiểm tra vị trí mới có nằm trên bàn cờ không
        if self.is_position_on_board(new_position) is False:
            raise ValueError("Vị trí nằm ngoài phạm vi")

        self._position = new_position

    @property
    def admissible_moves(self) -> list:
        # Trả về danh sách các nước đi hợp lệ của quân cờ
        if self._admissible_moves is None:
            self._admissible_moves = self.get_admissible_moves()

        return self._admissible_moves

    # Instance method initialization
    def _get_piece_team_on_position(self, position: tuple) -> Team:
        # Trả về đội của quân cờ trên vị trí
        if self.is_position_on_board(position) is False:
            raise ValueError("Vị trí nằm ngoài phạm vi")

        notation = self.board[position[0]][position[1]]
        if notation == "NN":
            return Team.NONE
        else:
            return Team[self.board[position[0]][position[1]][0]]

    def is_position_teammate(self, position: tuple) -> bool:
        # Trả về True nếu quân cờ trên vị trí là đồng đội, ngược lại
        return self._get_piece_team_on_position(position) is self.team

    def is_position_free(self, position: tuple) -> bool:
        # Trả về True nếu vị trí không có quân cờ, ngược lại
        return self._get_piece_team_on_position(position) is Team.NONE

    def is_position_opponent(self, position: tuple) -> bool:
        # Trả về True nếu quân cờ trên vị trí là đối thủ, ngược lại
        return self._get_piece_team_on_position(position).value == -self.team.value

    def is_crossed_river(self) -> bool:
        # Trả về True nếu quân cờ đã vượt sông, ngược lại
        return abs(self.position[0] + 9 * (self.team.value - 1) / 2) < 5

    # Abstract method
    @abstractmethod
    def piece_value(self, value_pack=0) -> float:
        """Phương thức trừu tượng trả về giá trị của quân cờ"""
        pass

    @abstractmethod
    def get_admissible_moves(self) -> list:
        """Phương thức trừu tượng trả về danh sách các nước đi hợp lệ của quân cờ"""
        pass

    # Static method
    @staticmethod
    def is_position_on_board(position: tuple) -> bool:
        """Trả về True nếu vị trí nằm trên bàn cờ, ngược lại"""
        # Kiểm tra xem phần tử x có nằm trên bàn cờ không
        result_x = position[0] >= 0 and position[0] < Piece.BOARD_SIZE_X
        # Kiểm tra xem phần tử y có nằm trên bàn cờ không
        result_y = position[1] >= 0 and position[1] < Piece.BOARD_SIZE_Y
        return result_x and result_y

    @staticmethod
    def is_position_in_palace(position: tuple) -> bool:
        """Trả về True nếu vị trí nằm trong cung điện, ngược lại"""
        # Kiểm tra xem phần tử x có nằm trong cung điện không
        result_x = (
            position[0] >= Piece.BOUND_PALACE_X_BLACK[0]
            and position[0] <= Piece.BOUND_PALACE_X_BLACK[1]
        ) or (
            position[0] >= Piece.BOUND_PALACE_X_RED[0]
            and position[0] <= Piece.BOUND_PALACE_X_RED[1]
        )
        # Kiểm tra xem phần tử y có nằm trong cung điện không
        result_y = (
            position[1] >= Piece.BOUND_PALACE_Y[0]
            and position[1] <= Piece.BOUND_PALACE_Y[1]
        )
        return result_x and result_y

    @staticmethod
    def create_instance(
        position: tuple,
        notation: str,
        board: list,
        number_of_pieces: int,
        number_of_team_pieces: int,
    ):
        """Phương thức tạo một thể hiện của quân cờ"""
        team = Team[notation[0]]
        piece_type = notation[1]
        match piece_type:
            case "A":
                return Advisor(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "C":
                return Cannon(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "E":
                return Elephant(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "G":
                return General(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "H":
                return Horse(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "P":
                return Pawn(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "R":
                return Rook(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )

class Advisor(Piece):
    """Lớp đại diện cho quân sĩ"""
    _piece_value = 20
    _piece_type = "advisor"

    def piece_value(self, value_pack: int = 0) -> float:
        # Dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value

        # Dữ liệu gói 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoản phạt 10 điểm nếu quân sĩ không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change

        # Dữ liệu gói 2
        elif value_pack == 2:
            change = 0
            x_orient = [1, 1, -1, -1]
            y_orient = [1, -1, -1, 1]
            for cnt in range(4):
                # Vị trí mới
                pos = (
                    self.position[0] + x_orient[cnt],
                    self.position[1] + y_orient[cnt],
                )

                # Kiểm tra xem vị trí mới có nằm trên bàn cờ không và có nằm trong cung điện không
                if self.is_position_on_board(pos) and self.is_position_in_palace(pos):
                    if self.board[pos[0]][pos[1]][1] == "A":
                        change += 5

            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân sĩ
        admissible_moves = []

        # Những hướng có thể của quân cờ
        x_orient = [1, 1, -1, -1]
        y_orient = [1, -1, -1, 1]
        maximum_move_count = 4

        # Duyệt qua các hướng
        for cnt in range(maximum_move_count):
            # Vị trí mới
            pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

            # Kiểm tra xem vị trí mới có nằm trên bàn cờ không và không có quân cờ đồng đội không
            if (
                self.is_position_on_board(pos)
                and not self.is_position_teammate(pos)
                and self.is_position_in_palace(pos)
            ):
                admissible_moves.append(pos)

        # Trả về danh sách các nước đi hợp lệ
        return admissible_moves

class Cannon(Piece):
    """Lớp đại diện cho quân pháo"""
    _piece_value = 45
    _piece_type = "cannon"

    def piece_value(self, value_pack: int = 0) -> float:
        # Dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value

        # Dữ liệu gói 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoản phạt 10 điểm nếu quân pháo không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change

        # Dữ liệu gói 2
        elif value_pack == 2:
            change = 0
            # Nhận một khoản phạt hoặc thưởng 10 điểm nếu quân pháo không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change += -10
            # Nhận một khoản thưởng dựa trên số quân cờ mà quân pháo có thể ăn
            change += (self.number_of_pieces - 16) * 0.75
            # Tránh trao đổi khi thua
            change += (16 - self.number_of_team_pieces) * 0.25
            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân pháo
        admissible_moves = []

        # Những hướng có thể của quân cờ
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Duyệt qua các hướng
        for direction in range(4):
            piece_behind = 0

            # Dần dần tăng số bước
            for steps in range(1, 10):
                # Tính toán vị trí mới
                new_position = (
                    self.position[0] + steps * x_direction[direction],
                    self.position[1] + steps * y_direction[direction],
                )

                # Kiểm tra xem vị trí mới có nằm trên bàn cờ không
                if self.is_position_on_board(new_position):
                    # Kiểm tra xem có quân cờ nào ở vị trí mới không
                    if self.is_position_free(new_position) is False:
                        piece_behind += 1
                        # Kiểm tra xem quân cờ ở vị trí mới có phải là đối thủ không
                        if piece_behind == 2 and self.is_position_opponent(
                            new_position
                        ):
                            admissible_moves.append(new_position)
                            break

                    elif piece_behind == 0:
                        admissible_moves.append(new_position)

        return admissible_moves

class Rook(Piece):
    """Lớp đại diện cho quân xe"""
    _piece_value = 90
    _piece_type = "rook"

    def __init__(
        self,
        position: tuple,
        team: Team,
        board: list,
        number_of_pieces: int,
        number_of_team_pieces: int,
    ) -> None:
        super().__init__(position, team, board, number_of_pieces, number_of_team_pieces)
        self._control_pos_count = 0

    def piece_value(self, value_pack: int = 0) -> float:
        # Dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value
        # Dữ liệu gói 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoản phạt 10 điểm nếu quân xe không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change = -10
            else:
                # Nhận một khoản thưởng dựa trên số vị trí mà quân xe kiểm soát
                change = self._control_pos_count * 0.5
            return self._piece_value + change
        # Dữ liệu gói 2
        elif value_pack == 2:
            change = 0
            # Nhận một khoản phạt 10 điểm nếu quân xe không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change += -10
            # Nhận một khoản thưởng dựa trên số vị trí mà quân xe kiểm soát
            else:
                change += self._control_pos_count * 0.5
            # Nhận một khoản thưởng dựa trên giai đoạn của trò chơi và xem quân xe đã vượt sông chưa
            change += (16 - self.number_of_team_pieces) * 0.25
            # Nhận một khoản thưởng dựa trên vị trí của quân xe
            change += (32 - self.number_of_pieces) * int(self.is_crossed_river())
            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân xe
        admissible_moves = []

        # Những hướng có thể của quân cờ
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Duyệt qua các hướng
        for direction in range(4):
            # Dần dần tăng số bước
            for steps in range(1, 10):
                # Tính toán vị trí mới
                new_position = (
                    self.position[0] + steps * x_direction[direction],
                    self.position[1] + steps * y_direction[direction],
                )
                # Kiểm tra xem vị trí mới có nằm trên bàn cờ không
                if self.is_position_on_board(new_position):
                    # Kiểm tra xem có quân cờ nào ở vị trí mới không
                    if self.is_position_free(new_position) is False:
                        # Kiểm tra xem quân cờ ở vị trí mới có phải là đối thủ không
                        if self.is_position_opponent(new_position):
                            admissible_moves.append(new_position)
                        break
                    else:
                        self._control_pos_count = self._control_pos_count + 1
                    admissible_moves.append(new_position)

        return admissible_moves

class Elephant(Piece):
    """Lớp đại diện cho quân tượng"""

    _piece_value = 25
    _piece_type = "elephant"

    def _cross_river(self, position: tuple) -> bool:
        # Trả về True nếu quân tượng đã vượt sông, ngược lại
        if self.team is Team.RED and position[0] < 5:
            return True
        if self.team is Team.BLACK and position[0] > 4:
            return True
        return False

    def piece_value(self, value_pack: int = 0) -> float:
        # Gói dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value
        # Gói dữ liệu 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoản phạt 10 điểm nếu quân tượng không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change
        # Gói dữ liệu 2
        elif value_pack == 2:
            change = 0
            # Các hướng có thể
            x_direction = [2, 2, -2, -2]
            y_direction = [2, -2, 2, -2]
            # Các vị trí chặn
            x_block = [1, 1, -1, -1]
            y_block = [1, -1, 1, -1]

            for direction in range(4):
                new_pos = (
                    self.position[0] + x_direction[direction],
                    self.position[1] + y_direction[direction],
                )
                block_pos = (
                    self.position[0] + x_block[direction],
                    self.position[1] + y_block[direction],
                )
                # Kiểm tra xem tất cả các điều kiện dưới đây có được thỏa mã
                if (
                    self.is_position_on_board(new_pos)
                    and self.is_position_free(block_pos)
                    and not self._cross_river(new_pos)
                ):
                    # Kiểm tra xem quân cờ ở vị trí mới có phải là đối thủ không
                    if self.board[new_pos[0]][new_pos[1]][1] == "E":
                        change += 5
                        break
            return self._piece_value + change
        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân tượng
        admissible_moves = []
        # Các hướng có thể
        x_direction = [2, 2, -2, -2]
        y_direction = [2, -2, 2, -2]
        maximum_move_count = 4
        # Các vị trí chặn
        x_block = [1, 1, -1, -1]
        y_block = [1, -1, 1, -1]
        # Duyệt qua các hướng
        for direction in range(maximum_move_count):
            new_pos = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            block_pos = (
                self.position[0] + x_block[direction],
                self.position[1] + y_block[direction],
            )
            # Kiểm tra xem tất cả các điều kiện dưới đây có được thỏa mã
            if (
                self.is_position_on_board(new_pos)
                and self.is_position_free(block_pos)
                and not self._cross_river(new_pos)
                and not self.is_position_teammate(new_pos)
            ):
                admissible_moves.append(new_pos)

        return admissible_moves

class Pawn(Piece):
    """Lớp đại diện cho quân tốt"""
    _piece_value = 10
    _piece_type = "pawn"

    def piece_value(self, value_pack=0) -> float:
        # Gói dữ liệu mặc định
        if value_pack == 0:
            if self.is_crossed_river() is True:
                self._piece_value = 20
            return self._piece_value
        # Gói dữ liệu 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoản thưởng dựa trên vị trí của quân tốt
            if self.team is Team.BLACK:
                if self.position == (3, 4):
                    change = 20
                elif self.position[0] == 5 or self.position[0] == 6:
                    change = 10
                elif self.position[0] == 7 or self.position[0] == 8:
                    if self.position[1] < 7 and self.position[1] > 1:
                        change = 20
                    else:
                        change = 10
            if self.team is Team.RED:
                if self.position == (6, 4):
                    change = 20
                elif self.position[0] == 3 or self.position[0] == 4:
                    change = 10
                elif self.position[0] == 1 or self.position[0] == 2:
                    if self.position[1] < 7 and self.position[1] > 1:
                        change = 20
                    else:
                        change = 10
            return self._piece_value + change

        # Gói dữ liệu 2
        elif value_pack == 2:
            change = 0
            # Nhận một khoản thưởng dựa trên vị trí của quân tốt
            if self.team is Team.BLACK:
                if self.position == (3, 4):
                    change += 20 - (32 - self.number_of_pieces) * 2
                elif self.position[0] in range(7, 9) and self.position[1] in range(2, 7):
                    change += 20
                elif self.position[0] in range(6, 9) and self.position[1] in range(1, 8):
                    change += 15
                elif self.is_crossed_river():
                    if self.position[0] == 9:
                        change += 0
                    else:
                        change += 10
            if self.team is Team.RED:
                if self.position == (6, 4):
                    change += 20 - (32 - self.number_of_pieces) * 2
                elif self.position[0] in range(1, 3) and self.position[1] in range(2, 7):
                    change += 20
                elif self.position[0] in range(1, 4) and self.position[1] in range(1, 8):
                    change += 15
                elif self.is_crossed_river():
                    if self.position[0] == 0:
                        change += 0
                    else:
                        change += 10
            # Nhận một khoản thưởng dựa trên số quân cờ mà quân tốt có thể ăn
            change += (16 - self.number_of_team_pieces) * 2
            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    # Searching admissible moves for the pawn
    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân tốt
        admissible_moves = []

        # Kiểm tra vị trí mới
        new_pos = (self.position[0] - self.team.value, self.position[1])
        if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
            admissible_moves.append(new_pos)

        if self.is_crossed_river() is True:
            new_pos = (self.position[0], self.position[1] + 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                admissible_moves.append(new_pos)

            new_pos = (self.position[0], self.position[1] - 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                admissible_moves.append(new_pos)

        return admissible_moves

class Horse(Piece):
    """Lớp đại diện cho quân mã"""
    _piece_value = 40
    _piece_type = "horse"

    def piece_value(self, value_pack: int = 0) -> float:
        # Gói dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value

        # Gói dữ liệu 1
        elif value_pack == 1:
            change = 0
            # Nhận một khoảng phạt hoặc thưởng dựa trên số nước đi hợp lệ mà quân mã có
            if len(self.admissible_moves) == 0 or len(self.admissible_moves) == 1:
                change += -10
            elif len(self.admissible_moves) == 2:
                change += -5
            elif len(self.admissible_moves) == 5 or len(self.admissible_moves) == 6:
                change += 5
            elif len(self.admissible_moves) == 7 or len(self.admissible_moves) == 8:
                change += 10
            if self.team is Team.BLACK and self.position == (1, 4):
                change += -25
            elif self.team is Team.RED and self.position == (8, 4):
                change += -25
            return self._piece_value + change

        # Gói dữ liệu 2
        elif value_pack == 2:
            change = 0
            # Nhận một khoản phạt hoặc thưởng dựa trên số nước đi hợp lệ mà quân mã có
            if len(self.admissible_moves) == 0 or len(self.admissible_moves) == 1:
                change += -5
            elif len(self.admissible_moves) == 2:
                change += -2.5
            elif len(self.admissible_moves) == 5 or len(self.admissible_moves) == 6:
                change += 2.5
            elif len(self.admissible_moves) == 7 or len(self.admissible_moves) == 8:
                change += 5

            # Nhận một khoản thưởng dựa trên số quân cờ mà quân mã có thể ăn
            change += (22 - self.number_of_pieces) * 0.75

            palace_pos = None
            if self.team is Team.RED:
                palace_pos = (1, 4)
            else:
                palace_pos = (8, 4)
            change += ((32 - self.number_of_pieces) * 0.15 *
                       (5 - (abs(palace_pos[0] - self.position[0]) + abs(palace_pos[1] - self.position[1]))))

            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân mã
        admissible_moves = []

        # Các hướng đích đến
        x_orient = [2, 2, 1, -1, -2, -2, -1, 1]
        y_orient = [1, -1, -2, -2, -1, 1, 2, 2]
        maximum_move_count = 8

        # Các hướng của quân mã
        p_orient = [1, 0, -1, 0]
        q_orient = [0, -1, 0, 1]

        for cnt in range(maximum_move_count):
            # Vị trí con mã bị chặn
            pos = (
                self.position[0] + p_orient[cnt // 2],
                self.position[1] + q_orient[cnt // 2],
            )

            # Kiểm tra xem con mã có bị chặn không
            if self.is_position_on_board(pos) and self.is_position_free(pos):
                # Goal position
                pos = (
                    self.position[0] + x_orient[cnt],
                    self.position[1] + y_orient[cnt],
                )

                # Kiểm tra xem vị trí mới có nằm trên bàn cờ không
                if self.is_position_on_board(pos) and not self.is_position_teammate(pos):
                    admissible_moves.append(pos)

        return admissible_moves

class General(Piece):
    """Lớp đại diện cho quân tướng"""
    _piece_value = 0
    _piece_type = "general"

    def piece_value(self, value_pack: int = 0) -> float:
        # Gói dữ liệu mặc định
        if value_pack == 0:
            return self._piece_value

        # Gói dữ liệu 1
        elif value_pack == 1:
            return self._piece_value

        # Gói dữ liệu 2
        elif value_pack == 2:
            opponent = Team.NONE
            if self.team is Team.RED:
                opponent = Team.BLACK
            else:
                opponent = Team.RED
            change = 0
            # Nhận một khoản phạt 10 điểm nếu tướng không có nước đi hợp lệ
            if len(self.admissible_moves) == 0:
                change += -10
            # Nhận một khoản phạt 15 điểm nếu tướng bị đối thủ ăn
            if General.is_general_exposed(self.board, self.team, opponent) is True:
                change += -15

            return self._piece_value + change

        # Nếu gói dữ liệu không tồn tại
        else:
            raise ValueError("Không tìm thấy gói giá trị")

    def get_admissible_moves(self) -> list:
        # Tạo một danh sách các nước đi hợp lệ cho quân tướng
        admissible_moves = []

        # Xác định hướng di chuyển
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Duyệt qua các hướng
        for direction in range(4):
            # Tính toán vị trí mới
            new_position = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            # Kiểm tra xem vị trí mới có nằm trên cung điện không
            if self.is_position_in_palace(new_position):
                # Kiểm tra xem vị trí mới có nằm trên bàn cờ không
                if self.is_position_free(new_position):
                    admissible_moves.append(new_position)

                # Kiểm tra xem vị trí mới có phải là quân cờ đối thủ không
                elif self.is_position_opponent(new_position):
                    admissible_moves.append(new_position)

        return admissible_moves

    @staticmethod
    def is_general_exposed(board: list, current_team: Team, opponent: Team) -> bool:
        """ Phương thức kiểm tra xem tướng có bị lộ mặt tướng không """
        # Tìm vị trí của tướng
        cur_general_pos = None

        for y in range(Piece.BOUND_PALACE_Y[0], Piece.BOUND_PALACE_Y[1] + 1):
            # Tìm vị trí của tướng theo hướng x
            bound_x = None
            if current_team is Team.RED:
                bound_x = Piece.BOUND_PALACE_X_RED
            elif current_team is Team.BLACK:
                bound_x = Piece.BOUND_PALACE_X_BLACK

            # Tìm vị trí của tướng
            for x in range(bound_x[0], bound_x[1] + 1):
                if board[x][y][1] == "G":
                    cur_general_pos = (x, y)

        # Chiếu tướng nếu như tướng bị lộ mặt tướng
        # Các hướng có thể của pháo, tốt, xe
        x_str_dir, y_str_dir = [0, 0, -1, 1], [1, -1, 0, 0]

        # Các hướng có thể của quân mã
        x_horse_offset = [2, 1, -1, -2, -2, -1, 1, 2]
        y_horse_offset = [-1, -2, -2, -1, 1, 2, 2, 1]
        x_orient, y_orient = [1, -1, -1, 1], [-1, -1, 1, 1]

        # Chiếu bằng xe
        for direction in range(4):
            for steps in range(1, 10):
                # Tính toán vị trí kiểm tra
                check_pos = (
                    cur_general_pos[0] + steps * x_str_dir[direction],
                    cur_general_pos[1] + steps * y_str_dir[direction],
                )
                # Nếu vị trí kiểm tra ra khỏi bàn cờ thì thoát voòng lặp
                if Piece.is_position_on_board(check_pos) is False:
                    break

                notation = board[check_pos[0]][check_pos[1]]
                # Nếu quân xe và tướng cùng một đội thì thoát voòng lặp
                if Team[notation[0]] is not Team.NONE:
                    # Nếu quân xe và tướng cùng khác đội thì trả về True
                    if Team[notation[0]] is opponent and notation[1] == "R":
                        return True
                    # Nếu không, thoát vòng lặp
                    else:
                        break

        # Chiếu bằng mã
        for index in range(8):
            check_pos = (
                cur_general_pos[0] + x_horse_offset[index],
                cur_general_pos[1] + y_horse_offset[index],
            )
            # Nếu vị trí kiểm tra ra khỏi bàn cờ thì thoát vòng lặp
            if Piece.is_position_on_board(check_pos) is False:
                continue

            notation = board[check_pos[0]][check_pos[1]]
            # Nếu quân mã và tướng khác đội thì trả về True
            if Team[notation[0]] is opponent and notation[1] == "H":
                mid_pos = (
                    cur_general_pos[0] + x_orient[index // 2],
                    cur_general_pos[1] + y_orient[index // 2],
                )
                mid_pos_notation = board[mid_pos[0]][mid_pos[1]]
                if mid_pos_notation == "NN":
                    return True

        # Chiếu bằng pháo
        for direction in range(4):
            piece_behind = 0
            for steps in range(1, 10):
                pos = (
                    cur_general_pos[0] + steps * x_str_dir[direction],
                    cur_general_pos[1] + steps * y_str_dir[direction],
                )
                # Nếu vị trí kiểm tra ra khỏi bàn cờ thì thoát vòng lặp
                if Piece.is_position_on_board(pos) is False:
                    break

                notation = board[pos[0]][pos[1]]
                # Nếu quân pháo đứng sau 1 quân khác và tướng nằm trong vị trí chiếu thì trả về True
                if (
                    piece_behind == 1
                    and Team[notation[0]] is opponent
                    and notation[1] == "C"
                ):
                    return True
                # Kiểm tra xem quân pháo có đứng sau 1 quân khác không
                if notation != "NN":
                    piece_behind += 1
                # Nếu như có 2 quân đứng trước quân pháo thì thoát vòng lặp
                if piece_behind > 1:
                    break

        # Chiếu bằng tốt
        # Kiểm tra tốt ở 2 hướng trái và phải
        for index in range(2):
            check_pos = (
                cur_general_pos[0] + x_str_dir[index],
                cur_general_pos[1] + y_str_dir[index],
            )
            notation = board[check_pos[0]][check_pos[1]]
            # Nếu như tốt và tướng ở vị trí chiếu thì trả về True
            if Team[notation[0]] is opponent and notation[1] == "P":
                return True
        # Kiểm tra phía trước tốt
        forward_notation = board[cur_general_pos[0] + opponent.value][cur_general_pos[1]]
        if Team[forward_notation[0]] is opponent and forward_notation[1] == "P":
            return True

        # Chiếu bằng tướng
        for steps in range(1, 10):
            pos = (cur_general_pos[0] + steps * opponent.value, cur_general_pos[1])
            # Nếu vị trí kiểm tra ra khỏi bàn cờ thì thoát vòng lặp
            if Piece.is_position_on_board(pos) is False:
                break

            notation = board[pos[0]][pos[1]]
            if notation == "NN":
                continue
            # Nếu như tướng và tướng đối phương ở vị trí chiếu thì trả về True
            if notation[1] == "G":
                return True
            # Nếu không, thoát vòng lặp
            else:
                break

        # Nếu như các trường hợp trên không xảy ra thì trả về False
        return False
