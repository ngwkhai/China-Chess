import sys

import pygame
import resource
from gui_utilities import Button

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

def main_menu():
    """Hàm này là màn hình menu chính"""
    # Tạo các nút
    pve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(120, 350),
                        text_input="Người và máy", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    pvp_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330, 350),
                        text_input="PvP", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    eve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(530, 350),
                        text_input="EvE", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(330.5, 450),
                         text_input="QUIT", font=resource.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
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
        menu_text = resource.get_font(100, 0).render("MENU", True, "White")
        menu_rect = menu_text.get_rect(center = (330.5, 150))
        SCREEN.blit(menu_text, menu_rect)

        for button in [pve_button, pvp_button, eve_button, quit_button]:
            button.draw(SCREEN)

        # xử lý sự kiện
        for event in events_list:
            # Thoát khỏi trò chơi nếu nút QUIT được nhấp
            if event.type == pygame.QUIT:
                print("")
                pygame.quit()
                sys.exit()

            # Xử lý sự kiện bấm vào các nút
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pve_button.check_for_input(mouse_pos):
                    pass
                if pvp_button.check_for_input(mouse_pos):
                    pass
                if eve_button.check_for_input(mouse_pos):
                    pass
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()



        # Cập nhật màn hình
        pygame.display.flip()

        # Chờ khung hình tiếp theo
        clock.tick(REFRESH_RATE)



if __name__ == "__main__":
    main_menu()
