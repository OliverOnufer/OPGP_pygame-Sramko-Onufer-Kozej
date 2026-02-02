import pygame
import math
from pathlib import Path
from settings import *

# Načítanie zvuku skoku
def load_jump_sound():
    sound_folder = Path(__file__).parent / "sounds"
    for ext in ("wav", "mp3", "ogg"):
        sound_path = sound_folder / f"jump.{ext}"
        if sound_path.exists():
            try:
                return pygame.mixer.Sound(sound_path)
            except pygame.error:
                pass
    return None

class Hrac:
    jump_sound = None
    
    def __init__(self, x, meno):
        if Hrac.jump_sound is None:
            Hrac.jump_sound = load_jump_sound()
        self.x = x
        self.y = VYSKA_OKNA - VYSKA_PODLAHY - POLOMER_HRACA
        self.radius = POLOMER_HRACA
        self.vel_y = 0
        self.na_zemi = False
        self.meno = meno
        self.animation_time = 0
        self.vel_x = 0
        
        # Farby hráčov podľa tímu
        if meno == "Yamal":  # Barcelona
            self.barva_tela = BAR_CERVENA
            self.barva_nohavic = BAR_MODRA
            self.barva_tela_light = (220, 100, 100)
        else:  # Mbappe - Real Madrid
            self.barva_tela = RM_BIELA
            self.barva_nohavic = RM_CERNA
            self.barva_tela_light = (200, 200, 200)

    def update(self, keys):
        prev_vel_x = self.vel_x
        self.vel_x = 0
        
        if keys[KEY_MAP[f"{self.meno}_LEFT"]]:
            self.x -= RYCHLOST_HRACA
            self.vel_x = -RYCHLOST_HRACA
        if keys[KEY_MAP[f"{self.meno}_RIGHT"]]:
            self.x += RYCHLOST_HRACA
            self.vel_x = RYCHLOST_HRACA
        if keys[KEY_MAP[f"{self.meno}_JUMP"]] and self.na_zemi:
            self.vel_y = SILA_SKOKU
            self.na_zemi = False
            if Hrac.jump_sound:
                Hrac.jump_sound.play()

        self.vel_y += GRAVITACIA
        self.y += self.vel_y

        if self.y + self.radius > VYSKA_OKNA - VYSKA_PODLAHY:
            self.y = VYSKA_OKNA - VYSKA_PODLAHY - self.radius
            self.vel_y = 0
            self.na_zemi = True

        net_x = SIRKA_OKNA // 2
        if self.meno == "Yamal":
            self.x = max(self.radius, min(self.x, net_x - SIRKA_SIETE//2 - self.radius))
        else:
            self.x = max(net_x + SIRKA_SIETE//2 + self.radius, min(self.x, SIRKA_OKNA - self.radius))
        
        # Animácia
        if self.vel_x != 0 or not self.na_zemi:
            self.animation_time += 0.1
        else:
            self.animation_time = 0

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        
        # Animačný offset pre ruky a nohy
        anim = math.sin(self.animation_time * 0.3) * 8
        jump_offset = 5 if not self.na_zemi else 0
        
        # Hlava - kožná farba
        koza = (255, 200, 130)
        pygame.draw.circle(screen, koza, (x, y - 25), 14)
        
        # Oči
        pygame.draw.circle(screen, CIERNA, (x - 5, y - 27), 3)
        pygame.draw.circle(screen, CIERNA, (x + 5, y - 27), 3)
        
        # Úsmev
        pygame.draw.arc(screen, CIERNA, (x - 6, y - 24, 12, 6), 0, math.pi, 2)
        
        # Telo - dres tímu
        pygame.draw.rect(screen, self.barva_tela, (x - 10, y - 8, 20, 18))
        
        # Pruhy na drese (logo)
        if self.meno == "Yamal":
            # Barcelona pruhy
            pygame.draw.line(screen, self.barva_tela_light, (x - 6, y - 5), (x - 6, y + 8), 2)
            pygame.draw.line(screen, self.barva_tela_light, (x, y - 5), (x, y + 8), 2)
            pygame.draw.line(screen, self.barva_tela_light, (x + 6, y - 5), (x + 6, y + 8), 2)
        else:
            # Real Madrid biele čiary
            pygame.draw.circle(screen, ZLTA, (x, y), 4)
        
        # Ruky s animáciou - kožná farba
        arm_y = y + 2
        pygame.draw.line(screen, koza, (x - 10, arm_y), 
                        (x - 20 - anim, arm_y - 5 + anim), 4)
        # Ľavá dlaň
        pygame.draw.circle(screen, koza, (int(x - 20 - anim), int(arm_y - 5 + anim)), 5)
        
        # Pravá ruka
        pygame.draw.line(screen, koza, (x + 10, arm_y), 
                        (x + 20 + anim, arm_y - 5 + anim), 4)
        # Pravá dlaň
        pygame.draw.circle(screen, koza, (int(x + 20 + anim), int(arm_y - 5 + anim)), 5)
        
        # Nohy s animáciou
        leg_y = y + 16
        
        # Ľavá noha
        pygame.draw.line(screen, self.barva_nohavic, (x - 5, leg_y), 
                        (x - 8 - anim, leg_y + 18 - jump_offset), 4)
        # Ľavý topánok - čierny
        pygame.draw.circle(screen, CIERNA, (int(x - 8 - anim), int(leg_y + 18 - jump_offset)), 5)
        
        # Pravá noha
        pygame.draw.line(screen, self.barva_nohavic, (x + 5, leg_y), 
                        (x + 8 + anim, leg_y + 18 - jump_offset), 4)
        # Pravý topánok - čierny
        pygame.draw.circle(screen, CIERNA, (int(x + 8 + anim), int(leg_y + 18 - jump_offset)), 5)
        
        # Meno hráča
        font = pygame.font.Font(None, 24)
        text = font.render(self.meno, True, BIELA)
        screen.blit(text, (x - 25, y - 60))