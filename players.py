import pygame


class Player:
    def __init__(self, nickname, color, game_field, num) -> None:
        self.square = 0
        self.nickname = nickname
        self.color = color
        self.game_field = game_field
        self.number = num

    def update(self):
        self.square = 0
        count_points_out = 0
        count_points_in = 0
        line_count = 0
        for polygon in self.game_field.polygons:
            if self.number == polygon.host and not polygon.is_selected:
                count_points_out = len(polygon.coords)
                for player_point in polygon.coords:
                    line_count = 0
                    in_line = False
                    for point in self.game_field.points:
                        if point.host != self.number or in_line:
                            if self.number == point.host:
                                hypo = False
                                for subpoint in polygon.coords:
                                    if subpoint[0] == point.x and subpoint[1] == point.y:
                                        hypo = True
                                if hypo:
                                    print(point.x, point.y, "host point")
                                    in_line = False
                                    break
                            if not in_line:
                                if (point.y == player_point[1] and point.x > player_point[0]):
                                    print("line was started")
                                    in_line = True
                                    line_count += 1
                            elif in_line and point.x > self.game_field.zero_x + self.game_field.length_x - self.game_field.delta_x * 2:
                                print(point.x, point.y, "end of line")
                                break
                            else:
                                line_count += 1
                                print(point.x, point.y, "|", self.game_field.zero_x + self.game_field.length_x - self.game_field.delta_x * 2, "check")
                    if not in_line:
                        print(line_count, "count")
                        count_points_in += line_count
                self.square += count_points_in + count_points_out / 2 - 1
