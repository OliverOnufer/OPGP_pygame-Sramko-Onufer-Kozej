import pygame, sys
from settings import *
from player import Hrac
from ball import Lopta

pygame.init()
screen = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
clock = pygame.time.Clock()

h1 = Hrac(150, "Yamal")
h2 = Hrac(650, "Mbappe")
lopta = Lopta()

score_p1 = 0
score_p2 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    h1.update(keys)
    h2.update(keys)
    lopta.update([h1, h2])

    if lopta.y + lopta.radius > VYSKA_OKNA - VYSKA_PODLAHY:
        if lopta.x < SIRKA_OKNA // 2:
            score_p2 += 1
            lopta.reset(2)
        else:
            score_p1 += 1
            lopta.reset(1)

    screen.fill(CIERNA)
    pygame.draw.rect(screen, SEDA, (0, VYSKA_OKNA-VYSKA_PODLAHY, SIRKA_OKNA, VYSKA_PODLAHY))
    pygame.draw.rect(screen, SEDA, (SIRKA_OKNA//2 - SIRKA_SIETE//2,
                                     VYSKA_OKNA - VYSKA_PODLAHY - VYSKA_SIETE,
                                     SIRKA_SIETE, VYSKA_SIETE))

    h1.draw(screen)
    h2.draw(screen)
    lopta.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
