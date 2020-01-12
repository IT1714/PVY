import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((15,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH/2,HEIGHT-60)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def jump(self):
        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
        if hits:
            self.vel.y = JUMP

   

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC


        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + PLAYER_ACC * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH


        self.rect.midbottom = self.pos
    

class Bulett(pg.sprite.Sprite):
    def __init__(self,x,y,s,k):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((4,6))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = s
        self.key = k

    def update(self):
        if self.key == 1:
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()
        else:
            self.rect.x += self.speedy
            if self.rect.bottom < 0:
                self.kill()



class Mob(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((20,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-10,WIDTH+10])
        self.vx = random.randrange(3,6)
        if self.rect.centerx>WIDTH:
            self.vx *=-1
        self.rect.y = random.randrange(HEIGHT-60)
        self.vy =0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy >3 or self.vy <-3:
            self.dy *=-1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH +100 or self.rect.right <-100:
            self.kill()
         



class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y