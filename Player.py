from pygame import *

move_speed = 7
width = 22
height = 32
color = '#888888'
jump_power = 10
gravity = 0.35  # Сила притяжения
place = 0


class player(sprite.Sprite):
    def __init__(self, x, y):
        self.yvel = 0  # Скорость по вертикали
        self.onground = False  # проверка на земле ли я
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещение 0 - стоять
        self.startx = x  # Начальна позиция
        self.starty = y
        self.image = Surface((width, height))
        self.image=image.load('persik.png')
        self.rect = Rect(x, y, width, height)  # Прямоугольный объект, наш персонаж
        self.place = place

    def update(self, left, right, up, platforms, moved_platforms):
        if left:
            self.xvel = -move_speed  # Лево х-n
            self.place = 0
        if right:
            self.xvel = move_speed  # Право x+n
            self.place = 0
        if not (left or right):
            self.xvel = 0  # Стоим если не указано направление
        if up:
            if self.onground:  # Стоим ли мы на земле чтобы прыгнуть
                self.yvel = -jump_power
                self.place = 0
        if not self.onground:
            self.yvel += gravity
        self.onground = False  # мы не знаем когда мы на земле
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, moved_platforms)
        if self.onground_move and self.xvel == 0:
            print('self.tmp ', self.tmp)
            self.xvel = self.tmp
        self.rect.x += self.xvel  # переносим прямоугольник
        self.collide(self.xvel, 0, platforms, moved_platforms)

    def collide(self, xvel, yvel, platforms, moved_platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересеченре платформы и игрока
                self.onground_move = False
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onground = True
                    self.yvel = 0
                    if p in moved_platforms:
                        self.onground_move = True
                        self.tmp = p.xvel_platform
                        print('self.tmp ', self.tmp)
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                # if p in moved_platforms:
                #     if self.place == 0:
                #         self.place = self.rect.x - p.rect.x
                #     self.rect.x = p.rect.x + self.place
