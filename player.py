import pygame
from settings import *

class Hrac:
    def __init__(self, x, prefix):
        self.x = x
        self.y = VYSKA_OKNA - VYSKA_PODLAHY - POLOMER_HRACA
        self.radius = POLOMER_HRACA
        self.vel_y = 0
        self.na_zemi = False
        self.prefix = prefix

    def update(self, keys):
        if keys[KEY_MAP[f"{self.prefix}_LEFT"]]:
            self.x -= RYCHLOST_HRACA
        if keys[KEY_MAP[f"{self.prefix}_RIGHT"]]:
            self.x += RYCHLOST_HRACA
        if keys[KEY_MAP[f"{self.prefix}_JUMP"]] and self.na_zemi:
            self.vel_y = SILA_SKOKU
            self.na_zemi = False

        self.vel_y += GRAVITACIA
        self.y += self.vel_y

        if self.y + self.radius > VYSKA_OKNA - VYSKA_PODLAHY:
            self.y = VYSKA_OKNA - VYSKA_PODLAHY - self.radius
            self.vel_y = 0
            self.na_zemi = True

        net_x = SIRKA_OKNA // 2
        if self.prefix == "P1":
            self.x = max(self.radius, min(self.x, net_x - SIRKA_SIETE//2 - self.radius))
        else:
            self.x = max(net_x + SIRKA_SIETE//2 + self.radius, min(self.x, SIRKA_OKNA - self.radius))

    def draw(self, screen):
        pygame.draw.circle(screen, BIELA, (int(self.x), int(self.y)), self.radius, 2)
