import math
import arcade

class Bullet(arcade.Sprite):
    def __init__(self, image, scale, angle, center_x, center_y):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.velocity = (13,0)#le defino una velocidad de una vez