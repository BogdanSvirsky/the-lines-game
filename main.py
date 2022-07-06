import time
import pygame
import os
from game_field import GameField
from game_field import Button
from game_field import SelectOption

def render(game_field, mouse_x, mouse_y):
    game_field.render(screen, mouse_x, mouse_y)
    for element in elements:
        element.render(screen)
    render_scoreboard(game_field, 20)

def render_scoreboard(game_field, width: int):
    os.system('cls')
    print("Таблица счёта".center(width, ' '))
    print("-" * width)
    print('|', end='')
    for player in game_field.players:
        print(player.nickname.center(width // len(game_field.players)))
    for player in game_field.players:
        print(str(player.square).center(width // len(game_field.players)))
    time.sleep(1)


pygame.init()
BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode([700, 700])
pygame.display.set_caption("Линейная игра")
game_field = GameField(100, 50)
elements = [
    SelectOption("Текущий инструмент", ["Линейка", "Ручка"], 10, 600)
]
running = True
ruler_selected = False
pointer_selected = True

for player in game_field.players:
    print(f'{player.nickname}', end='\t')
print()
while running:
    os.system('cls')
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
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    if ruler_selected:
                        game_field.select_place(mouse_x, mouse_y)
                    if pointer_selected:
                        game_field.select_point(mouse_x, mouse_y)
                    for element in elements:
                        element.click(mouse_x, mouse_y)
    except Exception as a:
        print(a)
    screen.fill(BACKGROUND_COLOR)
    render(game_field, mouse_x, mouse_y)
    
    pygame.display.flip()


pygame.quit()
