"""
Camera Example

Artwork from: https://kenney.nl
Tiled available from: https://www.mapeditor.org/

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.camera_example
"""


import time
import random 
import arcade
#carpetas
from game_character import Player
from game_character import Enemy
from game_skills import Bullet


TILE_SCALING = 0.5
PLAYER_SCALING = 0.13

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

SCREEN_TITLE = "Dwolf"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

# Physics
MOVEMENT_SPEED = 4
JUMP_SPEED = 24
GRAVITY = 1.1


# Map Layers
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
#LAYER_NAME_BOMBS = "Bombs"


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True, fullscreen=True)
        #bullets & skills
        self.bullets = arcade.SpriteList()  #lista de balas
        self.enemies = arcade.SpriteList()  #lista de enemigos
        self.sprites = arcade.SpriteList()  #lista que contienen listas :D
        
        #Jugador en init
        self.bar_list = arcade.SpriteList()
        self.player = Player(("img/StormW.gif"),PLAYER_SCALING,196,128, self.bar_list)
        
        self.bullet = None  #Existe una bala que aun no esta instanciada
        self.enemy = None  #Existe un enemigo que aun no esta instanciado
        
        
        #Cronos
        arcade.schedule(self.add_enemy_12, 2)
        arcade.schedule(self.add_enemy_stronger, 5)

        

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None
        self.scene_bullet = None

        # Set up the player
        self.score = 0
        #self.player_sprite = None

        self.physics_engine = None
        self.top_of_map = 0
        self.end_of_map = 0
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        self.shake_offset_1 = 0
        self.shake_offset_2 = 0
        self.shake_vel_1 = 0
        self.shake_vel_2 = 0

        # Text
        self.text_fps = arcade.Text(
            "",
            start_x=10,
            start_y=40,
            color=arcade.color.GREEN,
            font_size=14,
        )
        
        self.text_score = arcade.Text(
            f"Score: {self.score}",
            start_x=10,
            start_y=20,
            color=arcade.color.GREEN,
            font_size=14,
        )
        self.text_vitality = arcade.Text(
            f"Score: {self.player.health}",
            start_x=150,
            start_y=20,
            color=arcade.color.GREEN,
            font_size=14,
        )
#AQUI PUEDO DEFINIR EL MAPA
    def setup(self):
        """Set up the game and initialize the variables."""
        # Map name
        map_name = ":resources:tiled_maps/test_map_2.json"

        # Layer Specific Options
            #Spatial hash mejora en detectar colisiones
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            }
        }
        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        #variable escena, agrega un jugador q es un sprite.
        self.scene.add_sprite("Player", self.player)
#DEFINIMOS LA CAMARAAAAAAAAAAAAAAAAAAAAAA
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Center camera on user
        self.pan_camera_to_user()

        # Calculate the right edge of the my_map in pixels
        self.top_of_map = self.tile_map.height * GRID_PIXEL_SIZE
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            self.background_color = self.tile_map.background_color

        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
            gravity_constant=GRAVITY,
        )

        self.game_over = False



#METODO DE LA CLASE
    def on_resize(self, width, height):
        """Resize window"""
        self.camera.resize(width, height)
        self.gui_camera.resize(width, height)


#METODO DE LA CLASE
    def on_draw(self):
        """Render the screen."""
        self.clear()
        self._fullscreen
        arcade.start_render()
        self.camera.use()

        # Draw our Scene
        self.scene.draw() #primeroe dibujo mis escenas, tipo sprites
        #self.bar_list.draw()
        self.gui_camera.use()

        # Update fps text periodically
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.text_fps.text = f"FPS: {fps:5.2f}"

        self.text_fps.draw()

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Draw Score
        self.text_score.draw()
        self.text_vitality.draw()

        # Draw game over
        if self.game_over:
            x = SCREEN_WIDTH/1.5
            y = SCREEN_HEIGHT/2
            arcade.draw_text("Game Over", x, y, arcade.color.RED, 50)
            self.score = 0
            exit


        self.frame_count += 1

   

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            print(self.player.center_x)
            if self.player.center_x > 193:
                self.player.change_x = -MOVEMENT_SPEED
            else:
                print(f"Log: el personaje no debe retroceder mas")
            
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
            self.player.angle = 0   

        if key == arcade.key.SPACE:
            self.bullet = Bullet(
                "img/ojo.png",
                0.1,
                angle=self.player.angle ,
                center_x=self.player.center_x,
                center_y=self.player.center_y,
            ) 
            self.bullets.append(self.bullet)
            self.sprites.append(self.bullet)
            self.scene.add_sprite("Bullet",self.bullet)
            print(self.player.center_y)

    def update_bullets(self):
        for b in self.bullets:
            if b.right > self.player.center_x + SCREEN_WIDTH:  #La bala tiene un rango de alcance
                print(f"Log Bala: Punto x= {self.player.center_x}, Punto_y = {self.player.center_y}")
                b.remove_from_sprite_lists()



    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Manage Scrolling

        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)

    def add_enemy_12(self, delta_time: float):
        numero_aleatorio = random.randint(int(self.player.center_y), int(self.player.center_y) + 100) #aleatoriamente se va a generar en un punto Y :D
        
        setEnemy = random.randint(1,3)
        
        self.enemy = Enemy((f"img/enemy{setEnemy}.png"),0.25,1500,numero_aleatorio, 1) #este enemigo necesita 2 balazos pa morir

        velocidad_aleatoria = random.randint(-15, -6)
        self.enemy.velocity = (velocidad_aleatoria ,0) #velocidad del enemigo, se mueve en -8 desde X

        self.enemies.append(self.enemy) 
        self.sprites.append(self.enemy)
        self.scene.add_sprite("Enemy",self.enemy)
        print("Log Enemigo: se genera un enemigo en la pantalla")

    def add_enemy_stronger(self, delta_time: float):
        numero_aleatorio = random.randint(int(self.player.center_y), int(self.player.center_y) + 100) #aleatoriamente se va a generar en un punto Y :D
        
        setEnemy = random.randint(1,2)
        self.enemy = Enemy((f"img/enemy3.png"),0.4,1500,numero_aleatorio, 4) #este enemigo necesita  5 balazos pa morir

        velocidad_aleatoria = random.randint(-5, -2)
        self.enemy.velocity = (velocidad_aleatoria ,0) #velocidad del enemigo, se mueve en -8 desde X

        self.enemies.append(self.enemy) 
        self.sprites.append(self.enemy)
        self.scene.add_sprite("Enemy",self.enemy)
        print("Log Enemigo_stronger: se genera un enemigo en la pantalla")

    def update_enemies_hitdown(self):
        for e in self.enemies:
            for b in self.bullets:
                if e.collides_with_list(self.bullets):  
                    b.remove_from_sprite_lists()

                    if e.vida > 0:
                        print(f"tiene vida {e.vida}")
                        e.vida -= 1  #la bala siempre hace 1 de damage
                    else:
                        e.remove_from_sprite_lists()
                        self.score += 1
    
    def update_enemies_offScene(self):
         '''
         Funcion en pantalla para poder tomar en cuenta el "Damage de los enemigos"
         Nuestro personaje tiene una vitalidad PREDEFINIDA de 15.
            Cada enemigo tiene una vitalidad de aguante...
            enemigo normal: aguante de 2
            enemigo fuerte: aguante de 5

            Damage q recibe nuestro personaje = aguante de vitalidad de enemigos
         '''
         for e in self.enemies:
            if e.left < -self.player.center_x or e.top > 750:
                    e.remove_from_sprite_lists()
                    if(self.player.health > 0):
                        print(f"Log vitalidad_Personaje: {self.player.health} \n Damage recibido {e.vida + 1}")
                        self.player.health -= e.vida + 1
                    else:
                        print("Personaje Muerto, fuera de escena")
                    
        


    def on_update(self, delta_time):
        """Movement and game logic"""
        self.player.update() #Update de mi jugador
        self.update_bullets() #update tomar en cuenta balas

        self.update_enemies_hitdown() #update tomar en cuenta mis enemigos
        self.update_enemies_offScene()  #Tomar en cuenta si el personaje salio de la pantalla

        self.sprites.update() #Update de mis listas

        if self.player.health <=0:
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()

        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.scene.get_sprite_list("Coins")
        )
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Bomb hits
        #bombs_hit = arcade.check_for_collision_with_list(
        #    self.player_sprite, self.scene.get_sprite_list("Bombs")
        #)
        #for bomb in bombs_hit:
        #    bomb.remove_from_sprite_lists()
        #    print("Pow")
        #    self.camera.shake((4, 7))

        # Pan to the user
        self.pan_camera_to_user(panning_fraction=0.12)

        # Update score text
        self.text_score.text = f"Score: {self.score}"
        self.text_vitality.text = f"Vitalidad: {self.player.health}"

    

def main():
    """Get this game started."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()