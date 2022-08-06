import pygame
from game_field import GameField
from elements import PenTool
from elements import RulerTool
from elements import StatisticWidget


def render(game_field):
    game_field.render(screen)
    allsprites.update()
    allsprites.draw(screen)
    for player in game_field.players:
        player.update()
    statistic.render(screen)

pygame.init()
BACKGROUND_COLOR = (255, 255, 255)
screen = pygame.display.set_mode([600, 900])
pygame.display.set_caption("Линейная игра")
game_field = GameField(50, 190)
running = True
pen = PenTool(screen, 50, 725)
ruler = RulerTool(screen, 320, 725)
statistic = StatisticWidget(100, 60, game_field)
allsprites = pygame.sprite.Group(pen, ruler)
FPS = 60
clock = pygame.time.Clock()

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("\nclose")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ruler.unselect(game_field)
                    pen.unselect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    if pen.is_clicked:
                        if pen.select_point(game_field, mouse_x, mouse_y):
                            continue
                    elif ruler.is_clicked:
                        info = ruler.select_place(game_field, mouse_x, mouse_y)
                        print(info)
                        if info:
                            continue
                    if pen.click(mouse_x, mouse_y):
                        if pen.is_clicked:
                            ruler.unselect(game_field)
                    elif ruler.click(mouse_x, mouse_y):
                        if ruler.is_clicked:
                            pen.unselect()
        screen.fill(BACKGROUND_COLOR)
        render(game_field)
        pygame.display.flip()
        clock.tick(FPS)
except Exception as a:
    print(a)
pygame.quit()
