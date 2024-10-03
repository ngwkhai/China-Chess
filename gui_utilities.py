import pygame

class Button():
    def __init__(self, image,pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        self.change_color(mouse_pos)
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return (
            position[0] in range(self.rect.left, self.rect.right)
            and position[1] in range(self.rect.top, self.rect.bottom)
        )

    def change_color(self, position):
        if self.check_for_input(position):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)
class InputBox:
  
    def __init__(self, x, y, w, h, font, color_inactive, color_active, text=''):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - w/2, y - h/2, w, h)   # Hình chữ nhật đại diện cho vùng nhập hôp nhập liệu

        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = self.color_inactive

        self.font = font
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)

        self.active = False

    def handle_event(self, event):
        # Xử lí tương tác từ người dùng
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Người dùng click chuột vào hộp nhập liệu.
            if self.rect.collidepoint(event.pos):
                self.text = ''
                self.active = not self.active
            else:
                self.active = False
            # Đổi màu hộp
            self.color = self.color_active if self.active else self.color_inactive

    '''
    def update(self):
        # Resize the box if the text is too long.
        width = max(40, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.x = self.x - width/2
    '''

    def draw(self, screen):
        # Blit the text.
        rect = self.txt_surface.get_rect(center=(self.x, self.y))
        screen.blit(self.txt_surface, rect)
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)