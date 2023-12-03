import pygame
from pygame.locals import *
import sys
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from item import Item
from constantes import *

flags = DOUBLEBUF
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags, 16)
pygame.init()
clock = pygame.time.Clock()

background = Background(0, 0, ANCHO_VENTANA, ALTO_VENTANA, f"images\locations\goku_house.png")
player = Player(x=0,y=400,speed_walk=6,speed_run=12,gravity=20,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)

enemies = []
enemies.append (Enemy(x=450,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
enemies.append (Enemy(x=700,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
enemies.append (Enemy(x=150,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))

plataformas = []
plataformas.append(Plataform(x=100,y=500,width=220,height=50,type=1))
plataformas.append(Plataform(x=500,y=500,width=150,height=50,type=2))   
plataformas.append(Plataform(x=600,y=430,width=230,height=50,type=12))
plataformas.append(Plataform(x=1020,y=540,width=800,height=50,type=12))


coins_sprites = pygame.sprite.Group()

coin1 = Item(170, 470)
coin2 = Item(570, 479)
coin3 = Item(714, 402)
coin4 = Item(1304, 508)
coins_sprites.add(coin1, coin2, coin3, coin4)

all_sprites = pygame.sprite.Group()
all_sprites.add(player,coin1, coin2, coin3, coin4 )


# coins_group = pygame.sprite.Group()
# coins_group.add(Item(100, 520))
# coins_group.add(Item(500, 620))
# coins_group.add(Item(600, 410))



flag_disparo = True
tiempo_ultimo_disparo = 0

while True:
    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()
    background.draw(screen)
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        
    
    # player update -- verificar como el player interctua con el nivel
    player.update(delta_ms,plataformas, keys, screen)
    
    # update de los enemigos
    for enemy in enemies:
        enemy.update(delta_ms, enemies)
        enemy.draw(screen)
        
    for platforma in plataformas:
        platforma.draw(screen)
        
    coins_sprites.update(delta_ms)
    coins_sprites.draw(screen)
    player.draw(screen)
    
    # Actualizar todos los sprites en el grupo
    # all_sprites.update(delta_ms=delta_ms, plataform_list=plataformas, keys=keys, screen=screen)

    # # Detectar colisiones con los items
    # collisions = pygame.sprite.spritecollide(player, coins_sprites, True)  # True para eliminar los items al colisionar

    # for item in collisions:
    #     # Manejar lo que sucede cuando el jugador colisiona con un item
    #     player.score += 1

    pygame.display.flip()
