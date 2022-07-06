import pygame
import random
from players import Player


POINT_SIZE = 7


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.host = None


class Polygon:
    def __init__(self, x, y, n) -> None:
        self.coords = [(x, y)]
        self.selected = True
        self.host = n
    
    def add_coords(self, x, y):
        if (x == self.coords[0][0]) and (y == self.coords[0][1]):
            self.selected = False
        else:
            self.coords.append((x, y))


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


class GameField: # i want to realize scaling of game field
    def __init__(self, zero_x, zero_y) -> None:
        self.players: Player = [Player("Богдан", (255, 0, 0)), Player("Даня", (0, 0, 255))]
        self.delta_x, self.delta_y = 50, 50
        self.points: Point = [Point(zero_x + self.delta_x, zero_y + self.delta_y)]
        self.polygons: Polygon = []
        self.length_x = 500
        self.length_y = 500
        self.zero_x = zero_x
        self.zero_y = zero_y
        last_point = self.points[-1]
        self.current_player = 0

        while (last_point.x + self.delta_x < self.zero_x + self.length_x) or (last_point.y + self.delta_y < self.zero_y + self.length_y):
            if (last_point.x + self.delta_x < self.zero_x + self.length_x) and (last_point.y + self.delta_y < self.zero_y + self.length_y):
                self.points.append((Point(last_point.x + self.delta_x, last_point.y)))
            elif last_point.x + self.delta_x >= self.zero_x + self.length_x:
                self.points.append((Point(self.zero_x + self.delta_x, last_point.y + self.delta_y)))
            elif (last_point.y + self.delta_y >= self.zero_y + self.length_y) and (last_point.x + self.delta_x < self.zero_x + self.length_x):
                self.points.append((Point(last_point.x + self.delta_x, last_point.y)))
            print(len(self.points), (self.length_x // self.delta_x) * (self.length_y // self.delta_y))
            last_point = self.points[-1]
    
    def render(self, screen, mouse_x, mouse_y) -> None:
        POINT_SIZE = 7
        pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(self.zero_x, self.zero_y, self.length_x, self.length_y), border_radius=8, )
        
        for point in self.points:
            if point.host:
                color = self.players[point.host].color
            else:
                color = (20, 20, 20)
            pygame.draw.polygon(screen, color, [(point.x - POINT_SIZE, point.y), (point.x, point.y + POINT_SIZE), (point.x + POINT_SIZE, point.y), (point.x, point.y - POINT_SIZE)])
        for polygon in self.polygons:
            if polygon.selected:
                coords = polygon.coords + [(mouse_x, mouse_y)]
            else:
                coords = polygon.coords
            pygame.draw.polygon(screen, self.players[polygon.host].color, coords)
    
    def select_point(self, x, y) -> bool:
        for i in range(len(self.points)):
            point = self.points[i]
            if (point.x - POINT_SIZE <= x <= point.x + POINT_SIZE) and (point.y - POINT_SIZE <= y <= point.y + POINT_SIZE):
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

    def select_place(self, x, y) -> bool:
        for i in range(len(self.points)):
            point = self.points[i]
            if (point.x - POINT_SIZE <= x <= point.x + POINT_SIZE) and (point.y - POINT_SIZE <= y <= point.y + POINT_SIZE):
                if self.polygons[-1].selected:
                    self.polygons[-1].add_coords(point.x, point.y)
                else:
                    self.polygons.append(Polygon(point.x, point.y, self.current_player))
                return True
        else:
            return False
