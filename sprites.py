"""
sprites.py
sprite classes
"""

import pygame
import constants as c
import random

class Player(pygame.sprite.Sprite):
    # snake
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(c.snake_head_img, (c.SIZE_OF_SBLOCK, c.SIZE_OF_SBLOCK))
        self.rect = self.image.get_rect()
        self.rect.center = (c.WIDTH/2, c.HEIGHT/2)
        self.speedx = 0
        self.speedy = 0
        self.posList = []
        self.length = 1
        self.score = 0
        self.direction = None

    def update(self):
        keystate = pygame.key.get_pressed()
        # user snake controls
        if keystate[pygame.K_LEFT]:
            self.speedx = -c.SPEED
            self.speedy = 0
            self.image = pygame.transform.rotate(c.snake_head_img, 90)
            self.direction = "L"

        elif keystate[pygame.K_RIGHT]:
            self.speedx = c.SPEED
            self.speedy = 0
            self.image = pygame.transform.rotate(c.snake_head_img, 270)
            self.direction = "R"

        elif keystate[pygame.K_UP]:
            self.speedy = -c.SPEED
            self.speedx = 0
            self.image = pygame.transform.rotate(c.snake_head_img, 360)
            self.direction = "U"

        elif keystate[pygame.K_DOWN]:
            self.speedy = c.SPEED
            self.speedx = 0
            self.image = pygame.transform.rotate(c.snake_head_img, 180)
            self.direction = "D"
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def collision(self):
        self.length += 5
        self.score += 1

class Food(pygame.sprite.Sprite):
    # squares that the snake eats to get bigger
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(c.apple_img, (c.SIZE_OF_SBLOCK+8, c.SIZE_OF_SBLOCK+8))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, (c.WIDTH)-self.rect.width-10, c.SIZE_OF_SBLOCK-10)
        self.rect.y = random.randrange(0, (c.HEIGHT)-self.rect.height-10, c.SIZE_OF_SBLOCK-10)


class Enemy(pygame.sprite.Sprite):
    # squares to avoid
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((c.SIZE_OF_SBLOCK, c.SIZE_OF_SBLOCK))
        self.image.fill(c.RED)
