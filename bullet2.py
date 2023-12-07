import pygame
class Projectile(object):
    def __init__(self, x, y, radio, color, facing, velocidad) -> None:
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.facing = facing
        self.velocidad = 8 * facing
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radio)