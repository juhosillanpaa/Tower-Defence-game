from ..GameObject.GameObject import GameObject
from ..HealthBar.HealthBar import HealthBar

class Castle(GameObject):
    def __init__(self, x, y, width=64, height=64, max_health = 10):
        self.image_url = "utility/images/castle.png"
        self.rotation = 0
        self.health = max_health
        self.max_health = max_health
        self.health_bar = HealthBar(x - width // 2, y + height//2, max_health, width)
        super().__init__(x, y, width, height, self.rotation, self.image_url)


    def reduce_health(self, damage):
        self.health -= damage

    def draw(self, window):
        self.health_bar.draw(window, self.health)
        super().draw(window)