import time
import pygame
import os
from game_field import GameField
from elements import PenTool
from elements import RulerTool

def render(game_field, mouse_x, mouse_y):
    game_field.render(screen, mouse_x, mouse_y)
    for element in elements:
        element.render(screen)
    allsprites.update()
    allsprites.draw(screen)
    print("render is complete ;)", end='\r')

def render_scoreboard(game_field, width: int):
    os.system('cls')
    print("Таблица счёта".center(width, ' '))
    print("-" * width)
    print('|', end='')
    for player in game_field.players:
        print(player.nickname.center(width // len(game_field.players)))
    for player in game_field.players:
        print(str(player.square).center(width // len(game_field.players)))


pygame.init()
BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode([700, 700])
pygame.display.set_caption("Линейная игра")
game_field = GameField(100, 50)
elements = []
running = True
pen = PenTool(screen, 600, 0)
ruler = RulerTool(screen, 0, 0)
allsprites = pygame.sprite.Group(pen, ruler)

for player in game_field.players:
    print(f'{player.nickname}', end='\t')
print()
while running:
    mouse_x, mouse_y = 0, 0
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("\nclose")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    for element in elements:
                        element.click(mouse_x, mouse_y)
                    if pen.is_clicked:
                        pen.select_point(game_field, mouse_x, mouse_y)
                    elif ruler.is_clicked:
                        ruler.select_place(game_field, mouse_x, mouse_y)
    except Exception as a:
        print(a)
    screen.fill(BACKGROUND_COLOR)
    render(game_field, mouse_x, mouse_y)
    
    pygame.display.flip()


pygame.quit()
