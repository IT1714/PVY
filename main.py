import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        #initialize game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_icon(pg.image.load("png/001-sword.png"))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
    
    def new(self):
        #new game
        self.time = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LVL1:
            p = Platform(*plat )
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        #loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #loop - update
        
        self.all_sprites.update()
        if self.player.vel.y >0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                self.player.pos.y = hits[0].rect.top+1
                self.player.vel.y = 0
               
        #KYS
        if self.player.rect.bottom > HEIGHT:
            for sprites in self.all_sprites:
                sprites.rect.y -= max(self.player.vel.y,10)
                if sprites.rect.bottom < 0:
                    sprites.kill()
            if len(self.platforms)==0:        
                self.playing = False

    def events(self):
        #loop - event
       for event in pg.event.get():
        if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.player.jump() 
            if event.key == pg.K_ESCAPE:
                self.show_menu_screen()




    def draw(self):
        #loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.time),40,WHITE,WIDTH/2,HEIGHT/4)

        # *after* DRAW 
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("ZULUL",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press any key to play",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("Arrows to move, Space to jump",20,BLACK,WIDTH/2,HEIGHT/1.85)
        pg.display.flip()
        self.wait_for_key()
    
    def show_menu_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("ZULUL",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press space to play",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("Arrows to move, Space to jump",20,BLACK,WIDTH/2,HEIGHT/1.85)
        pg.display.flip()
        self.wait_for_key()
    
    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press any key to play again",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("TIME: " +str(self.time),20,BLACK,WIDTH/2,HEIGHT/1.85)
        pg.display.flip()
        self.wait_for_key()
    
    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
    
    def wait_for_key(self):
        wait=True
        while wait:
            self.clock.tick(FPS)
            for events in pg.event.get():
                if events.type == pg.QUIT:
                    wait=False
                    self.running=False
                if events.type == pg.KEYUP:
                    if events.key == pg.K_SPACE:
                        wait=False




g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()