from typing import (
    List
)

import arcade
from arcade import Texture
from loguru import logger

FACE_LEFT = -1
FACE_RIGHT = 1


class Copter(arcade.Sprite):
    def __init__(
            self,
            scale: float = 1,
            image_x: float = 0,
            image_y: float = 0,
            center_x: float = 0,
            center_y: float = 0,
            left_textures: List[Texture] = [],
            right_textures: List[Texture] = [],
            border_top=0,
            border_left=0,
            border_right=0
    ):
        super().__init__(
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            center_x=center_x,
            center_y=center_y,
        )
        self.landed = False
        self.state = FACE_RIGHT
        self.left_textures = left_textures
        self.right_textures = right_textures
        self.cur_texture_index = 0
        self.crashed = False
        self.border_top = border_top
        self.border_left = border_left
        self.border_right = border_right
        logger.debug(f'border top {border_top}, left {border_left}, right {border_right}')

        self.update_animation()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.crashed or self.landed:
            return

        self.cur_texture_index += 1
        if self.cur_texture_index >= len(self.right_textures):
            self.cur_texture_index = 0

        self.texture = (self.right_textures if self.state == FACE_RIGHT else self.left_textures)[self.cur_texture_index]
        self.width = self._texture.width * self.scale
        self.height = self._texture.height * self.scale

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)

        if self.center_y > self.border_top:
            self.center_y = self.border_top
            self.change_y = 0

        if self.center_x < self.border_left:
            self.center_x = self.border_left
            self.change_x = 0

        if self.center_x > self.border_right:
            self.center_x = self.border_right
            self.change_x = 0

    def touchdown(self):
        if not self.landed:
            self.landed = True
            logger.debug('heli landed')
            self.change_x = 0

    def takeoff(self):
        self.landed = False
        logger.debug('heli takeoff')

    def turn(self):
        self.state *= -1

    def move_right(self):
        if not self.landed:
            self.change_x += 5
            if self.state == FACE_LEFT:
                self.turn()

    def move_left(self):
        if not self.landed:
            self.change_x -= 5
            if self.state == FACE_RIGHT:
                self.turn()

    def move_up(self):
        self.change_y += 5
        if self.landed:
            self.takeoff()
