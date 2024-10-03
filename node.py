from math import inf, sqrt, log
from abc import ABC, abstractmethod
from random import choice, shuffle
from game_state import GameState
from team import Team


class Node(ABC):
    # Lớp này đại diện cho một "nút" trong cây trò chơi

    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Tham chiếu đến nút cha và các nút con của một nút
        self.parent = parent
        self.parent_move = parent_move
        self.list_of_children = list()

        # Thống kê của nút
        self.game_state = game_state
        self._is_generated_all_children = False

    # Phương thức của đối tượng
    def get_all_children(self) -> list:
        # Phương thức này tạo tất cả các nút con của nút hiện tại
        current_state = self.game_state
        children = []

        # Tạo danh sách các trạng thái trò chơi có thể xảy ra
        list_of_states = current_state.all_child_gamestates

        # Tạo các nút mới và thêm vào danh sách con
        for state, move in list_of_states:
            new_node = self._create_node(state, self, move)
            children.append(new_node)

        return children

    def generate_all_children(self) -> None:
        # Phương thức này điền vào danh sách các nút con
        if self._is_generated_all_children:
            return
        self.list_of_children = self.get_all_children()
        self._is_generated_all_children = True

    # Phương thức trừu tượng
    @abstractmethod
    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        # Phương thức này trả về một nút mới
        pass

    # [KẾT THÚC PHƯƠNG THỨC]


class NodeMinimax(Node):
    # Lớp này đại diện cho một "nút minimax" trong cây trò chơi

    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Tham chiếu đến một nút
        super().__init__(game_state, parent, parent_move)

        # Thống kê minimax
        self._is_children_sorted = False
        self.minimax_value = None

    # Phương thức của đối tượng
    def minimax(
        self, depth: int, max_turn: bool, alpha: float = -inf, beta: float = inf
    ) -> float:
        # Phương thức Minimax

        self.minimax_value = None
        # Nếu nút đạt độ sâu mục tiêu
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

        # Lượt của người chơi tối đa hóa
        if max_turn is True:
            best_value = -inf

            # Sắp xếp danh sách các nút con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=True
                )
                self._is_children_sorted = True

            # Đi đến độ sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, False, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            self.minimax_value = best_value
            return best_value

        # Lượt của người chơi tối thiểu hóa
        else:
            best_value = inf

            # Sắp xếp danh sách các nút con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=False
                )
                self._is_children_sorted = True

            # Đi đến độ sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, True, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            self.minimax_value = best_value
            return best_value

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        # Phương thức này tạo một nút minimax mới
        return NodeMinimax(game_state, parent, parent_move)

    def best_move(self):
        # Phương thức này trả về "nút con tốt nhất" của nút hiện tại
        # Tạo danh sách các nút có giá trị tốt nhất
        best_children = list()

        for child in self.list_of_children:
            # Nếu nút có giá trị giống với giá trị của nút hiện tại, thì thêm vào danh sách
            if child.minimax_value == self.minimax_value:
                best_children.append(child)

        # Trả về một nút ngẫu nhiên trong danh sách
        return choice(best_children)
class NodeMCTS(Node):
    """Lớp này đại diện cho một "nút Monte-Carlo tree search" trong cây trò chơi"""

    # [BẮT ĐẦU HẰNG SỐ]

    EXPLORATION_CONSTANT = sqrt(6) - 1
    EXPONENTIAL_INDEX = 0.99
    MAX_NODE_COUNT = 5

    # [KẾT THÚC HẰNG SỐ]

    # [BẮT ĐẦU KHỞI TẠO]

    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Tham chiếu đến một nút
        super().__init__(game_state, parent, parent_move)

        # Thống kê MCTS
        self._number_of_visits = 0
        self._rating = 0
        self.worst_child = None

        # Thống kê khác
        self.is_children_sorted = False
        self.rollout_index = -1
        self.num = 0

    # Khởi tạo thuộc tính
    @property
    def q(self):
        """Trả về đánh giá của nút"""
        return -self.game_state._current_team.value * self._rating

    @property
    def n(self):
        """Trả về số lượt ghé thăm nút này"""
        return self._number_of_visits

    @property
    def e(self):
        """Trả về hằng số khám phá hiện tại"""
        return self.EXPLORATION_CONSTANT

    # [KẾT THÚC KHỞI TẠO]

    # [BẮT ĐẦU PHƯƠNG THỨC]
    # Phương thức thể hiện

    def best_uct(self):
        """Hàm này tính toán đứa con có chỉ số UCT tốt nhất của nút"""

        # Khởi tạo giá trị tốt nhất hiện tại
        current_best_uct_value = -inf
        current_result_child = []

        for child in self.list_of_children:
            if child.n != 0:
                # Nếu đứa con hiện tại đã được thăm
                uct = child.q / child.n + self.e * (log(self.n) / child.n**2) ** self.EXPONENTIAL_INDEX
            else:
                # Nếu đứa con hiện tại chưa được thăm
                uct = inf

            # So sánh việc lựa chọn ngẫu nhiên
            if uct > current_best_uct_value:
                current_best_uct_value = uct
                current_result_child = [child]
            elif uct == current_best_uct_value:
                current_result_child.append(child)

        shuffle(current_result_child)
        res = current_result_child.pop()
        return res

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Phương thức này tạo một nút MCTS mới"""
        return NodeMCTS(game_state, parent, parent_move)

    def update_stat(self, result):
        """Phương thức này cập nhật thống kê của một nút"""
        self._rating += result
        self._number_of_visits += 1
        if self.worst_child is None:
            self.worst_child = result
        else:
            if self.game_state._current_team is Team.RED:
                self.worst_child = min(self.worst_child, result)
            else:
                self.worst_child = max(self.worst_child, result)

    def terminate_value(self, is_end: bool) -> float:
        """Phương thức này trả về giá trị nếu một nút đạt trạng thái kết thúc"""
        if is_end:
            winning_team = self.game_state.get_team_win()
            if winning_team is Team.RED:
                return 1
            elif winning_team is Team.BLACK:
                return -1
            elif winning_team is Team.NONE:
                return 0
        else:
            if self.game_state.value == inf:
                return 1
            elif self.game_state.value == -inf:
                return -1
            return self.game_state.value / 1000

    def rollout_policy(self, value_pack):
        """Phương thức này trả về nút khởi tạo mô phỏng được chọn dựa trên chính sách rollout đã cho"""

        # Chính sách ngẫu nhiên
        if value_pack == "RANDOM":
            new_game_state = self.game_state.generate_random_game_state()
            if new_game_state is None:
                return None
            else:
                return self._create_node(new_game_state[0], self, new_game_state[1])

        # MCTSVariant1: Lựa chọn ngẫu nhiên cao nhất
        if value_pack == "VAR1":
            potential_game_state = None
            potential_game_value = -inf
            all_states = self.game_state.all_child_gamestates

            if len(all_states) == 0:
                return None

            for _ in range(5):
                cur = choice(all_states)
                if cur[0].value > potential_game_value:
                    potential_game_state = cur
                    potential_game_value = cur[0].value

            if potential_game_state is None:
                return None
            return self._create_node(
                potential_game_state[0], self, potential_game_state[1]
            )

        # MCTSVariant2: Lựa chọn sắp xếp
        if value_pack == "VAR2":
            if len(self.game_state.all_child_gamestates) == 0:
                return None

            if self.is_children_sorted is False:
                self.game_state.all_child_gamestates.sort(
                    key=lambda child: child[0].value, reverse=True
                )
                self.is_children_sorted = True

            self.rollout_index = min(
                self.rollout_index + 1, len(self.game_state.all_child_gamestates) - 1
            )

            return self._create_node(
                self.game_state.all_child_gamestates[self.rollout_index][0],
                self,
                self.game_state.all_child_gamestates[self.rollout_index][1],
            )

    def rollout(self, rollout_policy, target_depth: int = MAX_NODE_COUNT):
        """Phương thức này thực hiện mô phỏng rollout"""
        node_count = 0
        current_node = self
        while node_count < target_depth:
            new_node = current_node.rollout_policy(rollout_policy)
            # Nếu nút hiện tại là nút kết thúc, trả về;
            # Nếu không, gán nút hiện tại cho một đứa con ngẫu nhiên
            if new_node is None:
                return current_node.terminate_value(True)
            current_node = new_node

            node_count += 1

        return current_node.terminate_value(False)

    def backpropagate(self, result):
        """Phương thức này thực hiện backpropagation của MCTS"""

        current_node = self
        while current_node.parent is not None:
            # Tổ tiên cuối cùng
            current_node.update_stat(result)
            current_node = current_node.parent

        current_node.update_stat(result)

    def best_move(self):
        """Phương thức này trả về "đứa con tốt nhất" của nút hiện tại"""

        max_number_of_visits = -inf
        current_best_child = []

        # Duyệt qua các nút con
        for child in self.list_of_children:
            val = child.n + child.q / child.n * 21000
            if val > max_number_of_visits:
                max_number_of_visits = val
                current_best_child.clear()
            if val == max_number_of_visits:
                current_best_child.append(child)

        shuffle(current_best_child)
        return current_best_child.pop()


class NodeExcavationMinimax(NodeMinimax):
    """Lớp này đại diện cho một "nút Excavation Minimax" trong cây trò chơi"""

    SIMULATION_FACTOR = 3
    DEPTH_COUNT = 3
    NORMALIZE_CONST = 6

    # Phương thức thể hiện

    def _simulation(self):
        """Từng bước khai thác độ sâu thấp hơn"""
        res = 0
        for depth in range(1, self.DEPTH_COUNT + 1):
            simulation_count = self.SIMULATION_FACTOR**depth
            for _ in range(simulation_count):
                node = NodeMCTS(self.game_state, None, None)
                value = node.rollout("RANDOM", depth)
                res += value * (1 / self.NORMALIZE_CONST**depth)
        return res

    def minimax(
        self, depth: int, max_turn: bool, alpha: float = -inf, beta: float = inf
    ):
        """Phương thức Excavation Minimax"""

        self.minimax_value = None
        # Nếu nút đạt độ sâu mục tiêu
        if depth == 0:
            temp = self._simulation()
            self.minimax_value = self.game_state.value + temp
            return self.minimax_value

        self.generate_all_children()
        # Nếu nút hiện tại không có đứa con
        if len(self.list_of_children) == 0:
            if self.game_state._current_team is Team.RED:
                self.minimax_value = -inf
            else:
                self.minimax_value = inf

            return self.minimax_value

        # Tối đa hóa lượt chơi
        if max_turn is True:
            best_value = -inf

            # Sắp xếp danh sách các đứa con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=True
                )
                self._is_children_sorted = True

            # Duyệt qua độ sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, False, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            self.minimax_value = best_value
            return best_value

        # Tối thiểu hóa lượt chơi
        else:
            best_value = inf

            # Sắp xếp danh sách các đứa con
            if self._is_children_sorted is False:
                self.list_of_children.sort(
                    key=lambda node: node.game_state.value, reverse=False
                )
                self._is_children_sorted = True

            # Duyệt qua độ sâu hơn
            for child in self.list_of_children:
                value = child.minimax(depth - 1, True, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            self.minimax_value = best_value
            return best_value

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """Phương thức này tạo ra một node Minimax Đào Bới mới"""

        return NodeExcavationMinimax(game_state, parent, parent_move)

    def best_move(self):
        """Phương thức này trả về "nước đi tốt nhất" của node hiện tại"""

        # Tạo danh sách các node có giá trị tốt nhất
        best_children = list()

        for child in self.list_of_children:
            # Nếu node có cùng giá trị với giá trị của node hiện tại, thì thêm nó vào danh sách
            if child.minimax_value == self.minimax_value:
                best_children.append(child)

        # Trả về một node ngẫu nhiên trong danh sách
        return choice(best_children)
