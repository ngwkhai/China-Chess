import sys

import pygame
import resource
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
                    pass
                if pvp_button.check_for_input(mouse_pos):
                    pass
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

def pve_menu() -> None:
    # Tạo giao diện menu 

    bot_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 270, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS", "DyMinimax", "DeMinimax", "ExMinimax"]) # Chọn thuật toán

    bot_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 270, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["0", "1", "2"])

    team_select = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        430, 220, 150, 50,
        pygame.font.SysFont(None, 30),
        "Team", ["BLACK", "RED"])

    bot_another_property = InputBox(165, 210, 40, 30, pygame.font.SysFont(
        None, 25), "Black", "Red", "Depth/Time allowed")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 430),
                          text_input="Simulate", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")


if __name__ == "__main__":
    main_menu()
