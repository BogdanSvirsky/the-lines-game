import pygame
from game_field import GameField
from game_field import Polygon


def select_point(self: GameField, x, y) -> bool:
    for i in range(len(self.points)):
        point = self.points[i]
        if (point.x - self.POINT_SIZE <= x <= point.x + self.POINT_SIZE) and (point.y - self.POINT_SIZE <= y <= point.y + self.POINT_SIZE):
            print(i, len(self.points))
            if not self.points[i].host:
                self.points[i].host = self.current_player
                if self.current_player < len(self.players) - 1:
                    self.current_player += 1
                else:
                    self.current_player = 0
                return True
    else:
        return False

def select_place(self: GameField, x, y) -> bool:
    for i in range(len(self.points)):
        point = self.points[i]
        if (point.x - self.POINT_SIZE <= x <= point.x + self.POINT_SIZE) and (point.y - self.POINT_SIZE <= y <= point.y + self.POINT_SIZE):
            if self.polygons[-1].selected:
                self.polygons[-1].add_coords(point.x, point.y)
            else:
                self.polygons.append(Polygon(point.x, point.y, self.current_player))
            return True
    else:
        return False


class SelectOption:
    def __init__(self, title: str, options: list, x: int, y: int) -> None:
        self.options = options
        self.title = title
        self.x = x
        self.y = y
    
    def render(self, screen):
        text_scale = 45
        font_title = pygame.font.Font(None, text_scale)
        text_title = font_title.render(self.title, True, (10, 10, 10))
        screen.blit(text_title, (self.x, self.y))
        delta = text_title.get_rect().height
        for i in range(len(self.options)):
            font_option = pygame.font.Font(None, text_scale - 10)
            text_option = font_option.render(self.options[i], True, (10, 10, 10))
            screen.blit(text_option, (self.x + 55, self.y + delta * (i + 1) + 5))
            radius = text_option.get_rect().height // 2 - 5
            pygame.draw.circle(screen, (10, 10, 10), (self.x + 55 - delta, self.y + int(delta * (i + 1.5)) + 5), radius, width=3)
            pygame.draw.circle(screen, (10, 10, 10), (self.x + 55 - delta, self.y + int(delta * (i + 1.5)) + 5), radius - 4)
    
    def click(self, x, y):
        for i in range(len(self.options)):
            pass


class Button:
    def __init__(self, x, y, w, h, text=None) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.is_clicked = False
    
    def render(self, screen):
        BORDER_RADUIS = 8
        if self.is_clicked:
            # clicked = True
            font = pygame.font.Font(None, 35)
            text = font.render(self.text, True, (255, 255, 255))
            main_rect = pygame.Rect(self.x, self.y, self.w, self.h)
            pygame.draw.rect(screen, (0, 0, 0), main_rect, border_radius=BORDER_RADUIS)
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(self.x, self.y, self.w, self.h - 7), border_radius=BORDER_RADUIS)
            screen.blit(text, (main_rect.centerx - text.get_rect().width // 2, main_rect.centery - text.get_rect().height // 2))
        else:
            # clicked = False
            font = pygame.font.Font(None, 35)
            text = font.render(self.text, True, (255, 255, 255))
            main_rect = pygame.Rect(self.x, self.y, self.w, self.h)
            pygame.draw.rect(screen, (0, 0, 0), main_rect, border_radius=BORDER_RADUIS)
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.x, self.y, self.w, self.h - 7), border_radius=BORDER_RADUIS)
            screen.blit(text, (main_rect.centerx - text.get_rect().width // 2, main_rect.centery - text.get_rect().height // 2))
    
    def click(self, x, y):
        if (self.x <= x <= self.x + self.w) and (self.y <= y <= self.y + self.h):
            if self.is_clicked:
                self.is_clicked = False
            else:
                self.is_clicked = True
        elif self.is_clicked:
            self.is_clicked = False