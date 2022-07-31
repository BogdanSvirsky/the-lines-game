import pygame


class Player:
    def __init__(self, nickname, color, game_field, num) -> None:
        self.square = 0
        self.nickname = nickname
        self.color = color
        self.game_field = game_field
        self.number = num

    def update(self):
        count_points_out = 0
        count_points_in = 0
        in_figure = False
        for polygon in self.game_field.polygons:
            if self.number == polygon.host:
                count_points_in = len(polygon.coords)
                for player_point in polygon.coords:
                    for point in self.game_field.points:
                        if point.x > player_point[0] and point.y > player_point[1]:
                            if self.number == point.host:
                                break
                            else:
                                count_points_in += 1
        if count_points_out:
            self.square = count_points_in + count_points_out / 2 - 1
