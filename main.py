import pygame, sys, random
from pathlib import Path
from settings import *
from player import Hrac
from ball import Lopta

pygame.init()
screen = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
pygame.display.set_caption("Arcade Volleyball")
clock = pygame.time.Clock()


font_big = pygame.font.SysFont("arial", 64)
font_small = pygame.font.SysFont("arial", 28)

# Načítanie náhodného pozadia z priečinka backgrounds
def load_random_background():
    bg_folder = Path(__file__).parent / "backgrounds"
    images = [f for ext in ("png", "jpg", "jpeg", "webp", "bmp") for f in bg_folder.glob(f"*.{ext}")]
    if images:
        try:
            bg = pygame.image.load(random.choice(images)).convert()
            return pygame.transform.scale(bg, (SIRKA_OKNA, VYSKA_OKNA))
        except pygame.error:
            return None
    return None

# Načítanie menu pozadia z priečinka menu_bg
def load_menu_background():
    bg_folder = Path(__file__).parent / "menu_bg"
    images = [f for ext in ("png", "jpg", "jpeg", "webp", "bmp") for f in bg_folder.glob(f"*.{ext}")]
    if images:
        try:
            bg = pygame.image.load(images[0]).convert()  # Prvý obrázok v priečinku
            return pygame.transform.scale(bg, (SIRKA_OKNA, VYSKA_OKNA))
        except pygame.error:
            return None
    return None

# Vytvorenie gradientu pre zatmavenie pozadia
def create_gradient_overlay():
    overlay = pygame.Surface((SIRKA_OKNA, VYSKA_OKNA), pygame.SRCALPHA)
    for y in range(VYSKA_OKNA):
        # Gradient od vrchu (tmavší) po spodok (svetlejší)
        alpha = int(120 - (y / VYSKA_OKNA) * 70)  # 120 hore, 50 dole
        pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (SIRKA_OKNA, y))
    return overlay

gradient_overlay = create_gradient_overlay()

menu_background = load_menu_background()
background = None

h1 = Hrac(150, "Yamal")
h2 = Hrac(650, "Mbappe")
lopta = Lopta()

score_p1 = 0
score_p2 = 0
WIN_SCORE = 10

state = "MENU"
winner_text = ""


def draw_score(p1, p2):
    text = font_small.render(f"{p1} : {p2}", True, BIELA)
    screen.blit(text, (SIRKA_OKNA // 2 - text.get_width() // 2, 10))

def draw_menu():
    title = font_big.render("ARCADE VOLLEYBALL", True, BIELA)
    info = font_small.render("ENTER - START | ESC - QUIT", True, SEDA)

    screen.blit(title, (SIRKA_OKNA // 2 - title.get_width() // 2, 220))
    screen.blit(info, (SIRKA_OKNA // 2 - info.get_width() // 2, 300))

def draw_game_over(text):
    title = font_big.render(text, True, ZLTA)
    info = font_small.render("ENTER - MENU", True, SEDA)

    screen.blit(title, (SIRKA_OKNA // 2 - title.get_width() // 2, 230))
    screen.blit(info, (SIRKA_OKNA // 2 - info.get_width() // 2, 320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if event.key == pygame.K_RETURN:
                    score_p1 = 0
                    score_p2 = 0
                    lopta.reset(1)
                    background = load_random_background()
                    state = "GAME"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    state = "MENU"

    if state == "MENU" or state == "GAME_OVER":
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill(CIERNA)
    else:
        if background:
            screen.blit(background, (0, 0))
            screen.blit(gradient_overlay, (0, 0))
        else:
            screen.fill(CIERNA)

    if state == "MENU":
        draw_menu()

    elif state == "GAME":
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

        if score_p1 >= WIN_SCORE:
            winner_text = "YAMAL WINS!"
            state = "GAME_OVER"
        elif score_p2 >= WIN_SCORE:
            winner_text = "MBAPPE WINS!"
            state = "GAME_OVER"

        pygame.draw.rect(screen, SEDA,
                         (SIRKA_OKNA // 2 - SIRKA_SIETE // 2,
                          VYSKA_OKNA - VYSKA_PODLAHY - VYSKA_SIETE,
                          SIRKA_SIETE, VYSKA_SIETE))

        h1.draw(screen)
        h2.draw(screen)
        lopta.draw(screen)
        draw_score(score_p1, score_p2)

    elif state == "GAME_OVER":
        draw_game_over(winner_text)

    pygame.display.flip()
    clock.tick(FPS)
