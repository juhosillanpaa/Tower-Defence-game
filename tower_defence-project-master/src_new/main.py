import pygame
import pygame_gui


from Classes.Tower.BlueTower import BlueTower
from Classes.Tower.RedTower import RedTower
from Classes.Game.Game import Game
from Classes.ShopItem.ShopItem import ShopItem
from Classes.Game.GUI import GUI


WHITE = (255, 255, 255)
FPS = 60
GREY = pygame.Color(200, 200, 200)
DARK = pygame.Color(50,50,50)



def main():
    pygame.init()
    pygame.display.set_caption("Tower defense")
    window = pygame.display.set_mode((1000, 800))

    game_started = False
    manager = pygame_gui.UIManager((1000, 800), 'theme.json')


    game_surface = window.subsurface((0, 0), (800, 600))
    game_surface.fill(DARK)

    toolbox_surface = window.subsurface((0, 600), (800,200))
    toolbox_surface.fill(GREY)

    stat_surface = window.subsurface((800, 0), (200, 800))
    stat_surface.fill(WHITE)

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 300), (100, 50)),
        text="Start game",
        manager=manager
    )

    game = Game(
        config_path="utility/default_map.txt",
        game_surface=game_surface,
    )
    gui = GUI(
        window_surface=window,
        game_surface=game_surface,
        toolbox_surface=toolbox_surface,
        stat_surface=stat_surface,
        game=game,
        manager=manager
    )

    clock = pygame.time.Clock()
    run = True

    while run:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        game_started = True
                        start_button.hide()

            gui.listen_pygame_user_events(event)
            gui.listen_mouse_events(event)
            manager.process_events(event)

        game_surface.fill(DARK)
        toolbox_surface.fill(GREY)
        manager.update(time_delta)
        if game_started:
            game.run_iteration()

        gui.run_iteration()
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()