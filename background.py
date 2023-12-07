import pygame
from constantes import *


class Background:
    def __init__(self, x, y,width, height,  path):

        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)


    def draw(self,screen):
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect) 
            
        screen.blit(self.image,self.rect)