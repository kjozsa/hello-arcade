import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALING = 2.0


class Heli(arcade.Window):
    def __init__(self):
        super().__init__(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), 'Heli')
        arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)

        self.player = arcade.Sprite('images/jet.png', SCALING, center_x=150 * SCALING, center_y=SCREEN_HEIGHT / 3 * 2 * SCALING)
        self.scene = arcade.Scene()
        self.scene.add_sprite('player', self.player)

        for x in range(32, int(SCREEN_WIDTH * SCALING), 64):
            wall = arcade.Sprite('images/Map_tile_76.png', SCALING, center_x=x, center_y=32)
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
        if self.player.center_y < 10 * SCALING:
            self.player.center_y = 10 * SCALING
            self.player.change_y = 0

        if self.player.center_y > (SCREEN_HEIGHT - 10) * SCALING:
            self.player.center_y = (SCREEN_HEIGHT - 10) * SCALING
            self.player.change_y = 0

        if self.player.center_x < 10 * SCALING:
            self.player.center_x = 10 * SCALING
            self.player.change_x = 0

        if self.player.center_x > (SCREEN_WIDTH - 10) * SCALING:
            self.player.center_x = (SCREEN_WIDTH - 10) * SCALING
            self.player.change_x = 0

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()


if __name__ == '__main__':
    app = Heli()
    arcade.run()
