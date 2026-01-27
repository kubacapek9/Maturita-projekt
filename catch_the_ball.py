import pygame
import random
import sys

# Inicializace
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball 🎯")

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

# Herní stavy
LOGIN = 0
PLAYING = 1
GAME_OVER = 2
game_state = LOGIN

player_name = ""

# Hráč (košík)
basket_width, basket_height = 120, 25
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 70
basket_speed = 14

# Herní proměnné
score = 0
lives = 3
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

# Přidání objektu
def spawn_object():
    obj_type = random.choice(object_types)
    obj = {
        "x": random.randint(obj_type["radius"], WIDTH - obj_type["radius"]),
        "y": -obj_type["radius"],
        "type": obj_type
    }
    falling_objects.append(obj)

# Hlavní smyčka
while True:
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # LOGIN – psaní jména
        if game_state == LOGIN and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name.strip() != "":
                game_state = PLAYING
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 12:
                    player_name += event.unicode

    keys = pygame.key.get_pressed()

    # ---------- LOGIN ----------
    if game_state == LOGIN:
        title = font.render("Enter your name", True, WHITE)
        name_text = font.render(player_name + "|", True, GOLD)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 70))
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 200, HEIGHT//2 - 10, 400, 50), 2)
        screen.blit(name_text, (WIDTH//2 - 180, HEIGHT//2))

    # ---------- HRA ----------
    elif game_state == PLAYING:
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        frame_count += 1
        if frame_count >= spawn_delay:
            spawn_object()
            frame_count = 0

        for obj in falling_objects[:]:
            obj["y"] += object_speed

            if basket_y < obj["y"] + obj["type"]["radius"] < basket_y + basket_height and \
               basket_x < obj["x"] < basket_x + basket_width:
                if obj["type"]["type"] == "bomb":
                    lives -= 1
                else:
                    score += obj["type"]["points"]
                falling_objects.remove(obj)
                continue

            if obj["y"] > HEIGHT:
                if obj["type"]["type"] != "bomb":
                    lives -= 1
                falling_objects.remove(obj)

        object_speed = 4 + score * 0.1
        spawn_delay = max(15, 40 - score // 2)

        if lives <= 0:
            game_state = GAME_OVER

        pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height), border_radius=10)

        for obj in falling_objects:
            pygame.draw.circle(screen, obj["type"]["color"],
                               (int(obj["x"]), int(obj["y"])),
                               obj["type"]["radius"])

        screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 150, 20))
        screen.blit(font.render(f"Player: {player_name}", True, WHITE), (20, 55))

    # ---------- GAME OVER ----------
    elif game_state == GAME_OVER:
        over = font.render(f"Game Over, {player_name}!", True, RED)
        final_score = font.render(f"Final Score: {score}", True, GOLD)
        restart = font.render("Press R to Restart", True, WHITE)

        screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 70))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 - 20))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 30))

        if keys[pygame.K_r]:
            score = 0
            lives = 3
            falling_objects.clear()
            object_speed = 4
            spawn_delay = 40
            basket_x = WIDTH // 2 - basket_width // 2
            game_state = PLAYING

    pygame.display.flip()
    clock.tick(FPS)

