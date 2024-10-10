import sys
from time import time
import threading
import pygame
import resource
from game_state import GameState
from game_tree import GameTree
from team import Team
from cmath import inf
from gui_utilities import Button, InputBox, DropDown
from game_tree import GameTree, GameTreeMinimax
from piece import Piece

# Tạo các biến toàn cục
# chứa nước đi và giá trị trạng thái trò chơi được giải quyết trong chuỗi chạy bot
moves_queue, value_queue = list(), list()
# Biến kết quả của eve module
winner = dict()
# Biến toàn cục để điều khiển trò chơi
is_end, force_end = False, False

# Khởi tạo pygame
pygame.init()

# Cài đặt cửa sổ
SCREEN = pygame.display.set_mode((660, 664))
pygame.display.set_caption("CỜ TƯỚNG")
pygame.display.set_icon(resource.icon())

# Đặt tốc độ làm mới
REFRESH_RATE = 30

# Tạo đối tượng đồng hồ
clock = pygame.time.Clock()

# Bắt đầu hàm chính
def str_to_type(type_str: str) -> GameTree:
    """Hàm này trả về loại cây trò chơi tương ứng với chuỗi đầu vào"""
    if type_str == 'Minimax':
        return GameTreeMinimax
    elif type_str == 'MCTS':
        pass
        

def draw_gamestate(game_state: GameState, inverse: bool = False) -> None:
    """Hàm vẽ trạng thái trò chơi"""

    # Vẽ bàn cờ
    board_img, board_position = resource.board_sprite()
    SCREEN.blit(board_img, board_position)

    # Vẽ quân cờ
    for x in range(GameState.BOARD_SIZE_X):
        for y in range(GameState.BOARD_SIZE_Y):
            notation = game_state.board[x][y]

            # Bỏ qua nếu không có quân nào ở vị trí
            if notation == "NN":
                continue

            # Tạo một thực thể quân cờ
            piece = Piece.create_instance(
                (abs(x - int(inverse) * 9), y),
                notation, game_state.board, None, None
            )

            # Vẽ quân cờ
            piece_img, piece_position = resource.piece_sprite(piece)
            SCREEN.blit(piece_img, piece_position)

def bot_run():
    return

def simulation_screen(
        red_type: str,
        red_value: str,
        red_another_property: str,
        black_type: str,
        black_value: str,
        black_another_property: str,
        number_of_simulations: str
) -> None:
    """Đây là hàm mô phỏng màn hình"""
    def get_bot_full_type(bot_type, bot_property, bot_value):
        """Hàm này dùng để lấy tên đầy đủ của bot
        được sử dụng cho màn hình kết quả"""
        res = bot_type + ' '

        if bot_type == "Minimax":
            res += 'Độ sâu ' + bot_property + ' '
        elif bot_type == "MCTS":
            res += 'Thời gian ' + bot_property + 's '

        res += 'Cấp độ ' + bot_value
        return res

    # Thay đổi chuỗi thành kiểu thích hợp
    red_full_type = get_bot_full_type(red_type, red_another_property, red_value)
    black_full_type = get_bot_full_type(black_type, black_another_property, black_value)

    red_type, black_type = str_to_type(red_type), str_to_type(black_type)
    red_value, black_value = int(red_value), int(black_value)

    red_another_property = int(red_another_property)
    black_another_property = int(black_another_property)
    number_of_simulations = int(number_of_simulations)

    # Tạo các nút
    pause_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(756, 450),
                          text_input="Hoãn", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    skip_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(756, 550),
                          text_input="Dừng", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    # Mở rộng kích thước của màn hình
    SCREEN = pygame.display.set_mode((896, 664))
    MOVE_TIME = 0.5

    # Tạo các biến cần thiết
    global is_end, force_end, winner
    winner = {"BLACK" : 0, "DRAW" : 0, "RED" : 0}
    is_end, is_paused = True, False
    check_point = time()
    gamestate, move, bot_run_thread = None, None, None
    games_done_count = 0
    black_win, red_win, draw = 0, 0, 0

    # Bắt đầu
    start = time()

    # Bắt đầu vòng lặp trò chơi
    while True:
        # Lấy trạng thái gama hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Xử lý sự kiên bấm
        for event in events_list:
            # Thoát trò chơi nếu bấm x
            if event.type == pygame.QUIT:
                force_end = True
                pygame.quit()
                sys.exit()

            #  Xử lý việc bấm vào các nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.check_for_input(mouse_pos):
                    is_paused = not is_paused
                elif skip_button.check_for_input(mouse_pos):
                    is_paused = False
                    force_end = True
                    is_end = True
                    bot_run_thread.join()
                    moves_queue.clear()
                    value_queue.clear()

        # Nếu trò chơi không bị tạm dừng thì cập nhật bảng
        if is_paused is False:
            if is_end is True and len(moves_queue) == 0:
                black_win, red_win, draw = winner["BLACK"], winner["RED"], winner["DRAW"]
                games_done_count += 1

                # Nếu đã đạt số lần mô phỏng thì dừng
                if games_done_count > number_of_simulations:
                    bot_run_thread.join()
                    break

                # Khôi phục lại các biến
                value_queue.clear()
                current_red_value, current_black_value = 0, 0
                is_end = False
                move = None
                gamestate = GameState.generate_initial_game_state()

                if bot_run_thread is not None:
                    bot_run_thread.join()

                bot_run_thread = threading.Thread(target=bot_run,
                    args=(red_type, red_value, red_another_property,
                          black_type, black_value, black_another_property
                ))
                bot_run_thread.start()

            # Cố gắng di chuyển
            try:
                if time() - check_point > MOVE_TIME:
                    move = moves_queue.pop(0)
                    gamestate = gamestate.generate_game_state_with_move(move[0], move[1])[0]
                    current_red_value, current_black_value = value_queue.pop(0)

                    check_point = time()

            # Nếu bot chưa thực hiện nước đi nào thì vượt qua
            except IndexError:
                pass

        # Làm sạch làm hình
        SCREEN.fill((241, 203, 157))

        # Vẽ
        # Trạng thái trò chơi
        draw_gamestate(gamestate)

        if move is not None:
            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(move[0])
            SCREEN.blit(chosen_ring_img, draw_pos)

            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(move[1])
            SCREEN.blit(chosen_ring_img, draw_pos)

        # Vẽ nút
        for button in [pause_button, skip_button]:
            button.draw(SCREEN)

        # Chữ
        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 18, 208, 79))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 22, 200, 71))
        text = resource.get_font(25, 0).render("Đen " + str(black_win), True, "Black")
        SCREEN.blit(text, (670, 30))

        text = resource.get_font(25, 0).render("Đỏ " + str(red_win), True, "Red")
        SCREEN.blit(text, (790, 30))

        text = resource.get_font(25, 0).render("Số nước " + str(draw), True, "#56000E")
        SCREEN.blit(text, (730, 60))

        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 110, 208, 109))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 114, 200, 101))

        text = resource.get_font(25, 0).render("Thống kê", True, "#56000E")
        SCREEN.blit(text, (730, 118))

        text = resource.get_font(25, 0).render(
            "Black        "+ str(round(float(current_black_value), 2)), True, "Black")
        SCREEN.blit(text, (670, 148))

        text = resource.get_font(25, 0).render(
            "Red          " + str(round(float(current_red_value), 2)), True, "Red")
        SCREEN.blit(text, (670, 178))

        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 240, 208, 92))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 244, 200, 84))

        # Trạng thái quân cờ
        piece_position = resource.get_piece_position(mouse_pos)
        if piece_position is not None:
            notation = gamestate.board[piece_position[0]][piece_position[1]]
            if notation != "NN":
                if Team[notation[0]] is Team.RED:
                    number_of_team_piece = gamestate.number_of_red_pieces
                else:
                    number_of_team_piece = gamestate.number_of_black_pieces

                piece = Piece.create_instance(
                    piece_position, notation, gamestate.board,
                    gamestate.number_of_black_pieces + gamestate.number_of_red_pieces,
                    number_of_team_piece
                )

                text = resource.get_font(26, 0).render(
                    "Kiểu quân: " + piece._piece_type.capitalize(), True, "#56000E"
                )
                SCREEN.blit(text, (670, 250))

                text = resource.get_font(26, 0).render(
                    "Đội quân: " + str(piece.team).capitalize(), True, "#56000E")
                SCREEN.blit(text, (670, 275))

                if piece.team is Team.RED:
                    text = resource.get_font(26, 0).render(
                        "Giá trị quân: " + str(round(piece.piece_value(red_value), 2)), True, "#56000E")
                else:
                    text = resource.get_font(26, 0).render(
                        "Giá tri quân: " + str(round(piece.piece_value(black_value), 2)), True, "#56000E")
                SCREEN.blit(text, (670, 300))

        # Cập nhật mà hình
        pygame.display.flip()

        # Thời gian đợi khung hình tiếp theo
        clock.tick(REFRESH_RATE)

    # Kết thúc xử lý
    print(winner)
    end = time()
    print("Tổng thời gian: {} s\n".format(end - start))

    # Di chuyển đến màn hình kết quả
    # eve_reslt(red_full_type, black_full_type)

def eve_menu():
    # Tạo một số tiện ích
    black_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 290, 100, 30,
        resource.get_font(26, 0),
        "Bot", ["Minimax", "MCTS"]
    )
    black_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 290, 100, 30,
        resource.get_font(26, 0),
        "Cấp độ", ["0", "1", "2"]
    )
    red_type = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        350, 290, 100, 30,
        resource.get_font(26, 0),
        "Bot", ["Minimax", "MCTS"]
    )
    red_value = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        510, 290, 100, 30,
        resource.get_font(26, 0),
        "Cấp độ", ["0", "1", "2"]
    )

    num_box = InputBox(330, 125, 40, 40, resource.get_font(30, 0),
                       "Black", "Red", "Số trận")
    black_another_property = InputBox(165, 230, 40, 30, resource.get_font(26, 0),
                                     "Black", "Red", "Độ sâu cho chép")
    red_another_property = InputBox(495, 230, 40, 30, resource.get_font(26, 0),
                                    "Red", "Black", "Độ sâu cho chép")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 450),
                          text_input="Bắt đầu", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 550),
                         text_input="Thoát", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 550),
                         text_input="Trở lại", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Bắt đầu vòng lặp trò chơi
    while True:
        # Nhận trạng thái trò chơi hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Vẽ menu chính
        # Vẽ nền
        bg_img, bg_pos = resource.background()
        SCREEN.blit(bg_img, bg_pos)

        # Vẽ chữ
        menu_text = resource.get_font(70, 0).render("Nhập cuộc", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 60))
        SCREEN.blit(menu_text, menu_rect)

        text = resource.get_font(60, 0).render("Black", True, "Black")
        rect = text.get_rect(center=(165, 185))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Kiểu Bot", True, "Black")
        rect = text.get_rect(center=(70, 270))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Cấp độ", True, "Black")
        rect = text.get_rect(center=(230, 270))
        SCREEN.blit(text, rect)

        text = resource.get_font(60, 0).render("Red", True, "#AB001B")
        rect = text.get_rect(center=(495, 185))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Kiểu Bot", True, "#AB001B")
        rect = text.get_rect(center=(400, 270))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Cấp độ", True, "#AB001B")
        rect = text.get_rect(center=(560, 270))
        SCREEN.blit(text, rect)

        # Vẽ nút
        for button in [start_button, quit_button, back_button]:
            button.draw(SCREEN)

        # Vẽ danh sách
        for lst in [black_type, black_value, red_type, red_value]:
            selected_option = lst.update(events_list)
            if selected_option >= 0:
                lst.main = lst.options[selected_option]

            lst.draw(SCREEN)

        # Vẽ hộp nhập
        for input_box in [num_box, black_another_property, red_another_property]:
            input_box.update()
            input_box.draw(SCREEN)

        # Xử lý sự kiện
        for event in events_list:
            # Thoát nếu bấm exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Xử lý khi bấm vào nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Nếu tất cả thông tin được điền đầy đủ
                # Trò chơi sẽ bắt đầu
                if start_button.check_for_input(mouse_pos):
                    if (red_type.main == "Bot" or black_type.main == "Bot"
                        or red_value.main == "Cấp độ" or black_value.main == "Cấp độ"
                        or not num_box.text.isnumeric()
                        or not black_another_property.text.isnumeric()
                        or not red_another_property.text.isnumeric()
                    ):
                        continue
                    simulation_screen(
                        red_type.main, red_value.main, red_another_property.text,
                        black_type.main, black_value.main, black_another_property.text,
                        num_box.text
                    )

                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

            for input_box in [num_box, black_another_property, red_another_property]:
                input_box.handle_event(event)


        # Cập nhật màn hình
        pygame.display.flip()
        # Thời gian khung hình
        clock.tick(REFRESH_RATE)

def main_menu():
    """Hàm này là màn hình menu chính"""
    # Tạo các nút
    pve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 220),
                        text_input="Người vs Máy", font=resource.get_font(30, 0), base_color="#AB001B", hovering_color="Black")
    pvp_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 330),
                        text_input="Người vs Người", font=resource.get_font(30, 0), base_color="#AB001B", hovering_color="Black")
    eve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 440),
                        text_input="Máy vs Máy", font=resource.get_font(30, 0), base_color="#AB001B", hovering_color="Black")
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(330.5, 550),
                         text_input="Thoát", font=resource.get_font(28, 0), base_color="Black", hovering_color="#AB001B")
    # Bắt đầu vòng lặp game
    while True:
        # Nhận trạng thái trò chơi hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Vẽ menu chính
        # Vẽ background
        bg_img, bg_pos = resource.background()
        SCREEN.blit(bg_img, bg_pos)

        # Vẽ chữ menu
        menu_text = resource.get_font(100, 0).render("CỜ TƯỚNG", True, "White")
        menu_rect = menu_text.get_rect(center = (330.5, 100))
        SCREEN.blit(menu_text, menu_rect)

        for button in [pve_button, pvp_button, eve_button, quit_button]:
            button.draw(SCREEN)

        # xử lý sự kiện
        for event in events_list:
            # Thoát khỏi trò chơi nếu nút QUIT được nhấp
            if event.type == pygame.QUIT:
                print("Thoát")
                pygame.quit()
                sys.exit()

            # Xử lý sự kiện bấm vào các nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pve_button.check_for_input(mouse_pos):
                    pve_menu()
                if pvp_button.check_for_input(mouse_pos):
                    pvp_menu()
                if eve_button.check_for_input(mouse_pos):
                    eve_menu()
                if quit_button.check_for_input(mouse_pos):
                    print("Thoát")
                    pygame.quit()
                    sys.exit()

        # Cập nhật màn hình
        pygame.display.flip()

        # Chờ khung hình tiếp theo
        clock.tick(REFRESH_RATE)

def pve_screen(
    bot_type: GameTree,
    bot_value: int,
    bot_another_property: int,
    player_team: Team
) -> None:

    # Tạo biến cho bot
    bot = bot_type(Team.get_reverse_team(player_team), bot_another_property, bot_value)
    is_bot_process = False

    # Tạo biến cho người chơi
    player_turn = player_team is Team.RED
    player_gamestate = GameState.generate_initial_game_state()

    # Tạo biến di chuyển 
    position_chosen, piece_chosen = None, None
    last_move = None

    #
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="Thoát", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="Trở lại", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Bắt đầu vòng lặp cho trò chơi
    while True:
        # Lấy trạng thái hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        win_status = player_gamestate.get_team_win()

        # Xử lí event
        for event in events_list:
            # Thoát trò chơi nếu bấm vào nút thoát
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Khi trò chơi kết thúc, thoát hoặc quay lại menu ban đầu
            if win_status is not Team.NONE and event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    pve_menu()

        # .Background
        SCREEN.fill(((241, 203, 157)))

        # Trạng thái trò chơi
        draw_gamestate(player_gamestate, player_team is Team.BLACK)

        # Chọn
        if position_chosen is not None:
            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(position_chosen)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # Hiển thị hình ảnh của các vòng tròn tương ứng với nước đi cuối cùng
        if last_move is not None:
            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(last_move[0], player_team is Team.BLACK)
            SCREEN.blit(chosen_ring_img, draw_pos)

            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(last_move[1], player_team is Team.BLACK)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # Nếu trò chơi kết thúc, hãy rút thông báo và nhấn nút
        if win_status is not Team.NONE:
            # Thông báo
            pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(0, 270, 660, 120))
            pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(4, 274, 652, 112))

            if win_status is player_team:
                text = resource.get_font(50, 0).render("Xin chúc mừng, bạn đã thắng.", True, "Black")
            else:
                text = resource.get_font(50, 0).render("Chúc bạn may mắn lần sau.", True, "Black")
            rect = text.get_rect(center=(330.5, 330))
            SCREEN.blit(text, rect)

            # Buttons
            for button in [quit_button, back_button]:
                button.draw(SCREEN)

        # Xử lí di chuyển
        else:
            # Lượt người chơi
            if player_turn:
                for event in events_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Tính toán vị trí nhấp chuột trong UI, vị trí nhấp chuột trong bảng trạng thái trò chơi
                        click_pos = resource.get_piece_position(mouse_pos)
                        board_pos = resource.get_piece_position(mouse_pos, player_team is Team.BLACK)

                       # Nếu vị trí nhấp chuột nằm ngoài bảng hoặc trên quân cờ đã chọn => bỏ chọn quân cờ
                        if click_pos is None or click_pos == position_chosen:
                            position_chosen, piece_chosen = None, None
                            continue

                        notation = player_gamestate.board[board_pos[0]][board_pos[1]]
                        # Nếu quân cờ thuộc về người chơi => chọn quân cờ đó
                        if Team[notation[0]] is player_team:
                            position_chosen = click_pos
                            piece_chosen = Piece.create_instance(
                                board_pos, 
                                notation, 
                                player_gamestate.board, 
                                None, None
                            )

                        # Nếu vị trí nhấp chuột nằm trong danh sách các nước đi được phép của quân cờ đã chọn
                        elif piece_chosen is not None and board_pos in piece_chosen.admissible_moves:
                            new_gamestate = player_gamestate.generate_game_state_with_move(piece_chosen.position, board_pos)
                            # Nếu nước đi hợp lệ thì di chuyển đến vị trí đó
                            if new_gamestate is not None:
                                player_gamestate = new_gamestate[0]
                                bot.move_to_child_node_with_move(piece_chosen.position, board_pos)

                                last_move = (piece_chosen.position, board_pos)
                                position_chosen, piece_chosen = None, None
                                player_turn = False

            # Lượt bot
            else:
                # Xử lí bot
                if is_bot_process is False:
                    # Tạo luồng chạy bot
                    bot_thread = threading.Thread(
                        target=bot.process, args=(moves_queue,))
                    bot_thread.start()

                    # Đánh dấu bot đã chạy
                    is_bot_process = True

                # Di chuyển
                try:
                    # Di chuyển quân 
                    old_pos, new_pos = moves_queue.pop(0)
                    player_gamestate = player_gamestate.generate_game_state_with_move(old_pos, new_pos)[0]

                    # End the bot run thread
                    bot_thread.join()

                    # Post process
                    is_bot_process = False
                    player_turn = True
                    last_move = (old_pos, new_pos)
                except IndexError:
                    pass

        # Cập nhật màn hình
        pygame.display.flip()

        # Đợi đến frame tiếp theo
        clock.tick(REFRESH_RATE)


def pve_menu():
    # Tạo giao diện menu 

    bot_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 270, 100, 30,
        resource.get_font(26, 0),
        "Kiểu Bot", ["Minimax", "MCTS"]) # Chọn thuật toán

    bot_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 270, 100, 30,
        resource.get_font(26, 0),
        "Cấp độ", ["0", "1", "2"])

    team_select = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        430, 220, 150, 50,
        pygame.font.SysFont(None, 30),
        "Màu quân", ["BLACK", "RED"])
        

    bot_another_property = InputBox(165, 210, 40, 30, resource.get_font(26, 0),
                                     "Black", "Red", "Độ sâu cho chép")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 430),
                          text_input="Bắt đầu", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="Thoát", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="Trở lại", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    
        # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Draw
        # .Background
        bg_img, bg_pos = resource.background()
        SCREEN.blit(bg_img, bg_pos)

        # .Text
        menu_text = resource.get_font(70, 0).render("Nhập cuộc", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 60))
        SCREEN.blit(menu_text, menu_rect)

        text = resource.get_font(50, 0).render("Chọn Bot", True, "Black")
        rect = text.get_rect(center=(165, 165))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Bot", True, "Black")
        rect = text.get_rect(center=(70, 250))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Cấp độ", True, "Black")
        rect = text.get_rect(center=(230, 250))
        SCREEN.blit(text, rect)

        text = resource.get_font(58, 0).render("Quân", True, "Black")
        rect = text.get_rect(center=(495, 165))
        SCREEN.blit(text, rect)

        # .Button
        for button in [start_button, quit_button, back_button]:
            button.draw(SCREEN)

        # .List
        for lst in [bot_type, bot_value, team_select]:
            selected_option = lst.update(events_list)
            if selected_option >= 0:
                lst.main = lst.options[selected_option]

            lst.draw(SCREEN)

        # .Input box
        for input_box in [bot_another_property]:
            input_box.update()
            input_box.draw(SCREEN)

        # Handle events
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(mouse_pos):
                    if (
                        bot_type.main == "Kiểu Bot"
                        or bot_value.main == "Cấp độ"
                        or team_select.main == "Quân"
                        or not bot_another_property.text.isnumeric()
                    ):
                        continue

                    pve_screen(
                            str_to_type(bot_type.main),
                            int(bot_value.main),
                            int(bot_another_property.text),
                            Team[team_select.main]
                        )
                    
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

            # Xử lí input box 
            for input_box in [bot_another_property]:
                input_box.handle_event(event)

         # Cập nhật màn hình
        pygame.display.flip()

        clock.tick(REFRESH_RATE)

def pvp_menu():
    # Tạo một số tiện ích

    num_box = InputBox(330, 125, 40, 40, resource.get_font(30, 0),
                       "Black", "Red", "Số trận")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 450),
                          text_input="Bắt đầu", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 550),
                         text_input="Thoát", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 550),
                         text_input="Trở lại", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Bắt đầu vòng lặp trò chơi
    while True:
        # Nhận trạng thái trò chơi hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Vẽ menu chính
        # Vẽ nền
        bg_img, bg_pos = resource.background()
        SCREEN.blit(bg_img, bg_pos)

        menu_text = resource.get_font(70, 0).render("Nhập cuộc", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 60))
        SCREEN.blit(menu_text, menu_rect)

        # Vẽ chữ
        text = resource.get_font(60, 0).render("Black", True, "Black")
        rect = text.get_rect(center=(165, 185))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Player 1", True, "Black")
        rect = text.get_rect(center=(165, 225))
        SCREEN.blit(text, rect)

        text = resource.get_font(60, 0).render("Red", True, "#AB001B")
        rect = text.get_rect(center=(495, 185))
        SCREEN.blit(text, rect)

        text = resource.get_font(30, 0).render("Player 2", True, "#AB001B")
        rect = text.get_rect(center=(495, 225))
        SCREEN.blit(text, rect)

        # Vẽ nút
        for button in [start_button, quit_button, back_button]:
            button.draw(SCREEN)

        # Vẽ hộp nhập
        num_box.update()
        num_box.draw(SCREEN)

        # Xử lý sự kiện
        for event in events_list:
            # Thoát nếu bấm exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Xử lý khi bấm vào nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Nếu tất cả thông tin được điền đầy đủ
                # Trò chơi sẽ bắt đầu
                if start_button.check_for_input(mouse_pos):
                    if not num_box.text.isnumeric():
                        continue
                    pvp_screen()

                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

            num_box.handle_event(event)

        # Cập nhật màn hình
        pygame.display.flip()
        # Thời gian khung hình
        clock.tick(REFRESH_RATE)
def pvp_screen() -> None:
    """Hàm này là màn hình chơi giữa người với người"""
    # Tạo biến cho người chơi
    player_turn = True  # True nếu là lượt của người chơi Đỏ, False nếu là lượt của người chơi Đen
    player_gamestate = GameState.generate_initial_game_state()

    # Tạo biến di chuyển
    position_chosen, piece_chosen = None, None
    last_move = None

    # Tạo các nút
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="QUIT", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="BACK", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Bắt đầu vòng lặp cho trò chơi
    while True:
        # Lấy trạng thái hiện tại
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        win_status = player_gamestate.get_team_win()

        # Xử lí event
        for event in events_list:
            # Thoát trò chơi nếu bấm vào nút thoát
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Khi trò chơi kết thúc, thoát hoặc quay lại menu ban đầu
            if win_status is not Team.NONE and event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

        # Background
        SCREEN.fill(((241, 203, 157)))

        # Trạng thái trò chơi
        draw_gamestate(player_gamestate, player_turn is False)

        # Chọn
        if position_chosen is not None:
            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(position_chosen)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # Hiển thị hình ảnh của các vòng tròn tương ứng với nước đi cuối cùng
        if last_move is not None:
            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(last_move[0], player_turn is False)
            SCREEN.blit(chosen_ring_img, draw_pos)

            chosen_ring_img, draw_pos = resource.chosen_ring_sprite(last_move[1], player_turn is False)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # Nếu trò chơi kết thúc, hãy rút thông báo và nhấn nút
        if win_status is not Team.NONE:
            # Thông báo
            pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(0, 270, 660, 120))
            pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(4, 274, 652, 112))

            if win_status is Team.RED:
                text = resource.get_font(50, 0).render("Đỏ thắng!", True, "Black")
            elif win_status is Team.BLACK:
                text = resource.get_font(50, 0).render("Đen thắng!", True, "Black")
            else:
                text = resource.get_font(50, 0).render("Hòa!", True, "Black")
            rect = text.get_rect(center=(330.5, 330))
            SCREEN.blit(text, rect)

            # Buttons
            for button in [quit_button, back_button]:
                button.draw(SCREEN)

        # Xử lí di chuyển
        else:
            for event in events_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Tính toán vị trí nhấp chuột trong UI, vị trí nhấp chuột trong bảng trạng thái trò chơi
                    click_pos = resource.get_piece_position(mouse_pos)
                    board_pos = resource.get_piece_position(mouse_pos, player_turn is False)

                    # Nếu vị trí nhấp chuột nằm ngoài bảng hoặc trên quân cờ đã chọn => bỏ chọn quân cờ
                    if click_pos is None or click_pos == position_chosen:
                        position_chosen, piece_chosen = None, None
                        continue

                    notation = player_gamestate.board[board_pos[0]][board_pos[1]]
                    # Nếu quân cờ thuộc về người chơi hiện tại => chọn quân cờ đó
                    if Team[notation[0]] is (Team.RED if player_turn else Team.BLACK):
                        position_chosen = click_pos
                        piece_chosen = Piece.create_instance(
                            board_pos,
                            notation,
                            player_gamestate.board,
                            None, None
                        )

                    # Nếu vị trí nhấp chuột nằm trong danh sách các nước đi được phép của quân cờ đã chọn
                    elif piece_chosen is not None and board_pos in piece_chosen.admissible_moves:
                        new_gamestate = player_gamestate.generate_game_state_with_move(piece_chosen.position, board_pos)
                        # Nếu nước đi hợp lệ thì di chuyển đến vị trí đó
                        if new_gamestate is not None:
                            player_gamestate = new_gamestate[0]

                            last_move = (piece_chosen.position, board_pos)
                            position_chosen, piece_chosen = None, None
                            player_turn = not player_turn

        # Cập nhật màn hình
        pygame.display.flip()

        # Đợi đến frame tiếp theo
        clock.tick(REFRESH_RATE)

if __name__ == "__main__":
    main_menu()
