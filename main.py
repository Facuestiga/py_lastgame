import pygame
from controller import pause
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
# pygame.mixer.music.load(r"sounds\sonido_intergalactic_odyssey.ogg")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.1)

fuente = pygame.font.SysFont("Arial", 30, True)
clock = pygame.time.Clock()
aux_time = 1

background = Background(0, 0, ANCHO_VENTANA, ALTO_VENTANA, f"images\locations\goku_house.png")
player = Player(x=0,y=400,speed_walk=6,speed_run=12,gravity=20,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)

enemies = []
enemies.append (Enemy(x=600,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
enemies.append (Enemy(x=700,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))

# enemies_group = pygame.sprite.Group()
# enemy1 = Enemy(x=600,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300)
# enemy2 = Enemy(x=700,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300)
# enemies_group.add(enemy1, enemy2)



plataformas = []
plataformas.append(Plataform(x=100,y=500,width=220,height=50,type=1))
plataformas.append(Plataform(x=500,y=500,width=150,height=50,type=2))   
plataformas.append(Plataform(x=690,y=430,width=230,height=50,type=12))
plataformas.append(Plataform(x=897,y=512,width=100,height=50,type=12))
plataformas.append(Plataform(x=1020,y=540,width=800,height=50,type=12))


coins_sprites = pygame.sprite.Group()

coin1 = Item(170, 470)
coin2 = Item(570, 479)
coin3 = Item(714, 402)
coin4 = Item(1304, 508)
coins_sprites.add(coin1, coin2, coin3, coin4)

lista_coins = []
lista_coins.append(Item(170, 470))
lista_coins.append(Item(570, 479))
lista_coins.append(Item(714, 402))
lista_coins.append(Item(1304, 508))

while True:
    time = int(pygame.time.get_ticks()/1000) #tiempo de juego
    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()
    background.draw(screen)
    contador_time = fuente.render("Tiempo: " + str(time),0, C_BLACK)
    screen.blit(contador_time, (52, 25))
        
    for event in lista_eventos:
        # Salir
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Pausa
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.music.pause()
                pause()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        
    
    # player update -- verificar como el player interctua con el nivel
    player.update(delta_ms,plataformas, keys)
    
    # update de los enemigos
    for enemy in enemies:
        enemy.update(delta_ms, enemies)
        enemy.draw(screen)
        
    for platforma in plataformas:
        platforma.draw(screen)
        
        
    for coin in lista_coins:
        coin.update(delta_ms, player)
        coin.draw(screen)
    
    
    for bala in player.list_balas:
        bala.update()
        screen.blit(bala.superficie, bala.rectangulo)

        
     
    # coins_sprites.update(delta_ms)
    # coins_sprites.draw(screen)
    player.draw(screen)
    
    # Actualizar todos los sprites en el grupo
    # all_sprites.update(delta_ms=delta_ms, plataform_list=plataformas, keys=keys, screen=screen)

    # # Detectar colisiones con los items
    # collisions = pygame.sprite.spritecollide(player, coins_sprites, True)  # True para eliminar los items al colisionar

    # for item in collisions:
    #     # Manejar lo que sucede cuando el jugador colisiona con un item
    #     player.score += 1

    pygame.display.flip()
