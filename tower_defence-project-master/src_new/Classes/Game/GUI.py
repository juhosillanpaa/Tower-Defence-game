import pygame
import pygame_gui
from ..ShopItem.ShopItem import ShopItem
from ..Tower.BlueTower import BlueTower
from ..Tower.RedTower import RedTower

BLACK = (0, 0, 0)
GREY = pygame.Color(200, 200, 200)
DARK = (40,40,40)
WHITE = (255,255,255)


class GUI:
    def __init__(self, window_surface, game_surface, toolbox_surface, stat_surface, game, manager):
        self.window_surface = window_surface
        self.game_surface = game_surface
        self.toolbox_surface = toolbox_surface
        self.stat_surface = stat_surface
        self.game = game
        self.manager = manager

        self.buy_blue = ShopItem(
            game=game,
            toolbox_surface=toolbox_surface,
            toolbox_pos=(150, 0),
            window_surface=window_surface,
            tower=BlueTower,
            image_url="utility/images/blue_tower/blue_tower.png",
            price=100
        )
        self.buy_red = ShopItem(
            game=game,
            toolbox_surface=toolbox_surface,
            toolbox_pos=(300, 0),
            window_surface=window_surface,
            tower=RedTower,
            image_url="utility/images/red_tower/red_tower.png",
            price=150
        )
        self.start_round_btn = self.create_start_round_btn()

    def create_start_round_btn(self):
        pos = self.toolbox_surface.get_offset()
        x = pos[0] + 10
        y = pos[1] + 25
        start_round_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (100, 50)),
            text="Start round",
            manager=self.manager,
        )
        return start_round_btn

    def listen_mouse_events(self, event):
        self.buy_blue.listen_mouse_events(event)
        self.buy_red.listen_mouse_events(event)

    def listen_pygame_user_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_round_btn:
                    self.game.start_round()

    def run_iteration(self):
        if self.game.won or self.game.lost:
            self.draw_end_view()
            return
        self.stat_surface.fill(GREY)
        self.buy_blue.update_and_draw()
        self.buy_red.update_and_draw()
        self.draw_level_text()
        self.draw_base_hp()
        self.draw_gold_amount()
        if self.game.level_started:
            self.start_round_btn.hide()
        else:
            self.start_round_btn.show()


    def draw_level_text(self):
        text = 'Level: ' + str(self.game.get_current_level_number())
        font = pygame.font.SysFont('arial', 24, False)
        img = font.render(text, True, BLACK)
        self.stat_surface.blit(img, (20, 20))

    def draw_base_hp(self):
        text = 'Castle health: ' + str(self.game.get_hp())
        font = pygame.font.SysFont('arial', 20, False)
        img = font.render(text, True, BLACK)
        self.stat_surface.blit(img, (20,100))

    def draw_gold_amount(self):
        text = 'Gold: ' + str(self.game.money)
        font = pygame.font.SysFont('arial', 20, False)
        img = font.render(text, True, BLACK)
        self.stat_surface.blit(img, (20,130))

    def draw_end_view(self):
        text = 'You won!' if self.game.won else 'You lost'
        self.window_surface.fill(DARK)
        font = pygame.font.SysFont('arial', 20, True)
        img = font.render(text, True, WHITE)
        self.window_surface.blit(img, (400, 300))
