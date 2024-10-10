"""Mô-đun dùng để tạo lớp Node và lớp con của nó"""
from abc import ABC, abstractmethod
from random import choice, shuffle
from cmath import inf
from game_state import GameState
from team import Team

class Node(ABC):
    """Lớp này đại diện cho một "nút" trong cây trò chơi"""
    # BẮT ĐẦU KHỞI TẠO
    def __init__(self, game_state: GameState, parent, parent_move: tuple):
        # Tham chiếu tới nút cha và nút con của một nút
        self.parent = parent
        self.parent_move = parent_move
        self.list_of_children = list()
        # Thống kê nút
        self.game_state = game_state
        self._is_generated_all_children = False

    # BẮT ĐẦU PHƯƠNG THỨC
    # Phương thức cơ bản
    def get_all_children(self) -> list:
        """Phương thức trả về tất cả các nút con của nút hiện tại"""
        current_state = self.game_state
        children = []

        # Tạo danh sách các trạng thái trò chơi có thể có
        list_of_state = current_state.all_child_gamestates

        # Tạo các nút mới và thêm nó vào danh sách con
        for state, move in list_of_state:
            new_node = self._create_node(state, self, move)
            children.append(new_node)

        return children

    def generate_all_children(self) -> None:
        """Phương thức này lấp đầy danh sách các nút con"""
        if self._is_generated_all_children:
            return
        self.list_of_children = self.get_all_children()
        self._is_generated_all_children = True

    # Phương thức trừu tượng
    @abstractmethod
    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Phương thức này trả về một nút mới"""
        pass

class NodeMinimax(Node):
    """Lớp đại diện cho nút xử lý minimax trong cây trò chơi"""
    # Bắt đầu khởi tạo
    def __init__(self, game_state: GameState, parent, parent_move: tuple)-> None:
        # Truyền lại cho lớp cha
        super().__init__(game_state, parent, parent_move)

        # Trạng thái minimax
        self._is_children_sorted = False
        self.minimax_value = None

    # Tạo phương thức
    def minimax(self, depth: int, max_run: bool, alpha: float = -inf, beta: float = inf) -> float:
        """Phương thức Minimax"""
        self.minimax_value = None

        # Nếu đã đạt đến độ sâu mục tiêu
        if depth == 0:
            self.minimax_value = self.game_state.value
            return self.minimax_value

        self.generate_all_children()

        # Nếu nút không có nút con
        if len(self.list_of_children) == 0:
            if self.game_state._current_team is Team.RED:
                self.minimax_value = -inf
            else:
                self.minimax_value = inf
            return self.minimax_value

        # Tối đa hoá
        if max_run is True:
            best_value = -inf

            # Sắp xếp danh sách nút con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=True
                )
                self._is_children_sorted = True

            # Đi đến độ sâu sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, True, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            self.minimax_value = best_value
            return best_value

        # Tối thiểu hoá
        else:
            best_value = inf

            # Sắp xếp danh sách nút con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=True
                )
                self._is_children_sorted = True

            # Đi đến độ sâu sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, True, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

            self.minimax_value = best_value
            return best_value

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Phương thức tạo nút minimax mới"""
        return NodeMinimax(game_state, parent, parent_move)

    def best_move(self):
        """Phương thức trả về nút con tốt nhất của nút hiện tại"""
        # Tạo danh sách nút có giá trị tốt
        best_children = list()

        for child in self.list_of_children:
            # Nếu nút có giá trị bằng nút hiện tại thì thêm vào danh sách
            if child.minimax_value == self.minimax_value:
                best_children.append(child)

        # Trả về ngẫu nhiên nút con trong danh sách
        return choice(best_children)