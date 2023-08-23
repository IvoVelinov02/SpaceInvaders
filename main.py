import  pygame, sys  
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
 
class Game:
    def __init__(self):  
        player_sprite = Player((screen_width / 2 , screen_height),screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.survived = False
        self.lives = 3
        self.live_surd = pygame.image.load('pictures/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surd.get_size()[0] * 2 + 7.5)
        self.score = 0
        self.font = pygame.font.Font('TTC/MarkerFelt.ttc', 45)
        self.alien_speed_multiplier = 1.5 
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount)  for num in range(self.obstacle_amount)]
        self.obstaclesMulti(*self.obstacle_x_positions, startXcoordinates = screen_width / 15, startYcoordinates = 480)
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group( )
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(455,935)
        self.backgrounds = [
            pygame.image.load("background/invaders.jpg"),
            pygame.image.load("background/4632ed00-ca92-11ea-971d-78aec0b072fa.png")
        ]
        self.background_y = 0  
        self.background_speed = 1  

        music = pygame.mixer.Sound('sound/Dream Theater - The Alien (Official Video).mp3')
        music.set_volume(0.2)
        music.play(loops= - 1) 
        self.gunSound = pygame.mixer.Sound('sound/Sci-Fi Laser Machine Gun Sound Effects.mp3')
        self.gunSound.set_volume(0.1)
        self.boomSound = pygame.mixer.Sound('sound/Small Bomb Explosion Sound Effect.mp3')
        self.boomSound.set_volume(0.3)


    def create_obstacle(self, startXcoordinates, startYcoordinates, x1):
        for  index_row, row in enumerate(self.shape):
            for index_col, col in enumerate(row):
                if col == 'x':
                    x =  startXcoordinates + index_col * self.block_size + x1
                    y = startYcoordinates +  index_row * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def obstaclesMulti(self, *offset, startXcoordinates, startYcoordinates):
        for x1 in offset: 
            self.create_obstacle(startXcoordinates,startYcoordinates, x1)

    def alien_setup(self,rows,cols, x_distance = 60, y_distance = 48, x_offset = 70 , y_offset = 100):
        for row_index in range(rows):  
            for col_index in range(cols):  
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien('red', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('yellow', x, y)  
                self.aliens.add(alien_sprite)
      
      

    def alien_positiom_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6,screen_height )
            self.alien_lasers.add(laser_sprite)
            self.gunSound.play()

    def alien_extra_timer(self): 
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']), screen_width))
            self.extra_spawn_time = randint(400,800)
    

    def impactTest(self):    
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                
                if pygame.sprite.spritecollide(laser,self.aliens, True):
                    self.score += 500   
                    laser.kill()
         
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                     for alien in aliens_hit:
                         self.score += alien.value     
                     laser.kill()
                     self.boomSound.play()


        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
                
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                         
        if self.aliens: 
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
                    else:
                        
                        self.player.sprite.rect.midbottom = (screen_width // 2, screen_height - 10)
                        pygame.time.wait(1000)


    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.live_surd.get_size()[0] + 8)
            screen.blit(self.live_surd,(x,8 ))

    def display_score(self):
       score_surf = self.font.render(f'score: {self.score}', False, 'darkred') 
       score_rect = score_surf.get_rect(topleft = (235   ,0))
       screen.blit(score_surf, score_rect)
        
    def start(self):
        self.background_y += self.background_speed
        if self.background_y >= screen_height:
            self.background_y = 0

        for background in self.backgrounds:
            screen.blit(background, (0, self.background_y))
            screen.blit(background, (0, self.background_y - screen_height))

        if self.survived: 
            self.player.sprite.speed += 5


        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_positiom_checker()
        self.alien_lasers.update()
        self.alien_extra_timer()
        self.extra.update()  
        self.impactTest()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen) 
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()   
        
        if self.survived:
            self.player.sprite.speed *= self.alien_speed_multiplier
   
        pygame.display.flip()
        clock.tick(60)

        
if __name__ == '__main__':     
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    visitorGun = pygame.USEREVENT + 1
    pygame.time.set_timer(visitorGun, 800)

    while True:
        for  event  in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == visitorGun:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.start()
      
        pygame.display.flip()
        clock.tick(60)