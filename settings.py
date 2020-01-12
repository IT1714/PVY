TITLE = "GAME 5HEAD"
WIDTH = 920
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'
HS_file = "hightscore.txt"

MOB_FREQ = 1200

#player
PLAYER_ACC = 0.675
PLAYER_FRICTION = -0.17
PLAYER_GRAV = 0.6
JUMP = -10
 

#platforms
PLATFORM_LVL1 = [#bottom
                (20, HEIGHT - 20, WIDTH/5,20),
                (WIDTH/2-75,HEIGHT-20,150,20),
                (WIDTH-WIDTH/5-20,HEIGHT-20,WIDTH/5-20,20),
                #left
                (WIDTH/8,(HEIGHT/7)*6,75,10),
                (WIDTH/4,HEIGHT*0.7,100,10),
                ((WIDTH/6)-25, HEIGHT*0.585,50,10),
                (WIDTH/4,HEIGHT*0.47,100,10),
                (WIDTH/8,(HEIGHT/7)*2.3,75,10),
                #right
                ((WIDTH/8)*7-75,(HEIGHT/7)*6,75,10),
                ((WIDTH/4)*3-100,HEIGHT* 0.7,100,10),
                ((WIDTH/6)*5-25, HEIGHT*0.585,50,10),
                ((WIDTH/4)*3-100,HEIGHT*0.47,100,10),
                ((WIDTH/8)*7-75,(HEIGHT/7)*2.3,75,10),
                #center
                (WIDTH/2-50, HEIGHT *0.4,100,10),
                (WIDTH/2-50, HEIGHT * 0.8,100,10)
                ]


#colors
WHITE = (255,255,255) 
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0,155,155)
PINK = (255,105,180)
BGCOLOR = LIGHTBLUE