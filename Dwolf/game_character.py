import arcade
import arcade

from characterIndicatorBar import IndicatorBar

class Player(arcade.Sprite):
    def __init__(self, image, scale, center_x, center_y, bar_list: arcade.SpriteList):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        self.indicator_bar: IndicatorBar = IndicatorBar(self, bar_list, [center_x, 20])
        self.health: int = 15    #por defecto tiene una vida de 15
        



class Enemy(arcade.Sprite):
    '''
    Clase de personajes estilo Enemigos
        Tiene una imagen, escala, posicionx, posiciony
            Tambien tiene un atributo "Vida": la cantidad de disparos para poder "morir"
    '''
    def __init__(self, image, scale, center_x, center_y, health: int):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        self.score = 0
        self.vida = health  #Enemigo con atributo vida

    


