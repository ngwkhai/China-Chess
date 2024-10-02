import pygame
import resource
from gui_utilities import Button

# Khởi tạo pygame
pygame.init()

# Cài đặt cửa sổ
SCREEN = pygame.display.set_mode((660, 664))
pygame.display.set_caption("CỜ TƯỚNG")
pygame.display.set_icon(resource.icon())

def main_menu():
    """Hàm này là màn hình menu chính"""
    # Tạo các nút
    pve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(120, 350),
                        text_input="PvE", font=resource.get_font(40, 0), base_color="#AB001B", hovering_color="Black")
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
        events = pygame.event.get()

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


        # Cập nhật màn hình
        pygame.display.flip()



if __name__ == "__main__":
    main_menu()
