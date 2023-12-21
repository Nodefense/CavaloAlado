import pygame
import os
import random
import time

folder = os.path.dirname(__file__)
assets_folder = os.path.join(folder, 'assets')

WIDTH = 500
HEIGHT = 700
FREQUENCY = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5

class Cavalo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (60, HEIGHT / 2)
        self.speedy = 0

    def update(self):
        self.speedy += GRAVITY
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 10 or self.rect.top < 0:
            pygame.quit()

class TopTube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((75, y))
        self.image = top_tube_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speedx = -3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

class BottomTube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((75, HEIGHT - y))
        self.image = bottom_tube_image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.speedx = -3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

    def onScreen(self):
        if self.rect.right < WIDTH:
            return True
        else:
            return False

pygame.init()
pygame.mixer.init()
pygame.font.init()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CavaloAlado')
clock = pygame.time.Clock()
player_image = pygame.image.load(os.path.join(assets_folder, 'cavaloplaceholder1.png')).convert()
top_tube_image = pygame.image.load(os.path.join(assets_folder, 'pipe_top.png')).convert()
bottom_tube_image = pygame.image.load(os.path.join(assets_folder, 'pipe_bottom.png')).convert()
background_image = pygame.image.load(os.path.join(assets_folder, 'PaulinaRiva_tilesetOpenGameBackground2.png')).convert()
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
game_over = font.render(f'GAME OVER. SCORE: {score}', True, BLACK, WHITE)
game_over_rect = game_over.get_rect()
game_over_rect.center = (WIDTH//2, HEIGHT//2)

tubes_list = []
sprites = pygame.sprite.Group()
tubes = pygame.sprite.Group()
singleTubes = pygame.sprite.Group()
cavalo = Cavalo()
toptube = TopTube(WIDTH + 100, 275)
bottomtube = BottomTube(WIDTH + 100, 425)
sprites.add(cavalo)
sprites.add(toptube)
sprites.add(bottomtube)
tubes.add(toptube)
tubes.add(bottomtube)
singleTubes.add(toptube)

def createTubes(x, y):
    toptube = TopTube(x, y - 75)
    bottomtube = BottomTube(x, y + 75)
    sprites.add(toptube)
    sprites.add(bottomtube)
    tubes.add(toptube)
    tubes.add(bottomtube)
    singleTubes.add(toptube)
    tubes_list.append(toptube)

while True:
    clock.tick(FREQUENCY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            # I had to write elif because if I just wrote "pygame.K_UP or pygame.K_SPACE or pygame.K_w", it would recognise any key on the keyboard.
            if event.key == pygame.K_UP:
                if GRAVITY > 0:
                    cavalo.speedy = -7.5
                else:
                    cavalo.speedy = 7.5
            elif event.key == pygame.K_SPACE:
                if GRAVITY > 0:
                    cavalo.speedy = -7.5
                else:
                    cavalo.speedy = 7.5
            elif event.key == pygame.K_w:
                cavalo.speedy = -7.5
            if event.key == pygame.K_g:
                if GRAVITY > 0:
                    GRAVITY = -GRAVITY
                else:
                    GRAVITY = abs(GRAVITY)

    for tube in singleTubes:
        if tube.rect.right < WIDTH:
            createTubes(WIDTH + 200, random.randint(125, 575))
            singleTubes.remove(tube)

    sprites.update()
    score += 1
    collision = pygame.sprite.spritecollide(cavalo, tubes, False)
    if collision:
        DISPLAY.blit(font.render(f'GAME OVER. SCORE: {score//75-2}', True, BLACK, WHITE), game_over_rect)
        pygame.display.flip()
        time.sleep(1)
        break
    DISPLAY.blit(background_image, (0, 0))
    sprites.draw(DISPLAY)
    pygame.display.flip()
pygame.quit()