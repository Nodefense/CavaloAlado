import pygame
import os
import random

WIDTH = 500
HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
loop = True

class Cavalo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (60, HEIGHT / 2)
        self.accelerationy = 0.5
        self.speedy = 0

    def update(self):
        self.speedy += self.accelerationy
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 10 or self.rect.top < 0:
            pygame.quit()

class TopTube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((75, y))
        self.image.fill(BLACK)
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
        self.image = pygame.Surface((75, HEIGHT - y))
        self.image.fill(BLACK)
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
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CavaloAlado')
clock = pygame.time.Clock()

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

while loop:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN:
            # I had to write elif because if I just wrote "pygame.K_UP or pygame.K_SPACE or pygame.K_w", it would recognise any key on the keyboard.
            if event.key == pygame.K_UP:
                cavalo.speedy = -7.5
            elif event.key == pygame.K_SPACE:
                cavalo.speedy = -7.5
            elif event.key == pygame.K_w:
                cavalo.speedy = -7.5

    for tube in singleTubes:
        if tube.rect.right < WIDTH:
            createTubes(WIDTH + 200, random.randint(125, 575))
            singleTubes.remove(tube)

    sprites.update()
    collision = pygame.sprite.spritecollide(cavalo, tubes, False)
    if collision:
        pygame.quit()
    DISPLAY.fill(WHITE)
    sprites.draw(DISPLAY)
    pygame.display.flip()
    print(tubes)

pygame.quit()