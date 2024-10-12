"""Mô-đun dùng để tạo lớp GameTree và các lớp con của nó"""
from abc import ABC
from cmath import inf
from time import time

from team import Team
from node import Node, NodeMinimax
from game_state import GameState

class GameTree(ABC):
    """Lớp này chịu trách nhiệm về việc biểu diễn cây trò chơi"""
    # Khởi tạo hằng số
    MAX_NODE = inf

    # Bắt đầu khởi tạo ban đầu
    def __init__(self, team: Team, value_pack: int = 0) -> None:
        # Phương thức này tạo cây trò chơi ban đầu
        self.team = team
        self.current_node = self._create_node(
            GameState.generate_initial_game_state(value_pack), None, None
        )
        self._value_pack = value_pack
        self.count = 0

    # Bắt đầu phương thức
    # Phương thức cơ bản
    def move_to_best_child(self) ->tuple:
        """Phương thức này di chuyển nút hiện tại tới "con tốt nhất" của nó trên cây trò chơi"""
        self.current_node = self.current_node.best_move()
        self.current_node.parent = None
        return self.current_node.parent_move

    def move_to_child_node_with_move(self, old_pos, new_pos):
        """Phương thức này di chuyển nút hiện tại đến "đích" của nó trên cây trò chơi"""
        # Xác định trạng thái trò chơi so sánh
        new_state, move = GameState.generate_game_state_with_move(
            self.current_node.game_state, old_pos, new_pos
        )

        # Tra cứu các trạng thái trong danh sách nút con để tìm nút con phù hợp
        for node in self.current_node.list_of_children:
            if new_state.board == node.game_state.board:
                self.current_node = node
                self.current_node.parent = None
                return

        # Không tìm thấy nút phù hợp
        self.current_node = self._create_node(new_state, None, move)

    def is_lost(self) ->bool:
        """Phương pháp này kiểm tra xem bot có bị thua hay không"""
        return len(self.current_node.game_state.all_child_gamestates) == 0

    # Phương thức trừu tượng
    def _create_node(self, game_state, parent, parent_move) -> Node:
        """Phương thức này trả về một nút mới trong cây"""
        pass

class GameTreeMinimax(GameTree):
    """Lớp này chịu trách nhiệm về cây trò chơi minimax"""
    def __init__(self, team, target_depth, value_pack: int = 0) -> None:
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    # Phương thức riêng
    def _create_node(self, game_state, parent, parent_move) -> NodeMinimax:
        """Phương thức tạo nút minimax"""
        return NodeMinimax(game_state, parent, parent_move)

    # Phương thức thực thể
    def process(self, moves_queue) -> tuple:
        """Cho bot chạy"""
        # Bắt đầu bộ đếm thời gian
        start = time()
        self.current_node.minimax(self.target_depth, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        print(self.current_node.minimax_value)
        self.count = 0
        end = time()  # Kết thúc bộ đếm
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

class GameTreeDynamicMinimax(GameTreeMinimax):
    """Lớp này chịu trách nhiệm về hiệu suất của cây trò chơi Dynamic Minimax"""

    # Khởi tạo hàm
    def process(self, moves_queue) -> tuple:
        """Lấy chạy bot"""
        ADVANTAGE_CONSTANT = 25

        # Bắt đầu bộ đếm thòi gian
        start = time()
        print(self.current_node.game_state.value * self.team.value)
        # Nếu hệ số phân nhánh của nút hiện tại là <= 3 thì chạy ở độ sâu mục tiêu + 2
        if len(self.current_node.game_state.all_child_gamestates) <= 3:
            self.current_node.minimax(self.target_depth + 2, self.team is Team.RED)
        # Nếu giá trị lợi thế của nút hiện tại >= hằng số lợi thế,
        # Sau đó chạy ở độ sâu mục tiêu + 1
        elif self.current_node.game_state.value * self.team.value >= ADVANTAGE_CONSTANT:
            self.current_node.minimax(self.target_depth + 1, self.team is Team.RED)
        # Nếu giá trị lợi thế của nút hiện tại nhỏ hơn hằng số lợi thế,
        # Sau đó chạy ở độ sâu mục tiêu
        else:
            self.current_node.minimax(self.target_depth, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # Kết thúc
        print(self.count)
        self.count = 0
        end = time()  # Bắt đầu bộ đếm thời gian
        print("Thời gian: {:.2f} s".format(end - start))
        print("{} di chuyển: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos


class GameTreeDeepeningMinimax(GameTreeMinimax):
    """Lớp này chịu trách nhiệm thực hiện cây trò chơi Deepening Minimax"""

    # Khởi tạo hàm
    def process(self, moves_queue) -> tuple:
        """Hãy để bot chạy"""

        # Hệ số cho từng gói giá trị
        if self._value_pack == 1:
            DEPTH_VALUE_CONSTANT = [0, 1, 2, 3, 16, 12]
        elif self._value_pack == 2:
            DEPTH_VALUE_CONSTANT = [0, 1, 1, 2, 4, 7]

        # Bắt đầu bộ đếm thời gian
        start = time()
        # Tìm danh sách di chuyển tốt nhất
        best_moves = dict()
        for depth in range(1, self.target_depth + 1):
            if DEPTH_VALUE_CONSTANT[depth] == 0:
                continue
            self.current_node.minimax(depth, self.team is Team.RED)
            for child in self.current_node.list_of_children:
                if child.minimax_value == self.current_node.minimax_value:
                    key = child.parent_move
                    best_moves[key] = (
                        best_moves.get(key, 0) + DEPTH_VALUE_CONSTANT[depth]
                    )
                    print(depth, key)

        # Tìm giá trị tốt nhất
        old_pos, new_pos = None, None
        max_move_val = -inf
        for key, val in best_moves.items():
            if val > max_move_val:
                max_move_val = val
                old_pos, new_pos = key

        print("Giá trị di chuyển:", best_moves[(old_pos, new_pos)])
        self.move_to_child_node_with_move(old_pos, new_pos)
        moves_queue.append((old_pos, new_pos))

        # Kết thúc
        print(self.count)
        self.count = 0
        end = time()  # Kết thúc bộ đếm
        print("Thời gian: {:.2f} s".format(end - start))
        print("{} di chuyển: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos
