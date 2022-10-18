import pygame
from game_field import GameField
from elements import PenTool
from elements import RulerTool
from elements import StatisticWidget
from elements import Button
from elements import MenuButton



class MainMenu:
    pass


class GameWindow:
    def __init__(self, screen) -> None:
        self.game_field = GameField(50, 190)
        self.pen = PenTool(screen, 50, 725)
        self.ruler = RulerTool(screen, 320, 725)
        self.pause_button = MenuButton(500, 0)
        self.statistic = StatisticWidget(100, 60, self.game_field)
        self.allsprites = pygame.sprite.Group(self.pen, self.ruler, self.pause_button)
        self.screen = screen
    
    def render(self):
        BACKGROUND_COLOR = (255, 255, 255)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ruler.unselect(self.game_field)
                    self.pen.unselect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    if self.pen.is_clicked:
                        if self.pen.select_point(self.game_field, mouse_x, mouse_y):
                            continue
                    elif self.ruler.is_clicked:
                        info = self.ruler.select_place(self.game_field, mouse_x, mouse_y)
                        print(info)
                        if info:
                            continue
                    if self.pen.click(mouse_x, mouse_y):
                        if self.pen.is_clicked:
                            self.ruler.unselect(self.game_field)
                    elif self.ruler.click(mouse_x, mouse_y):
                        if self.ruler.is_clicked:
                            self.pen.unselect()
        # ------------ Render part ------------
        self.screen.fill(BACKGROUND_COLOR)
        self.game_field.render(self.screen)
        self.allsprites.update()
        self.allsprites.draw(self.screen)
        for player in self.game_field.players:
            player.update()
        self.statistic.render(screen)
        print("render complete ;)")


class PauseMenu:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.buttons = [
            Button(screen.get_rect().centerx - 125, screen.get_rect().centery - 65, 250, 50, text="Завершить игру"),
            Button(screen.get_rect().centerx - 125, screen.get_rect().centery, 250, 50, text="Помощь"),
            Button(screen.get_rect().centerx - 125, screen.get_rect().centery + 65, 250, 50, text="Главное меню")
        ]
        font = pygame.font.SysFont("Comic Sans Ms", 37)
        self.text = font.render("Меню паузы", True, (255, 255, 255))
        self.textpos = self.text.get_rect(centerx=screen.get_rect().centerx, y=screen.get_rect().centery - 137)
    
    def render(self):
        BACKGROUND_COLOR = (51, 153, 102)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nclose")
                return True
        self.screen.fill(BACKGROUND_COLOR)
        # pygame.draw.rect(self.screen, (0, 204, 0), pygame.Rect(self.screen.get_rect().centerx - 150, 290, 300, 300), border_radius=5)
        self.screen.blit(self.text, self.textpos)
        for button in self.buttons:
            button.render(self.screen)



class WindowsManager:
    def __init__(self, screen, game_window, main_menu, pause_menu) -> None:
        self.screen = screen
        self.game_window = game_window
        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.windows = {
            "game_window": self.game_window,
            "main_menu": self.main_menu,
            "pause_menu": self.pause_menu
        }
        self.current_window = "main_menu"
    
    def switch_window(self, new_window):
        self.current_window = new_window
    
    def render(self):
        self.current_window.render()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([600, 900])
    pygame.display.set_caption("Линейная игра")
    running = True
    pause_menu = PauseMenu(screen)
    game_window = GameWindow(screen)
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("\nclose")
            pause_menu.render()
            pygame.display.flip()
    except Exception as a:
        print(a)
    pygame.quit()