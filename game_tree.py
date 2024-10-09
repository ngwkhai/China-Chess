"""Mô-đun dùng để tạo lớp GameTree và các lớp con của nó"""
from abc import ABC
from cmath import inf

from node import Node
from team import Team
from node import Node, NodeMinimax

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
        self.current_node = self.current_node_best_move()
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