import pygame
import random
import sys

# Inicializace
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball Deluxe 🎯")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Barvy
WHITE = (255, 255, 255)
RED   = (255, 60, 60)
GOLD  = (255, 215, 0)
BLACK = (0, 0, 0)
BLUE  = (80, 150, 255)
BG_TOP = (10, 10, 40)
BG_BOTTOM = (40, 40, 100)

# Font
font = pygame.font.SysFont("arial", 32, bold=True)

# Zvuky (můžeš nahradit vlastními soubory .wav)
#catch_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.get_init() and pygame.mixer.Sound(buffer=b'\x00'*10))))
#pygame.mixer.music.load(pygame.mixer.music.get_busy() and "background.mp3" or pygame.mixer.music.get_busy() or pygame.mixer.Sound)
# Pokud nemáš žádné zvuky, Pygame je přeskočí bez chyby

# Hudba na pozadí (volitelně)
#pygame.mixer.music.stop()

# Hráč (košík)
basket_width, basket_height = 120, 25
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 70
basket_speed = 8

# Herní proměnné
score = 0
lives = 3
game_over = False
object_speed = 4
spawn_delay = 40
frame_count = 0

# Typy objektů
object_types = [
    {"color": RED,  "points": 1, "radius": 15, "type": "ball"},
    {"color": GOLD, "points": 3, "radius": 18, "type": "gold"},
    {"color": BLACK,"points": -1, "radius": 20, "type": "bomb"},
]
falling_objects = []

# Gradient pozadí
def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

# Přidání nového objektu
def spawn_object():
    obj_type = random.choice(object_types)
    obj = {
        "x": random.randint(obj_type["radius"], WIDTH - obj_type["radius"]),
        "y": -obj_type["radius"],
        "type": obj_type
    }
    falling_objects.append(obj)

# Hlavní herní smyčka
while True:
    screen.fill((0, 0, 0))
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Pohyb hráče
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        # Spawn nových objektů
        frame_count += 1
        if frame_count >= spawn_delay:
            spawn_object()
            frame_count = 0

        # Pohyb objektů
        for obj in falling_objects[:]:
            obj["y"] += object_speed

            # Kolize
            if basket_y < obj["y"] + obj["type"]["radius"] < basket_y + basket_height and \
               basket_x < obj["x"] < basket_x + basket_width:
                if obj["type"]["type"] == "bomb":
                    lives -= 1
                else:
                    score += obj["type"]["points"]
                falling_objects.remove(obj)
                # pygame.mixer.Sound.play(catch_sound)
                continue

            # Když spadne mimo
            if obj["y"] > HEIGHT:
                if obj["type"]["type"] != "bomb":
                    lives -= 1
                falling_objects.remove(obj)

        # Zvyšování obtížnosti
        object_speed = 4 + score * 0.1
        spawn_delay = max(15, 40 - score // 2)

        if lives <= 0:
            game_over = True

    # Vykreslení košíku
    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height), border_radius=10)

    # Vykreslení objektů
    for obj in falling_objects:
        pygame.draw.circle(screen, obj["type"]["color"], (int(obj["x"]), int(obj["y"])), obj["type"]["radius"])

    # Text
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (WIDTH - 150, 20))

    if game_over:
        over_text = font.render("GAME OVER! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
        if keys[pygame.K_r]:
            score = 0
            lives = 3
            falling_objects.clear()
            object_speed = 4
            spawn_delay = 40
            game_over = False

    pygame.display.flip()
    clock.tick(FPS)
