import pygame, sys, random
from pathlib import Path
from settings import *
from player import Hrac
from ball import Lopta
from network import Network

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
        alpha = int(120 - (y / VYSKA_OKNA) * 70)  # 120 hore, 50 dole
        pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (SIRKA_OKNA, y))
    return overlay

gradient_overlay = create_gradient_overlay()

# Načítanie zvukov
def load_sound(name):
    sound_folder = Path(__file__).parent / "sounds"
    for ext in ("wav", "mp3", "ogg"):
        sound_path = sound_folder / f"{name}.{ext}"
        if sound_path.exists():
            try:
                return pygame.mixer.Sound(sound_path)
            except pygame.error:
                pass
    return None

# Načítanie hudby do pozadia
def load_music():
    sound_folder = Path(__file__).parent / "sounds"
    for ext in ("wav", "mp3", "ogg"):
        music_path = sound_folder / f"music.{ext}"
        if music_path.exists():
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.3)
                return True
            except pygame.error:
                pass
    return False

sound_point = load_sound("point")
sound_click = load_sound("click")
sound_jump = load_sound("jump")
sound_gameover = load_sound("gameover")
has_music = load_music()

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
connected_players = 0

# Premenná na sledovanie zmien skóre (kvôli zvuku u klienta)
last_score_sum = 0

def start_game():
    global score_p1, score_p2, last_score_sum, background, state
    score_p1 = 0
    score_p2 = 0
    last_score_sum = 0
    lopta.reset(1)
    background = load_random_background()
    if has_music:
        pygame.mixer.music.play(-1)
    state = "GAME"


def draw_score(p1, p2):
    text = font_small.render(f"{p1} : {p2}", True, BIELA)
    screen.blit(text, (SIRKA_OKNA // 2 - text.get_width() // 2, 10))

def draw_menu():
    title = font_big.render("ARCADE VOLLEYBALL", True, BIELA)
    info = font_small.render("ENTER - START | ESC - QUIT", True, SEDA)
    screen.blit(title, (SIRKA_OKNA // 2 - title.get_width() // 2, 220))
    screen.blit(info, (SIRKA_OKNA // 2 - info.get_width() // 2, 300))

def draw_waiting():
    if connected_players < 2:
        title = font_big.render("Čaká sa na hráča...", True, BIELA)
        info = font_small.render("Počkaj, kým sa pripojí druhý hráč", True, SEDA)
    else:
        title = font_big.render("Druhý hráč je pripojený!", True, BIELA)
        info = font_small.render("Stlač ENTER pre začatie hry", True, SEDA)
    screen.blit(title, (SIRKA_OKNA // 2 - title.get_width() // 2, 220))
    screen.blit(info, (SIRKA_OKNA // 2 - info.get_width() // 2, 300))

def draw_game_over(text):
    title = font_big.render(text, True, ZLTA)
    info = font_small.render("ENTER - MENU", True, SEDA)
    screen.blit(title, (SIRKA_OKNA // 2 - title.get_width() // 2, 230))
    screen.blit(info, (SIRKA_OKNA // 2 - info.get_width() // 2, 320))

n = Network()
player_id = n.p 

if player_id is None:
    print("Server nebeží, spusti lokálnu hru.")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if event.key == pygame.K_RETURN:
                    if connected_players == 2:
                        server_data = n.send({"start_game": True})
                        if server_data:
                            connected_players = server_data.get("players_connected", connected_players)
                        start_game()
                    else:
                        state = "WAITING"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif state == "WAITING":
                if event.key == pygame.K_RETURN and connected_players == 2:
                    server_data = n.send({"start_game": True})
                    if server_data:
                        connected_players = server_data.get("players_connected", connected_players)
                    start_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    state = "MENU"
                    if player_id is not None:
                        n.send({"reset_start": True})

    if state in ("MENU", "WAITING", "GAME_OVER"):
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

    if state in ("MENU", "WAITING") and player_id is not None:
        status_data = {"status": True}
        server_data = n.send(status_data)
        if server_data:
            connected_players = server_data.get("players_connected", connected_players)
            if state == "WAITING" and server_data.get("start_game"):
                start_game()

    if state == "MENU":
        draw_menu()
    elif state == "WAITING":
        draw_waiting()

    elif state == "GAME":
        keys = pygame.key.get_pressed()
        
        if player_id is not None:
            # PLAYER 0 (HOST) - Počíta fyziku, body aj 3 dotyky
            if player_id == 0:
                h1.update(keys)  
                lopta.update([h1, h2]) 

                # Kontrola pravidla 3 dotykov
                if lopta.touch_count > 3:
                    if sound_point:
                        sound_point.play()
                    if lopta.x < SIRKA_OKNA // 2:
                        score_p2 += 1  # Bod pre Mbappe (Yamal spravil 4 dotyky)
                        lopta.reset(2)
                    else:
                        score_p1 += 1  # Bod pre Yamala (Mbappe spravil 4 dotyky)
                        lopta.reset(1)

                # Kontrola pádu na zem
                elif lopta.y + lopta.radius > VYSKA_OKNA - VYSKA_PODLAHY:
                    if sound_point:
                        sound_point.play()
                    if lopta.x < SIRKA_OKNA // 2:
                        score_p2 += 1
                        lopta.reset(2)
                    else:
                        score_p1 += 1
                        lopta.reset(1)
                
                if score_p1 >= WIN_SCORE or score_p2 >= WIN_SCORE:
                    state = "GAME_OVER"

                # Odosielanie dát na server
                data = {
                    "hrac": {"x": h1.x, "y": h1.y, "anim": h1.animation_time, "na_zemi": h1.na_zemi},
                    "ball": {"x": lopta.x, "y": lopta.y, "vel_x": lopta.vel_x, "vel_y": lopta.vel_y, "waiting": lopta.waiting},
                    "score": [score_p1, score_p2],
                    "game_over": (state == "GAME_OVER")
                }
                server_data = n.send(data)
                
                if server_data:
                    connected_players = server_data.get("players_connected", connected_players)
                    h2.x, h2.y = server_data[1]["x"], server_data[1]["y"]
                    h2.animation_time = server_data[1]["anim"]
                    h2.na_zemi = server_data[1]["na_zemi"]

            # PLAYER 1 (CLIENT) - Hýbe sebou, všetko ostatné ťahá zo servera
            else: 
                h2.update(keys)
                data = {"hrac": {"x": h2.x, "y": h2.y, "anim": h2.animation_time, "na_zemi": h2.na_zemi}}
                server_data = n.send(data)

                if server_data:
                    connected_players = server_data.get("players_connected", connected_players)
                    h1.x, h1.y = server_data[0]["x"], server_data[0]["y"]
                    h1.animation_time = server_data[0]["anim"]
                    h1.na_zemi = server_data[0]["na_zemi"]
                    
                    lopta.x, lopta.y = server_data["ball"]["x"], server_data["ball"]["y"]
                    lopta.waiting = server_data["ball"]["waiting"]
                    
                    # Detekcia zmeny skóre u klienta, aby zahralo zvuk "point"
                    nové_skore = server_data["score"]
                    if sum(nové_skore) > last_score_sum:
                        if sound_point:
                            sound_point.play()
                        last_score_sum = sum(nové_skore)

                    score_p1, score_p2 = nové_skore
                    
                    if server_data.get("game_over"):
                         state = "GAME_OVER"

            # Vyhodnocovanie konca hry pre oboch
            if state == "GAME_OVER":
                if score_p1 >= WIN_SCORE: 
                    winner_text = "YAMAL WINS!"
                else: 
                    winner_text = "MBAPPE WINS!"
                pygame.mixer.music.stop()
                if sound_gameover: 
                    sound_gameover.play()

        # Vykresľovanie
        pygame.draw.rect(screen, SEDA, (SIRKA_OKNA // 2 - SIRKA_SIETE // 2, VYSKA_OKNA - VYSKA_PODLAHY - VYSKA_SIETE, SIRKA_SIETE, VYSKA_SIETE))
        h1.draw(screen)
        h2.draw(screen)
        lopta.draw(screen)
        draw_score(score_p1, score_p2)

    elif state == "GAME_OVER":
        draw_game_over(winner_text)

    pygame.display.flip()
    clock.tick(FPS)