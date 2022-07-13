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
        self.is_clicked = True
        self.screen = screen
    
    def select_point(self, game_field: GameField, x, y) -> bool:
        for i in range(len(game_field.points)):
            point = game_field.points[i]
            if (point.x - game_field.POINT_SIZE <= x <= point.x + game_field.POINT_SIZE) and (point.y - game_field.POINT_SIZE <= y <= point.y + game_field.POINT_SIZE):
                print(i, len(game_field.points))
                if not game_field.points[i].host:
                    game_field.points[i].host = game_field.current_player
                    if game_field.current_player < len(game_field.players) - 1:
                        game_field.current_player += 1
                    else:
                        game_field.current_player = 0
                    return True
        else:
            return False
        
    def update(self):
        color = (0, 0, 0)
        if self.is_clicked:
            self.image, self.rect = load_image("pen_icon_selected.png", -1)
        else:
            self.image, self.rect = load_image("pen_icon.png", -1)
        self.rect.move_ip(self.x, self.y)
        if self.is_clicked:
            pygame.draw.rect(self.screen, color, self.rect, border_radius=3)
        
    def click(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.rect_image.width:
            if self.y <= mouse_y <= self.rect_image.height:
                self.is_clicked = not self.is_clicked
                return True
            else:
                return False
        else:
            return False


class RulerTool(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_clicked = False
        self.screen = screen
        self.image, self.rect = load_image("ruler_icon.png", -1)
    
    def select_place(self, game_field: GameField, x, y) -> bool:
        for i in range(len(game_field.points)):
            point = game_field.points[i]
            if (point.x - game_field.POINT_SIZE <= x <= point.x + game_field.POINT_SIZE) and (point.y - game_field.POINT_SIZE <= y <= point.y + game_field.POINT_SIZE):
                if game_field.polygons[-1].selected:
                    game_field.polygons[-1].add_coords(point.x, point.y)
                else:
                    game_field.polygons.append(Polygon(point.x, point.y, game_field.current_player))
                return True
        else:
            return False

    def render(self, screen):
        pass
    
    def click(self, mouse_x, mouse_y):
        pass