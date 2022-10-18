from turtle import width
import pygame
import os
from game_field import GameField
from game_field import Polygon


def load_image(name, colorkey=None, scale=1): # this was taken from the official pygame website
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "resources")
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


class PenTool(pygame.sprite.Sprite): # i want to make tool for move and scale a game field, pointer tool and ruler tool
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_clicked = False
        self.screen = screen
        self.update()
    
    def select_point(self, game_field: GameField, x, y) -> bool:
        for i in range(len(game_field.points)):
            point = game_field.points[i]
            if (point.x - game_field.POINT_SIZE <= x <= point.x + game_field.POINT_SIZE) and (point.y - game_field.POINT_SIZE <= y <= point.y + game_field.POINT_SIZE):
                print(i, len(game_field.points))
                if game_field.points[i].host == None:
                    game_field.points[i].host = game_field.current_player
                    if game_field.current_player < len(game_field.players) - 1:
                        game_field.current_player += 1
                    else:
                        game_field.current_player = 0
                    return True
        else:
            return False
        
    def update(self):
        indent = 20
        if self.is_clicked:
            self.image, self.rect = load_image("pen_icon_selected.png")
        else:
            self.image, self.rect = load_image("pen_icon.png", -1)
        self.rect.move_ip(self.x, self.y)
        if self.is_clicked:
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render("Ручка", True, (255, 255, 255))
            textpos = text.get_rect(centery=self.rect.centery + 3, x=self.x + self.rect.width + indent)
            w = self.rect.width + textpos.width + indent * 2.5
            h = self.rect.height + indent
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.x - indent // 2, self.y - indent // 2, w, h), border_radius=10)
            self.screen.blit(text, textpos)
        else:
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render("Ручка", True, (0, 0, 0))
            textpos = text.get_rect(centery=self.rect.centery + 3, x=self.x + self.rect.width + indent)
            self.screen.blit(text, textpos)
            w = self.rect.width + textpos.width + indent * 2.5
            h = self.rect.height + indent
        self.w, self.h = w, h
        
    def click(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.w:
            if self.y <= mouse_y <= self.y + self.h:
                self.is_clicked = not self.is_clicked
                print("pen was clicked")
                return True
            else:
                return False
        else:
            return False
    
    def unselect(self):
        self.is_clicked = False
        self.update()


class RulerTool(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_clicked = False
        self.screen = screen
        self.update()
    
    def select_place(self, game_field: GameField, x, y) -> bool:
        for point in game_field.points:
            if (point.x - game_field.POINT_SIZE <= x <= point.x + game_field.POINT_SIZE) and (point.y - game_field.POINT_SIZE <= y <= point.y + game_field.POINT_SIZE):
                if game_field.current_player == point.host:
                    if game_field.polygons and game_field.polygons[-1].is_selected:
                        game_field.polygons[-1].add_coords(point.x, point.y)
                    else:
                        game_field.polygons.append(Polygon(point.x, point.y, game_field.current_player, game_field))
                    return True
        else:
            return False

    def update(self):
        indent = 20
        if self.is_clicked:
            self.image, self.rect = load_image("ruler_icon_selected.png")
        else:
            self.image, self.rect = load_image("ruler_icon.png", -1)
        self.rect.move_ip(self.x, self.y)
        if self.is_clicked:
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render("Линейка", True, (255, 255, 255))
            textpos = text.get_rect(centery=self.rect.centery + 3, x=self.x + self.rect.width + indent)
            w = self.rect.width + textpos.width + indent * 2.5
            h = self.rect.height + indent
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.x - indent // 2, self.y - indent // 2, w, h), border_radius=10)
            self.screen.blit(text, textpos)
        else:
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render("Линейка", True, (0, 0, 0))
            textpos = text.get_rect(centery=self.rect.centery + 3, x=self.x + self.rect.width + indent)
            self.screen.blit(text, textpos)
            w = self.rect.width + textpos.width + indent * 2.5
            h = self.rect.height + indent
        self.w, self.h = w, h

    def unselect(self, game_field: GameField):
        self.is_clicked = False
        if game_field.polygons:
            if not self.is_clicked and game_field.polygons[-1].is_selected:
                game_field.polygons.pop(-1)
        self.update()

    def click(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.w:
            if self.y <= mouse_y <= self.y + self.h:
                self.is_clicked = not self.is_clicked
                print("ruler was clicked")
                return True
            else:
                return False
        else:
            return False


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_clicked = False
        self.update()

    def update(self):
        if self.is_clicked:
            self.image, self.rect = load_image("menu_button_selected.png")
        else:
            self.image, self.rect = load_image("menu_button.png", -1)
        self.rect.move_ip(self.x, self.y)

    def unselect(self):
        self.is_clicked = False
        self.update()
    
    def click(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.w:
            if self.y <= mouse_y <= self.y + self.h:
                self.is_clicked = not self.is_clicked
                print("pause_button was clicked")
                return True
            else:
                return False
        else:
            return False


class StatisticWidget:
    def __init__(self, x, y, game_field: GameField) -> None:
        self.game_field = game_field
        self.x = x
        self.y = y
    
    def render(self, screen):
        indent = 20
        textdata_list = []
        font_title = pygame.font.SysFont("Calibri", 33)
        text_title = font_title.render("Количество очков:", True, (0, 0, 0))
        text_title_pos = text_title.get_rect(centerx=screen.get_rect().centerx, y=self.y)
        screen.blit(text_title, text_title_pos)
        for i in range(len(self.game_field.players)):
            color = self.game_field.players[i].color
            font = pygame.font.SysFont("Calibri", 40)
            if i == self.game_field.current_player:
                font.underline = True
            text = font.render(f"{self.game_field.players[i].nickname}: {self.game_field.players[i].square}", True, (0, 0, 0))
            if textdata_list:
                if textdata_list[-1][-1].x >= screen.get_rect().centerx // 2:
                    if i + 1 == len(self.game_field.players):
                        textpos = text.get_rect(y=textdata_list[-1][-1].y + textdata_list[-1][-1].height + indent, centerx=screen.get_rect().centerx)
                    else:
                        textpos = text.get_rect(y=textdata_list[-1][-1].y + textdata_list[-1][-1].height + indent, centerx=screen.get_rect().centerx // 2)
                else:
                    textpos = text.get_rect(centery=textdata_list[-1][-1].centery, centerx=screen.get_rect().centerx * 1.5)
            else:
                textpos = text.get_rect(y=text_title_pos.height + self.y + indent, centerx=screen.get_rect().centerx // 2)
            textdata_list.append((text, color, textpos))

        for text, color, textpos in textdata_list:
            pygame.draw.rect(screen, color, text.get_rect(width=textpos.width + indent, height=textpos.height + indent, centerx=textpos.centerx, centery=textpos.centery), border_radius=7)
            screen.blit(text, textpos)                      


class Button:
    def __init__(self, x, y, w: int, h: int, text=None) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.is_clicked = False
    
    def render(self, screen):
        BUTTON_DEPTH = 6
        BORDER_RADUIS = 8
        BUTTON_COLOR = (204, 153, 0)
        BUTTON_SIDE_COLOR = (102, 77, 0)
        if self.is_clicked:
            # clicked = True
            font = pygame.font.SysFont("Cursive", 35)
            text = font.render(self.text, True, (255, 255, 255))
            main_rect = pygame.Rect(self.x + BUTTON_DEPTH - 3, self.y, self.w, self.h)
            pygame.draw.rect(screen, (0, 0, 0), main_rect, border_radius=BORDER_RADUIS)
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(self.x + BUTTON_DEPTH - 3, self.y, self.w, self.h - BUTTON_DEPTH), border_radius=BORDER_RADUIS)
            screen.blit(text, (main_rect.centerx - text.get_rect().width // 2, main_rect.centery - text.get_rect().height // 2))
        else:
            # clicked = False
            font = pygame.font.SysFont("Cursive", 35)
            text = font.render(self.text, True, (255, 255, 255))
            main_rect = pygame.Rect(self.x, self.y, self.w, self.h)
            pygame.draw.rect(screen, BUTTON_SIDE_COLOR, main_rect, border_radius=BORDER_RADUIS)
            pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(self.x, self.y, self.w, self.h - BUTTON_DEPTH), border_radius=BORDER_RADUIS)
            screen.blit(text, (main_rect.centerx - text.get_rect().width // 2, main_rect.centery - text.get_rect().height // 2))


class Camera:
    def __init__(self) -> None: # i don't know...
        pass