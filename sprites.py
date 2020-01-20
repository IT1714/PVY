import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game,a,j):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((15,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH/2,HEIGHT-60)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.j=j
        self.a=a
    
    def jump(self):
        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
        if hits:
            self.vel.y = self.j

   

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -self.a
        if keys[pg.K_d]:
            self.acc.x = self.a


        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + self.a * self.acc

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
        if self.rect.top <30:
            if self.rect.left > WIDTH +100:
                self.rect.left = -10
                self.rect.top =HEIGHT -60
            if self.rect.right <-100:
                self.rect.right = WIDTH +10
                self.rect.top =HEIGHT -60
        else:
            if self.rect.left > WIDTH +100:
                self.rect.left = -10
            if self.rect.right <-100:
                self.rect.right = WIDTH +10

class Mob2(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = random.choice([-10,HEIGHT+10])
        self.vy = random.randrange(3,6)
        if self.rect.centery>HEIGHT:
            self.vy *=-1
        self.rect.x = random.randrange(WIDTH-60)
        self.vx =0
        self.dx = 0.5

    def update(self):
        self.rect.y += self.vy
        self.vx += self.dx
        if self.vx >3 or self.vx <-3:
            self.dx *=-1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.x += self.vx
        if self.rect.bottom > HEIGHT +100:
            self.rect.bottom =-10
        if self.rect.top <-100:
            self.rect.top =HEIGHT +10

class Boss(pg.sprite.Sprite):
    def __init__(self,game,s,):
        self.groups = game.all_sprites, game.boss
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT/3
        self.vy = s+3
        if self.rect.centery>WIDTH:
            self.vy *=-1
        self.rect.x = random.randrange(WIDTH-60)
        self.vx =0
        self.dx = 0.5
        

    def update(self):
        self.rect.x += self.vy
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        if self.rect.left > WIDTH:
            self.rect.right =0
        if self.rect.right <0:
            self.rect.left =WIDTH
        
    
class Boss_bullet(pg.sprite.Sprite):
    def __init__(self,game,s):
        self.groups = game.all_sprites, game.boss_bullet
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((10,10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = random.choice([-40,-30,-20,-10])
        self.vy = s+3
        self.rect.x = random.randrange(WIDTH)

    def update(self):
        self.rect.y += self.vy
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        if self.rect.top >HEIGHT:
            self.kill()

class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y