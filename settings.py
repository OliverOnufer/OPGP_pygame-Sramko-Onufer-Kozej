import pygame

SIRKA_OKNA, VYSKA_OKNA = 800, 600
FPS = 60

CIERNA = (20,20,20)
BIELA = (240,240,240)
SEDA = (100,100,100)
ZLTA = (255,255,0)

# Barcelona farby
BAR_MODRA = (4, 108, 207)
BAR_CERVENA = (206, 17, 38)

# Real Madrid farby
RM_BIELA = (255, 255, 255)
RM_CERNA = (0, 0, 0)

GRAVITACIA = 0.4
RYCHLOST_HRACA = 6
SILA_SKOKU = -10

VYSKA_SIETE = 200
SIRKA_SIETE = 8
VYSKA_PODLAHY = 40

POLOMER_HRACA = 35
POLOMER_LOPTY = 20

KEY_MAP = {
    "Yamal_LEFT": pygame.K_a, "Yamal_RIGHT": pygame.K_d, "Yamal_JUMP": pygame.K_w,
    "Mbappe_LEFT": pygame.K_LEFT, "Mbappe_RIGHT": pygame.K_RIGHT, "Mbappe_JUMP": pygame.K_UP
}
