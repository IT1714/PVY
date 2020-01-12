import pygame as pg
import random
from settings import *
from sprites import *
from os import path
vec = pg.math.Vector2


class Game:
    def __init__(self):
        #initialize game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_icon(pg.image.load("png/001-sword.png"))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.pom=0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.load_data()
        
    def load_data(self):
        self.dir= path.dirname(__file__)
        with open(path.join(self.dir, HS_file), 'w') as f:
            try:
                self.hightscore = int(f.read())
            except:
                self.hightscore = 0
        self.snd_dir=path.join(self.dir, 'snd')
        self.laser_sound = pg.mixer.Sound(path.join(self.snd_dir, 'laser7.ogg'))
        self.exp_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Explosion.ogg'))
    def new(self):
        #new game
        pg.mixer.music.load("snd/StarWarsCantinaBand.ogg")
        pg.mixer.music.set_volume(0.09)
        self.hp = 3
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.bullets = pg.sprite.Group( )
        self.mobs = pg.sprite.Group()
        self.mob_timer =0
        self.hit_timer =0
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LVL1:
            p = Platform(*plat )
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        #loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        #loop - update
        self.all_sprites.update()

        #mob spawn?
        now1 = pg.time.get_ticks()
        if now1-self.mob_timer > MOB_FREQ + random.choice([-500,0,500]):
            self.mob_timer = now1
            Mob(self)
        mob_hits = pg.sprite.spritecollide(self.player,self.mobs,False)
        now2 = pg.time.get_ticks()
        if now2-self.hit_timer >1000 and mob_hits:
            self.hit_timer = now2
            self.hp -=1
        bullets_hits = pg.sprite.groupcollide(self.bullets,self.mobs,True,True)
        if bullets_hits:
            self.exp_sound.play()
            self.score +=10
            self.pom +=10
        
        if self.pom==100:
            if self.hp < 3:
                self.hp += 1
            self.pom =0


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
        if self.hp==0:
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
            if event.key == pg.K_UP:
                self.laser_sound.play()
                bullet = Bulett(self.player.rect.centerx, self.player.rect.top, -10, 1)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
            if event.key == pg.K_LEFT:
                self.laser_sound.play()
                bullet = Bulett(self.player.rect.centerx, self.player.rect.top, -10, 0)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
            if event.key == pg.K_RIGHT:
                self.laser_sound.play()
                bullet = Bulett(self.player.rect.centerx, self.player.rect.top, 10, 0)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
           




    def draw(self):
        #loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),40,WHITE,WIDTH/2,10)
        self.draw_text(str(self.hp),40,WHITE,WIDTH-65,10)
        if self.hp == 3:
            pg.draw.rect(self.screen,PINK,(WIDTH-45,10,40,40))
        if self.hp == 2:
            pg.draw.rect(self.screen,PINK,(WIDTH-45,10,40,40))
            pg.draw.rect(self.screen,BLACK,(WIDTH-45,10,40,20))
        if self.hp == 1:
            pg.draw.rect(self.screen,PINK,(WIDTH-45,10,40,40))
            pg.draw.rect(self.screen,BLACK,(WIDTH-45,10,40,30))

        # *after* DRAW 
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load("snd/sax.ogg")
        pg.mixer.music.set_volume(0.07)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press  space to play",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("A,D pohyb, Space skok",20,BLACK,WIDTH/2,(HEIGHT/8)*7)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    
    def show_menu_screen(self):
        self.screen.fill(BGCOLOR)
        pg.mixer.music.set_volume(0.03)
        self.draw_text("GAME MENU",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press space to play",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("A,D pohyb, Space skok",20,BLACK,WIDTH/2,(HEIGHT/8)*7)
        self.draw_text("Score: " +str(self.score),20,BLACK,WIDTH/2,HEIGHT/1.85)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.set_volume(0.09)
    
    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load("snd/You Died.ogg")
        pg.mixer.music.set_volume(0.07)
        pg.mixer.music.play(loops=1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER",40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Press space to play again",30,BLACK,WIDTH/2,HEIGHT/2.25)
        self.draw_text("Score: " +str(self.score),20,BLACK,WIDTH/2,HEIGHT/1.7)
        if self.score > self.hightscore:
            self.hightscore = self.score
            self.draw_text("LMAO, Nove Hight Score", 30,BLACK,WIDTH/2,HEIGHT-60)
            with open(path.join(self.dir, HS_file),'w') as f:
                f.write(str(self.hightscore))
        else:
            self.draw_text("Hight Score: " +str(self.hightscore),20,BLACK,WIDTH/2,HEIGHT/1.9)
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