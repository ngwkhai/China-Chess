import sys

import pygame
import resource
from game_state import GameState
from game_tree import GameTree
from team import Team
from cmath import inf
from gui_utilities import Button, InputBox, DropDown

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
        menu_text = resource.get_font(70, 0).render("Chọn Bots", True, "Black")
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

# def pve_screen(
#     bot_type: GameTree,
#     bot_value: int,
#     bot_another_property: int,
#     player_team: Team
# ) -> None:

#     # Tạo biến cho bot
#     bot = bot_type(Team.get_reverse_team(player_team), bot_another_property, bot_value)
#     is_bot_process = False

#     # Tạo biến cho người chơi
#     player_turn = player_team is Team.RED
#     player_gamestate = GameState.generate_initial_game_state()

#     # Tạo biến di chuyển 
#     position_chosen, piece_chosen = None, None
#     last_move = None

#     #
#     quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
#                          text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

#     back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
#                          text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

#     # Bắt đầu vòng lặp cho trò chơi
#     while True:
#         # Lấy trạng thái hiện tại
#         mouse_pos = pygame.mouse.get_pos()
#         events_list = pygame.event.get()
#         win_status = player_gamestate.get_team_win()

#         # Xử lí event
#         for event in events_list:
#             # Thoát trò chơi nếu bấm vào nút thoát
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             # Khi trò chơi kết thúc, thoát hoặc quay lại menu ban đầu
#             if win_status is not Team.NONE and event.type == pygame.MOUSEBUTTONDOWN:
#                 if quit_button.check_for_input(mouse_pos):
#                     pygame.quit()
#                     sys.exit()
#                 if back_button.check_for_input(mouse_pos):
#                     pve_menu()

#         # .Background
#         SCREEN.fill(((241, 203, 157)))

#         # Trạng thái trò chơi
#         draw_gamestate(player_gamestate, player_team is Team.BLACK)

#         # Chọn
#         if position_chosen is not None:
#             chosen_ring_img, draw_pos = resources.chosen_ring_sprite(position_chosen)
#             SCREEN.blit(chosen_ring_img, draw_pos)

#         # Hiển thị hình ảnh của các vòng tròn tương ứng với nước đi cuối cùng
#         if last_move is not None:
#             chosen_ring_img, draw_pos = resources.chosen_ring_sprite(last_move[0], player_team is Team.BLACK)
#             SCREEN.blit(chosen_ring_img, draw_pos)

#             chosen_ring_img, draw_pos = resources.chosen_ring_sprite(last_move[1], player_team is Team.BLACK)
#             SCREEN.blit(chosen_ring_img, draw_pos)

#         # Nếu trò chơi kết thúc, hãy rút thông báo và nhấn nút
#         if win_status is not Team.NONE:
#             # Thông báo
#             pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(0, 270, 660, 120))
#             pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(4, 274, 652, 112))

#             if win_status is player_team:
#                 text = resources.get_font(50, 0).render("Xin chúc mừng, bạn đã thắng.", True, "Black")
#             else:
#                 text = resources.get_font(50, 0).render("Chúc bạn may mắn lần sau.", True, "Black")
#             rect = text.get_rect(center=(330.5, 330))
#             SCREEN.blit(text, rect)

#             # Buttons
#             for button in [quit_button, back_button]:
#                 button.draw(SCREEN)

#         # Xử lí di chuyển
#         else:
#             # Lượt người chơi
#             if player_turn:
#                 for event in events_list:
#                     if event.type == pygame.MOUSEBUTTONDOWN:
#                         # Tính toán vị trí nhấp chuột trong UI, vị trí nhấp chuột trong bảng trạng thái trò chơi
#                         click_pos = resources.get_piece_position(mouse_pos)
#                         board_pos = resources.get_piece_position(mouse_pos, player_team is Team.BLACK)

#                        # Nếu vị trí nhấp chuột nằm ngoài bảng hoặc trên quân cờ đã chọn => bỏ chọn quân cờ
#                         if click_pos is None or click_pos == position_chosen:
#                             position_chosen, piece_chosen = None, None
#                             continue

#                         notation = player_gamestate.board[board_pos[0]][board_pos[1]]
#                         # Nếu quân cờ thuộc về người chơi => chọn quân cờ đó
#                         if Team[notation[0]] is player_team:
#                             position_chosen = click_pos
#                             piece_chosen = Piece.create_instance(
#                                 board_pos, 
#                                 notation, 
#                                 player_gamestate.board, 
#                                 None, None
#                             )

#                         # Nếu vị trí nhấp chuột nằm trong danh sách các nước đi được phép của quân cờ đã chọn
#                         elif piece_chosen is not None and board_pos in piece_chosen.admissible_moves:
#                             new_gamestate = player_gamestate.generate_game_state_with_move(piece_chosen.position, board_pos)
#                             # Nếu nước đi hợp lệ thì di chuyển đến vị trí đó
#                             if new_gamestate is not None:
#                                 player_gamestate = new_gamestate[0]
#                                 bot.move_to_child_node_with_move(piece_chosen.position, board_pos)

#                                 last_move = (piece_chosen.position, board_pos)
#                                 position_chosen, piece_chosen = None, None
#                                 player_turn = False

#             # Lượt bot
#             else:
#                 # Xử lí bot
#                 if is_bot_process is False:
#                     # Tạo luồng chạy bot
#                     bot_thread = threading.Thread(
#                         target=bot.process, args=(moves_queue,))
#                     bot_thread.start()

#                     # Đánh dấu bot đã chạy
#                     is_bot_process = True

#                 # Di chuyển
#                 try:
#                     # Di chuyển quân 
#                     old_pos, new_pos = moves_queue.pop(0)
#                     player_gamestate = player_gamestate.generate_game_state_with_move(old_pos, new_pos)[0]

#                     # End the bot run thread
#                     bot_thread.join()

#                     # Post process
#                     is_bot_process = False
#                     player_turn = True
#                     last_move = (old_pos, new_pos)
#                 except IndexError:
#                     pass

#         # Cập nhật màn hình
#         pygame.display.flip()

#         # Đợi đến frame tiếp theo
#         clock.tick(REFRESH_RATE)


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

        menu_text = resource.get_font(70, 0).render("Chuẩn bị", True, "Black")
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

if __name__ == "__main__":
    main_menu()
