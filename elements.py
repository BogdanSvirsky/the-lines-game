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
        self.unselect()


class RulerTool(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_clicked = False
        self.screen = screen
        self.update()
    
    def select_place(self, game_field: GameField, x, y) -> bool:
        for i in range(len(game_field.points)):
            point = game_field.points[i]
            if (point.x - game_field.POINT_SIZE <= x <= point.x + game_field.POINT_SIZE) and (point.y - game_field.POINT_SIZE <= y <= point.y + game_field.POINT_SIZE):
                if point.host == game_field.current_player:
                    if not game_field.polygons[-1].selected or not game_field.polygons:
                        game_field.polygons.append(Polygon(point.x, point.y, game_field.current_player))
                    else:
                        game_field.polygons[-1].add_coords(point.x, point.y)
                    return True
                else:
                    print('\n', point.host)
                    return False
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

    def unselect(self):
        self.is_clicked = False
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


class StatisticWidget:
    def __init__(self, x, y, game_field: GameField) -> None:
        self.game_field = game_field
        self.x = x
        self.y = y
    
    def render(self, screen):
        indent = 20
        textdata_list = []
        for i in range(len(self.game_field.players)):
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render(f"{self.game_field.players[i].nickname}: {self.game_field.players[i].square}", True, (0, 0, 0))
            textpos = text.get_rect(centery=text.get_rect().centery + 3, x=self.x + text.get_rect().width + indent)
            w = textpos.width + indent * 2.5
            h = textpos.height + indent
            if textdata_list:
                x = textdata_list[-1][0] + textdata_list[-1][2] + indent * 2
            else:
                x = self.x
            y = self.y
            textdata_list.append((x, y, w, h, text, self.game_field.players[i].color))
        for textdata in textdata_list:
            x = textdata[0]
            y = textdata[1]
            w = textdata[2]
            h = textdata[3]
            color = textdata[-1]
            pygame.draw.rect(screen, color, pygame.Rect(x - indent, y - indent // 2, w - indent // 2, h), border_radius=10)
            screen.blit(textdata[-2], (x, y))


class HelpButton:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
