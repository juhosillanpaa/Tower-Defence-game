from .Enemy import Enemy


class RedEnemy(Enemy):
    def __init__(self, path, width=64, height=64):
        self.velocity = 2
        self.max_health = 100
        self.norm_vec = (1, 0)
        self.image_url = "utility/images/red_car/red_car.png"
        self.broken_image_url = "utility/images/red_car/red_car_exploded.png"

        super().__init__(
            path=path,
            width=width,
            height=height,
            velocity=self.velocity,
            max_health=self.max_health,
            norm_vec=self.norm_vec,
            image_url=self.image_url,
            broken_image_url=self.broken_image_url,
            bounty=20
        )