import pygame
from auxiliar import Auxiliar
from constantes import *

class Bala():
    def __init__(self, x, y, direccion, speed_shoot) -> None:
        super().__init__()
        self.superficie = pygame.image.load(r"images\bullet\bala.jpg")
        self.superficie = pygame.transform.scale(self.superficie, (100, 60))
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = x
        self.rectangulo.centery = y
        self.direccion = direccion
        self.speed_shoot = speed_shoot
        
    def update(self):
        if self.direccion == DIRECTION_R:
            self.rectangulo.x += self.speed_shoot
        elif self.direccion == DIRECTION_L:
            self.rectangulo.x -= self.speed_shoot
            
    # def update(self, screen: pygame.surface.Surface):
    
    #     match self.direccion:
    #         case 'right':
    #             self.rectangulo.x += self.speed_shoot
    #             if self.rectangulo.x >= ANCHO_VENTANA:
    #                 self.kill()
    #         case 'left':
    #             self.rectangulo.x -= self.speed_shoot
    #             if self.rectangulo.x <= 0:
    #                 self.kill()
    #     self.draw(screen)
        
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.superficie, self.rectangulo)
        