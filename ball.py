import pygame
import math
from settings import *

class Lopta:
    def __init__(self):
        self.radius = POLOMER_LOPTY
        self.reset(1)

    def reset(self, side):
        self.x = 200 if side == 1 else SIRKA_OKNA - 200
        self.y = 200
        self.vel_x = 0
        self.vel_y = 0

    def update(self, hraci):
        self.vel_y += GRAVITACIA * 0.6
        self.x += self.vel_x
        self.y += self.vel_y

        if self.x - self.radius < 0 or self.x + self.radius > SIRKA_OKNA:
            self.vel_x *= -0.9
        if self.y - self.radius < 0:
            self.vel_y *= -0.9

        net_left = SIRKA_OKNA//2 - SIRKA_SIETE//2
        net_right = SIRKA_OKNA//2 + SIRKA_SIETE//2
        net_top = VYSKA_OKNA - VYSKA_PODLAHY - VYSKA_SIETE

        if net_left < self.x < net_right and self.y + self.radius > net_top:
            self.vel_x *= -1
            self.vel_y *= -0.7

        for h in hraci:
            dist = math.hypot(self.x - h.x, self.y - h.y)
            if dist < self.radius + h.radius:
                angle = math.atan2(self.y - h.y, self.x - h.x)
                speed = max(8, math.hypot(self.vel_x, self.vel_y))
                self.vel_x = math.cos(angle) * speed
                self.vel_y = math.sin(angle) * speed

    def draw(self, screen):
        pygame.draw.circle(screen, ZLTA, (int(self.x), int(self.y)), self.radius)
