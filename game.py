import random

import arcade
from loguru import logger

from copter import Copter

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCALING = 2.0
BORDER_TOP = (SCREEN_HEIGHT - 10) * SCALING
BORDER_RIGHT = (SCREEN_WIDTH - 25) * SCALING
BORDER_LEFT = 25 * SCALING


class Game(arcade.Window):
    def __init__(self):
        super().__init__(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), 'Heli')
        self.scene = None
        self.crashed = False
        self.paused = False
        arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)
        self.background = arcade.load_texture('images/background.png')
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.physics_engine = None
        self.restart()

    def restart(self):
        self.paused = False
        self.player = Copter(SCALING * 1.4,
                             center_x=150 * SCALING,
                             center_y=SCREEN_HEIGHT / 3 * 2 * SCALING,
                             left_textures=[arcade.load_texture(f'images/heli/helicopter_{x}.png', flipped_horizontally=True) for x in range(1, 9)],
                             right_textures=[arcade.load_texture(f'images/heli/helicopter_{x}.png') for x in range(1, 9)],
                             border_top=BORDER_TOP,
                             border_left=BORDER_LEFT,
                             border_right=BORDER_RIGHT
                             )
        self.scene = arcade.Scene()
        self.scene.add_sprite('player', self.player)

        prev = 32
        for x in range(32, 64 + int(SCREEN_WIDTH * SCALING), 64):
            prev += random.randint(-30, 30)
            prev = max(0, prev)
            wall = arcade.Sprite('images/Map_tile_76.png', SCALING, center_x=x, center_y=prev)
            self.scene.add_sprite('walls', wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.scene.get_sprite_list('walls'), gravity_constant=0.2)
        logger.info('starting up')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.move_up()

        if symbol == arcade.key.RIGHT:
            self.player.move_right()

        if symbol == arcade.key.LEFT:
            self.player.move_left()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.R:
            self.restart()

        if symbol in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.close_window()

    def on_update(self, delta_time: float):
        if self.paused:
            return

        self.scene.on_update(delta_time)
        self.scene.update_animation(0, ['player'])

        speed = self.player.change_y
        hit = self.physics_engine.update()

        if len(hit) > 0:
            if speed < -5:
                arcade.play_sound(self.collision_sound)
                self.player.crashed = True
            else:
                self.player.touchdown()

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH * SCALING, SCREEN_HEIGHT * SCALING, self.background, alpha=200)
        self.scene.draw()

        if self.player.crashed:
            arcade.draw_text('CRASHED', -150 + SCREEN_WIDTH * SCALING / 2, SCREEN_HEIGHT * SCALING / 2, font_size=80, color=arcade.color.RED_ORANGE, bold=True)
            self.paused = True


if __name__ == '__main__':
    app = Game()
    arcade.run()
