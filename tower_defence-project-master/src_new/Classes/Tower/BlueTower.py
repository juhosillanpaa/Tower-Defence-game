from .Tower import Tower



class BlueTower(Tower):
    def __init__(self, x=0, y=0, width=64, height=64):
        super().__init__(
            x, y, width, height,
            fire_rate=60,
            firing_distance=200,
            barrel_length=width/2 - width/10,
            damage=50,
            norm_vec=(0, -1),
            image_url="utility/images/blue_tower/blue_tower.png",
            firing_image_url="utility/images/blue_tower/blue_tower_firing.png",
            price=100
        )