import pygame
from game_field import GameField
from game_field import Polygon


class PenTool: # i want to make tool for move and scale a game field, pointer tool and ruler tool
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.is_clicked = True
    
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
        
    def render(self, screen):
        if self.is_clicked:
            pass
        else:
            pass

    def click(self, mouse_x, mouse_y):
        pass


class RulerTool:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.is_clicked = False
    
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
