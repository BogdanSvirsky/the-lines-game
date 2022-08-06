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
        for polygon in self.game_field.polygons:
            if self.number == polygon.host and not polygon.is_selected:
                count_points_in, count_points_out = check_polygon_params(polygon, self.game_field)[:2]
                self.square += count_points_in + count_points_out / 2 - 1


def check_polygon_params(polygon, game_field):
    DEBUG = False
    opponents_point = False
    count_points_in = 0
    count_points_out = len(polygon.coords)
    for player_point in polygon.coords:
        line_count = 0
        in_line = False
        for point in game_field.points:
            if point.host != polygon.host or in_line:
                if polygon.host == point.host:
                    hypo = False
                    for subpoint in polygon.coords:
                        if subpoint[0] == point.x and subpoint[1] == point.y:
                            hypo = True
                    if hypo:
                        if DEBUG: print(point.x, point.y, "host point")
                        in_line = False
                        break
                if not in_line:
                    if (point.y == player_point[1] and point.x > player_point[0]):
                        if DEBUG: print("line was started")
                        in_line = True
                        line_count += 1
                elif in_line and point.x > game_field.zero_x + game_field.length_x - game_field.delta_x * 2:
                    if DEBUG: print(point.x, point.y, "end of line")
                    break
                else:
                    line_count += 1
                    if DEBUG: print(point.x, point.y, "|", game_field.zero_x + game_field.length_x - game_field.delta_x * 2, "check")
                if in_line:
                    if point.host and point.host != polygon.host:
                        opponents_point = True
        if not in_line:
            if DEBUG: print(line_count, "count")
            count_points_in += line_count
        else:
            if DEBUG: print("opponent's point not here")
            opponents_point = False
    return count_points_in, count_points_out, opponents_point
