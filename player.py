import pygame
from auxiliar import Auxiliar
from constantes import *
from bala import Bala
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height,p_scale=1,interval_time_jump=100) -> None:
        super().__init__()
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Idle ({0}).png",1,10,flip=False,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Idle ({0}).png",1,10,flip=True,scale=p_scale)
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Jump ({0}).png",1,10,flip=False,scale=p_scale)
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Jump ({0}).png",1,10,flip=True,scale=p_scale)
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Run ({0}).png",1,8,flip=False,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Run ({0}).png",1,8,flip=True,scale=p_scale)
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Shoot ({0}).png",1,3,flip=False,scale=p_scale,repeat_frame=2)
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Shoot ({0}).png",1,3,flip=True,scale=p_scale,repeat_frame=2)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Melee ({0}).png",1,7,flip=False,scale=p_scale,repeat_frame=1)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/cowgirl/Melee ({0}).png",1,7,flip=True,scale=p_scale,repeat_frame=1)

        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = DIRECTION_R
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H
    
        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False
        
        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
        self.is_looking_right = True
        
        self.lista_balas = pygame.sprite.Group()
        
    
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.move_x = move_x
        self.animation = animation_list
        self.is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        self.move_y = -self.jump_power
        self.move_x = self.speed_run if self.is_looking_right else -self.speed_run
        self.animation = self.jump_r if self.is_looking_right else self.jump_l
        self.initial_frame = 0
        self.is_jumping = True
    
    
    def walk(self,direction):
        if(self.is_jump == False and self.is_fall == False):
            if(self.direction != direction or (self.animation != self.walk_r and self.animation != self.walk_l)):
                self.frame = 0
                self.direction = direction
                if(direction == DIRECTION_R):
                    
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                    self.__set_x_animations_preset(self.speed_walk, self.walk_r, look_r=True)
                else:
                    
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    self.__set_x_animations_preset(-self.speed_walk, self.walk_l, look_r=False)
                    
    def shoot(self,on_off = True):
        if on_off:
            print("Método shoot llamado.")
            if self.is_shoot and not self.is_jump and not self.is_fall:
                if self.animation != self.shoot_r and self.animation != self.shoot_l:
                    self.frame = 0
                    self.is_shoot = True
                    if self.direction == DIRECTION_R:
                        self.animation = self.shoot_r
                        self.create_bullet(DIRECTION_R)
                    else:
                        self.animation = self.shoot_l
                        self.create_bullet(DIRECTION_L)
    
    def create_bullet(self, direction):
        bala = Bullet(self, self.rect.centerx, self.rect.centery,
                        self.rect.centerx, self.rect.centery,  # x_end, y_end
                        10,
                        "images/bullet/bala.jpg",
                        10, 10,
                        )
        self.lista_balas.add(bala)
    def lanzar_proyectil(self):
        x = None
        margen = 47
        
        y = self.rect.centery + 10
        if self.direction == DIRECTION_R or self.animation == self.stay_r:
            x = self.rect.right - margen
        elif self.direction == DIRECTION_L:
            x = self.rect.left - 100 + margen
            
        if x is not None:
            self.lista_balas.append(Bala(x, y, self.direction, speed_shoot=10))
            
    def actualizar_proyectil(self, pantalla):
        i = 0
        while i < len(self.lista_balas):
            p = self.lista_balas[i]
            pantalla.blit(p.superficie, p.rectangulo)
            p.update()
            if p.rectangulo.centerx < 0 or p.rectangulo.centerx > pantalla.get_width():
                self.lista_balas.pop(i)
                i -= 1
            i += 1
                
    # def disparo(self, shooting = True):
    #     flag_disparo = True
    #     self.is_shoot = shooting
    #     if(shooting == True and flag_disparo) 
                    
    def receive_shoot(self):
        self.lives -= 1

    def knife(self,on_off = True):
        self.is_knife = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):
            if(self.animation != self.knife_r and self.animation != self.knife_l):
                self.frame = 0
                if(self.direction == DIRECTION_R):
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l      

    def jump(self,on_off = True):
        if(on_off and self.is_jump == False and self.is_fall == False):
            self.y_start_jump = self.rect.y
            if(self.direction == DIRECTION_R):
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_r
            else:
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_l
            self.frame = 0
            self.is_jump = True
        if(on_off == False):
            self.is_jump = False
            self.stay()
            
    def stay(self):
        if(self.is_knife or self.is_shoot):
            return

        if(self.animation != self.stay_r and self.animation != self.stay_l):
            if(self.direction == DIRECTION_R):
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def change_x(self,delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if(abs(self.y_start_jump - self.rect.y) > self.jump_height and self.is_jump):
                self.move_y = 0
          
            self.change_x(self.move_x)
            self.change_y(self.move_y)

            if(not self.is_on_plataform(plataform_list)):
                if(self.move_y == 0):
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                if (self.is_jump): 
                    self.jump(False)
                self.is_fall = False            

    def is_on_plataform(self,plataform_list):
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True     
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno                 

    def do_animation(self,delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            if(self.frame < len(self.animation) - 1):
                self.frame += 1 
                #print(self.frame)
            else: 
                self.frame = 0
 
    def update(self,delta_ms,plataform_list, keys, screen):
        self.events(delta_ms, keys)
        self.actualizar_proyectil(screen)
        self.do_movement(delta_ms,plataform_list)
        self.do_animation(delta_ms)
        
    
    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        

    def events(self,delta_ms,keys):
        self.tiempo_transcurrido += delta_ms
        tiempo_ultimo_disparo = 0


        if(keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]):
            self.walk(DIRECTION_L)

        if(not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
            self.walk(DIRECTION_R)

        if(not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]):
            self.stay()
        if(keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]):
            self.stay()  

        if(keys[pygame.K_SPACE]):
            if((self.tiempo_transcurrido - self.tiempo_last_jump) > self.interval_time_jump):
                self.jump(True)
                self.tiempo_last_jump = self.tiempo_transcurrido

        if(not keys[pygame.K_a]):
            self.shoot(False)  

        if(not keys[pygame.K_a]):
            self.knife(False)  

        if(keys[pygame.K_s] and not keys[pygame.K_a]) and self.is_shoot:
            # self.tiempo_transcurrido = pygame.time.get_ticks()
            # if self.tiempo_transcurrido - tiempo_ultimo_disparo >= 1000: 
            self.shoot()   
                # self.lanzar_proyectil()
                # tiempo_ultimo_disparo = self.tiempo_transcurrido
        if(keys[pygame.K_a] and not keys[pygame.K_s]):
            self.knife()