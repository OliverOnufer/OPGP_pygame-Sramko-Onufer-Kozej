import pygame
import math
from pathlib import Path
from settings import *

# Načítanie zvuku dotyku lopty
def load_click_sound():
    sound_folder = Path(__file__).parent / "sounds"
    for ext in ("wav", "mp3", "ogg"):
        sound_path = sound_folder / f"click.{ext}"
        if sound_path.exists():
            try:
                return pygame.mixer.Sound(sound_path)
            except pygame.error:
                pass
    return None

class Lopta:
    click_sound = None
    
    def __init__(self):
        if Lopta.click_sound is None:
            Lopta.click_sound = load_click_sound()
        self.radius = POLOMER_LOPTY
        self.image = self.load_ball_image()
        self.reset(1)

    def load_ball_image(self):
        img_folder = Path(__file__).parent / "images"
        for ext in ("png", "jpg", "jpeg", "webp", "bmp"):
            for img_path in img_folder.glob(f"ball.{ext}"):
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    size = self.radius * 2
                    return pygame.transform.scale(img, (size, size))
                except pygame.error:
                    pass
        return None

    def reset(self, side):
        self.x = 200 if side == 1 else SIRKA_OKNA - 200
        self.y = 425
        self.vel_x = 0
        self.vel_y = 0
        self.waiting = True  # Čaká na dotyk hráča

    def update(self, hraci):
        # Ak lopta čaká, nehybe sa - len kontroluje kolíziu s hráčmi
        if not self.waiting:
            self.vel_y += GRAVITACIA * 0.6
            self.x += self.vel_x
            self.y += self.vel_y

        # Kolízia s ľavou stenou
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vel_x *= -0.9
        # Kolízia s pravou stenou
        if self.x + self.radius > SIRKA_OKNA:
            self.x = SIRKA_OKNA - self.radius
            self.vel_x *= -0.9
        # Kolízia so stropom
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vel_y *= -0.9

        # Kolízia so sieťou
        net_left = SIRKA_OKNA//2 - SIRKA_SIETE//2
        net_right = SIRKA_OKNA//2 + SIRKA_SIETE//2
        net_top = VYSKA_OKNA - VYSKA_PODLAHY - VYSKA_SIETE

        # Kontrola či lopta koliduje so sieťou (vrátane polomeru)
        if self.x + self.radius > net_left and self.x - self.radius < net_right:
            if self.y + self.radius > net_top:
                # Kolízia zhora (lopta dopadla na sieť)
                if self.vel_y > 0 and self.y - self.radius < net_top:
                    self.y = net_top - self.radius
                    self.vel_y *= -0.7
                # Kolízia zboku
                else:
                    if self.x < SIRKA_OKNA // 2:
                        self.x = net_left - self.radius
                    else:
                        self.x = net_right + self.radius
                    self.vel_x *= -0.9

        for h in hraci:
            dist = math.hypot(self.x - h.x, self.y - h.y)
            min_dist = self.radius + h.radius
            if dist < min_dist and dist > 0:
                if Lopta.click_sound:
                    Lopta.click_sound.play()
                
                # Ak lopta čakala, teraz sa začne hýbať
                if self.waiting:
                    self.waiting = False
                
                # Vypočítaj uhol odrazu
                angle = math.atan2(self.y - h.y, self.x - h.x)
                
                # Posuň loptu mimo hráča (aby sa nelepila)
                overlap = min_dist - dist
                self.x += math.cos(angle) * (overlap + 1)
                self.y += math.sin(angle) * (overlap + 1)
                
                # Nastav rýchlosť odrazu - vyššia minimálna rýchlosť
                current_speed = math.hypot(self.vel_x, self.vel_y)
                speed = max(12, current_speed * 1.1)  # Minimálne 12
                self.vel_x = math.cos(angle) * speed
                self.vel_y = math.sin(angle) * speed

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(screen, ZLTA, (int(self.x), int(self.y)), self.radius)
            