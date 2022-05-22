import random

import arcade
from arcade.sprite import FACE_RIGHT, FACE_LEFT
from loguru import logger

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCALING = 2.0
BORDER_TOP = (SCREEN_HEIGHT - 10) * SCALING
BORDER_RIGHT = (SCREEN_WIDTH - 25) * SCALING
BORDER_LEFT = 25 * SCALING


class Heli(arcade.Window):
    def __init__(self):
        super().__init__(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), 'Heli')
        self.crashed = False
        self.paused = False
        arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)
        self.background = arcade.load_texture('images/background.png')

        self.player = arcade.AnimatedWalkingSprite(SCALING * 1.3, center_x=150 * SCALING, center_y=SCREEN_HEIGHT / 3 * 2 * SCALING)
        self.player.name = 'player'
        self.player.textures = [arcade.load_texture(f'images/heli/helicopter_{x}.png') for x in range(1, 9)]
        self.player.textures_l = [arcade.load_texture(f'images/heli/helicopter_{x}.png', flipped_horizontally=True) for x in range(1, 9)]
        self.scene = arcade.Scene()
        self.scene.add_sprite('player', self.player)

        prev = 32
        for x in range(32, 64 + int(SCREEN_WIDTH * SCALING), 64):
            prev += random.randint(-30, 30)
            prev = max(0, prev)
            wall = arcade.Sprite('images/Map_tile_76.png', SCALING, center_x=x, center_y=prev)
            wall.name = f'wall{x}'
            self.scene.add_sprite('walls', wall)

        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.scene.get_sprite_list('walls'), gravity_constant=0.2)
        logger.info('starting up')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.close_window()
        if symbol == arcade.key.UP:
            self.player.change_y += 5
        if symbol == arcade.key.RIGHT:
            self.player.change_x += 5
            if self.player.state == FACE_LEFT:
                self.player.state = FACE_RIGHT
        if symbol == arcade.key.LEFT:
            self.player.change_x -= 5
            if self.player.state == FACE_RIGHT:
                self.player.state = FACE_LEFT
        if symbol == arcade.key.P:
            self.paused = not self.paused

    def on_update(self, delta_time: float):
        if self.paused:
            return
        speed = self.player.change_y

        hit = self.physics_engine.update()

        if len(hit) > 0 and speed < -5:
            arcade.play_sound(self.collision_sound)
            self.crashed = True

        self.player.cur_texture_index += 1
        if self.player.cur_texture_index >= len(self.player.textures):
            self.player.cur_texture_index = 0
        texture_used = self.player.textures if self.player.state == FACE_RIGHT else self.player.textures_l
        self.player.texture = texture_used[self.player.cur_texture_index]

        if self.player.center_y > BORDER_TOP:
            self.player.center_y = BORDER_TOP
            self.player.change_y = 0

        if self.player.center_x < BORDER_LEFT:
            self.player.center_x = BORDER_LEFT
            self.player.change_x = 0

        if self.player.center_x > BORDER_RIGHT:
            self.player.center_x = BORDER_RIGHT
            self.player.change_x = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH * SCALING, SCREEN_HEIGHT * SCALING, self.background, alpha=200)
        self.scene.draw()

        if self.crashed:
            arcade.draw_text('CRASHED', -150 + SCREEN_WIDTH * SCALING / 2, SCREEN_HEIGHT * SCALING / 2, font_size=80, color=arcade.color.RED_ORANGE, bold=True)
            self.paused = True


if __name__ == '__main__':
    app = Heli()
    arcade.run()
