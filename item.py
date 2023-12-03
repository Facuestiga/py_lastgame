import pygame
from auxiliar import Auxiliar

import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.image_coin = Auxiliar.get_surface_from_spritesheet(r"images\coin\newCoins.jpg", 24, 1)
        self.frame = 0
        self.image = self.image_coin[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.topleft = (x, y)
        self.tiempo_transcurrido = pygame.time.get_ticks()
        
    def do_animation(self,delta_ms):
        tiempo_actual = pygame.time.get_ticks()
        self.tiempo_transcurrido += delta_ms
        if tiempo_actual - self.tiempo_transcurrido > 100:
            self.tiempo_transcurrido = 0
            self.frame = (self.frame + 1) % len(self.image_coin)
            self.image = self.image_coin[self.frame]
            self.tiempo_transcurrido = tiempo_actual

    def update(self, delta_ms):
        self.do_animation(delta_ms)

        
    
        

        