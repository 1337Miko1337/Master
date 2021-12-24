from pygame import *

platform_width = 32
move_platform_width=96
platform_height = 32
platform_color = '#FF6262'
platform_move_speed = 2


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_width, platform_height))
        self.image.fill(Color(platform_color))
        self.rect = Rect(x, y, platform_width, platform_height)


class Move_platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel_platform = 0
        self.startx_platform = x
        self.starty_platform = y
        self.image = Surface((move_platform_width, platform_height))
        self.image.fill(Color(platform_color))
        self.rect = Rect(x, y, move_platform_width, platform_height)

    def update(self):
        if self.rect.x > self.startx_platform + 100:
            self.xvel_platform = -platform_move_speed
        if self.rect.x == self.startx_platform:
            self.xvel_platform = platform_move_speed
        self.rect.x += self.xvel_platform
