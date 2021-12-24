import pygame
from pygame import *
from Player import *
from blocks import *

window_width = 800  # Ширина
window_height = 640  # Высотав
display = (window_width, window_height)
background_color = '#004400'


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + window_width / 2, -t + window_height / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - window_width), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - window_height), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(display)  # Создаем окно
    pygame.display.set_caption('')  # Название окна
    bg = Surface((window_width, window_height))  # Видимая зона окна
    bg.fill(Color(background_color))  # Заливка окна
    hero = player(494, 128)
    left = right = up = False
    entities = pygame.sprite.Group()  # все объекты
    moved_platforms = []
    platforms = []  # то, во что будем врезаться
    entities.add(hero)
    level = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-                                -",
        "-             +                  -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                            --- -",
        "-                                -",
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == '+':
                pf = Move_platform(x, y)
                entities.add(pf)
                platforms.append(pf)
                moved_platforms.append(pf)
            x += platform_width
        y += platform_height
        x = 0
    total_level_width = len(level[0]) * platform_width  # ширина уровня
    total_level_height = len(level) * platform_height  # высота
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
        for i in moved_platforms:
            i.update()
        screen.blit(bg, (0, 0))  # Перерисовка
        hero.update(left, right, up, platforms, moved_platforms)  # Отображаем
        camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))  # Рисуем
        pygame.display.update()  # Обновление и вывод изменений


if __name__ == '__main__':
    main()
