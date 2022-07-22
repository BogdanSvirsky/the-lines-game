import pygame
import random
from players import Player

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


class GameField: # i want to realize scaling of game field
    def __init__(self, zero_x: int, zero_y: int) -> None:
        self.players: Player = [Player("Богдан", (0, 191, 255)), Player("Даня", (255, 99, 71))]
        self.delta_x, self.delta_y = 50, 50
        self.points: Point = [Point(zero_x + self.delta_x, zero_y + self.delta_y)]
        self.polygons: Polygon = []
        self.length_x = 500
        self.length_y = 500
        self.zero_x = zero_x
        self.zero_y = zero_y
        last_point = self.points[-1]
        self.current_player = 0
        self.POINT_SIZE = 7

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
        pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(self.zero_x, self.zero_y, self.length_x, self.length_y), border_radius=8, )
        
        for point in self.points:
            if point.host != None:
                color = self.players[point.host].color
            else:
                color = (20, 20, 20)
            pygame.draw.polygon(screen, color, [(point.x - self.POINT_SIZE, point.y), (point.x, point.y + self.POINT_SIZE), (point.x + self.POINT_SIZE, point.y), (point.x, point.y - self.POINT_SIZE)])
        for polygon in self.polygons:
            if polygon.selected:
                coords = polygon.coords + [(mouse_x, mouse_y)]
            else:
                coords = polygon.coords
            pygame.draw.polygon(screen, self.players[polygon.host].color, coords)
