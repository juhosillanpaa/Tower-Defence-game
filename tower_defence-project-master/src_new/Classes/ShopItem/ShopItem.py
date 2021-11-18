import pygame
import pygame_gui
RED = (199, 14, 14)
GREEN = (9, 143, 18)
RADIUS = 32
BLACK = (0, 0, 0)


class ShopItem:
    def __init__(self, game, toolbox_surface, toolbox_pos, window_surface,  tower, image_url, price):
        self.game = game
        self.toolbox_pos = toolbox_pos
        self.drag_pos = (0,0)
        self.toolbox_surface = toolbox_surface
        self.window_surface = window_surface
        self.tower = tower
        self.image = pygame.transform.scale(
            pygame.image.load(image_url),
            (64, 64)
        )
        self.cancel_image = pygame.transform.scale(
            pygame.image.load("utility/images/trash.jpg"),
            (64, 64)
        )
        self.image_rect = self.get_toolbox_image_rect()
        self.dragging = False
        self.width = 64
        self.height = 64
        self.price = price

    def get_toolbox_image_rect(self):
        offset = self.toolbox_surface.get_offset()
        image_pos = (offset[0] + self.toolbox_pos[0], offset[1] + self.toolbox_pos[1])
        image_rect = pygame.Rect(image_pos, (64, 64))
        return image_rect

    def draw(self):
        if self.dragging:
            self.toolbox_surface.blit(self.cancel_image, self.toolbox_pos)
            if self.game.can_place_tower(self.get_center_drag_pos()):
                pygame.draw.circle(self.window_surface,GREEN, self.get_center_drag_pos(), RADIUS, 2)
            else:
                pygame.draw.circle(self.window_surface, RED, self.get_center_drag_pos(), RADIUS, 2)
            self.window_surface.blit(self.image, self.drag_pos)

        else:
            pygame.draw.rect(self.toolbox_surface, (255,255,255), pygame.Rect(self.toolbox_pos, (64,64)))
            self.toolbox_surface.blit(self.image, self.toolbox_pos)
        self.draw_price_text_below()


    def draw_price_text_below(self):
        text = 'Price: ' + str(self.price)
        font = pygame.font.SysFont('arial', 16, False)
        img = font.render(text, True, BLACK)
        pos = self.toolbox_pos
        y = pos[1] + 74
        x = pos[0] - 5
        self.toolbox_surface.blit(img, (x, y))

    def update_position(self, pos):
        x = pos[0] - self.width//2
        y = pos[1] - self.height//2
        self.drag_pos = (x, y)

    def update_and_draw(self):
        if self.dragging:
            self.update_position(pygame.mouse.get_pos())
        self.draw()

    def listen_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.image_rect.collidepoint(event.pos):
                if self.game.can_afford(self.price):
                    self.activate_drag()
        if event.type == pygame.MOUSEBUTTONUP:
            if self.image_rect.collidepoint(event.pos):
                self.end_drag()
            elif self.dragging:
                self.end_drag()
                self.place_tower()



    def activate_drag(self):
        self.dragging = True

    def end_drag(self):
        self.dragging = False

    def get_center_drag_pos(self):
        return self.drag_pos[0] + 32, self.drag_pos[1] + 32

    def place_tower(self):

        tower = self.tower()
        tower.set_position(self.get_center_drag_pos())
        if self.game.can_place_tower(tower.get_position()):
            self.game.add_tower(tower)
            self.game.reduce_money(self.price)
        else:
            return
