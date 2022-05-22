import random

import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCALING = 2.0
BORDER_TOP = (SCREEN_HEIGHT - 10) * SCALING
BORDER_RIGHT = (SCREEN_WIDTH - 25) * SCALING
BORDER_LEFT = 25 * SCALING


class Heli(arcade.Window):
    def __init__(self):
        super().__init__(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), 'Heli')
        arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)

        self.player = arcade.Sprite('images/jet.png', SCALING, center_x=150 * SCALING, center_y=SCREEN_HEIGHT / 3 * 2 * SCALING)
        self.scene = arcade.Scene()
        self.scene.add_sprite('player', self.player)

        prev = 32
        for x in range(32, 64 + int(SCREEN_WIDTH * SCALING), 64):
            prev += random.randint(-15, 15)
            wall = arcade.Sprite('images/Map_tile_76.png', SCALING, center_x=x, center_y=prev)
            self.scene.add_sprite('walls', wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.scene.get_sprite_list('walls'), gravity_constant=0.2)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.close_window()
        if symbol == arcade.key.UP:
            self.player.change_y += 5
        if symbol == arcade.key.RIGHT:
            self.player.change_x += 5
        if symbol == arcade.key.LEFT:
            self.player.change_x -= 5

    def on_update(self, delta_time: float):
        self.physics_engine.update()

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
        self.scene.draw()


if __name__ == '__main__':
    app = Heli()
    arcade.run()
