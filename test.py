import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 1050
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Avoidance Game")

# Load bomb sprite images
BOMB_IMAGES = [
    pygame.image.load("images/bomb1.png"),
    pygame.image.load("images/bomb2.png"),
    pygame.image.load("images/bomb3.png"),
    pygame.image.load("images/bomb4.png"),
    pygame.image.load("images/bomb5.png"),
    pygame.image.load("images/bomb6.png")
]
BOMB_SIZES = [image.get_size() for image in BOMB_IMAGES]

# Load leaf sprite images
LEAF_IMAGES = [
    pygame.image.load("images/leaf1.png"),
    pygame.image.load("images/leaf2.png"),
    pygame.image.load("images/leaf3.png"),
    pygame.image.load("images/leaf4.png"),
    pygame.image.load("images/leaf5.png"),
    pygame.image.load("images/leaf6.png"),
    pygame.image.load("images/leaf7.png"),
    pygame.image.load("images/leaf8.png")
]
LEAF_SIZES = [image.get_size() for image in LEAF_IMAGES]

# Game constants
BOMB_SPAWN_INTERVAL = 1000  # milliseconds
LEAF_SPAWN_INTERVAL = 300  # milliseconds
MIN_BOMB_SPEED = 4
MAX_BOMB_SPEED = 4
MIN_LEAF_SPEED = 4
MAX_LEAF_SPEED = 4
NO_TAP_TIMEOUT = 300000  # milliseconds

# Game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
score = 0
last_tap_time = pygame.time.get_ticks()
bombs = []
leaves = []
last_bomb_spawn_time = pygame.time.get_ticks()
last_leaf_spawn_time = pygame.time.get_ticks()

class FallingObject:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.width, self.height = image.get_size()

    def move(self):
        self.y += self.speed

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > HEIGHT

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))

def spawn_bomb():
    image_index = random.randint(0, len(BOMB_IMAGES) - 1)
    image = BOMB_IMAGES[image_index]
    x = random.randint(0, WIDTH - BOMB_SIZES[image_index][0])
    speed = random.randint(MIN_BOMB_SPEED, MAX_BOMB_SPEED)
    bomb = FallingObject(image, x, 0, speed)
    bombs.append(bomb)

def spawn_leaf():
    image_index = random.randint(0, len(LEAF_IMAGES) - 1)
    image = LEAF_IMAGES[image_index]
    x = random.randint(0, WIDTH - LEAF_SIZES[image_index][0])
    speed = random.randint(MIN_LEAF_SPEED, MAX_LEAF_SPEED)
    leaf = FallingObject(image, x, 0, speed)
    leaves.append(leaf)

def main():
    global score, last_tap_time, last_bomb_spawn_time, last_leaf_spawn_time

    running = True
    while running:
        SCREEN.fill((0, 0, 0))  # Clear screen with black
        current_time = pygame.time.get_ticks()

        # Spawn bombs at regular intervals
        if current_time - last_bomb_spawn_time > BOMB_SPAWN_INTERVAL:
            spawn_bomb()
            last_bomb_spawn_time = current_time

        # Spawn leaves at regular intervals
        if current_time - last_leaf_spawn_time > LEAF_SPAWN_INTERVAL:
            spawn_leaf()
            last_leaf_spawn_time = current_time

        # Move and draw leaves
        for leaf in leaves[:]:
            leaf.move()
            leaf.draw()
            if leaf.is_off_screen():
                leaves.remove(leaf)

        # Move and draw bombs
        for bomb in bombs[:]:
            bomb.move()
            bomb.draw()
            if bomb.is_off_screen():
                bombs.remove(bomb)
                score += 1

        draw_score()

        # Check for game over due to no taps
        if current_time - last_tap_time > NO_TAP_TIMEOUT:
            running = False

        pygame.display.flip()
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                last_tap_time = pygame.time.get_ticks()
                mouse_x, mouse_y = event.pos
                for bomb in bombs[:]:
                    if bomb.x < mouse_x < bomb.x + bomb.width and bomb.y < mouse_y < bomb.y + bomb.height:
                        running = False
                for leaf in leaves[:]:
                    if leaf.x < mouse_x < leaf.x + leaf.width and leaf.y < mouse_y < leaf.y + leaf.height:
                        leaves.remove(leaf)
                        score += 1

    print(f"Game Over! Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()