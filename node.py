"""Mô-đun dùng để tạo lớp Node và lớp con của nó"""
from abc import ABC, abstractmethod


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
        """This method returns a new node"""
        pass

