class Gamestate:
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9
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

    @property
    def value(self) -> float:

    @property
    def all_child_gamestates(self) -> list:

    def _get_game_state_value(self) -> float:

    def _get_the_opponent_team(self) -> Team: