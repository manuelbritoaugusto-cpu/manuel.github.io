import pygame
import random
from sys import exit

GAME_WIDTH = 750
GAME_HEIGHT = 250

class Block(pygame.Rect):
    def __init__(self, coordinates,size, image ):
        pygame.Rect.__init__(self, coordinates, size)
        self.image = image
        self.velocity_x = 0 
        self.velocity_y = 0

#images
DINOSAUR = pygame.transform.scale(pygame.image.load("Wakfu_Bird.png"), (88, 94))
DEAD_DINOSAUR = pygame.transform.scale(pygame.image.load("Wakfu_Bird_Dead.png"), (88, 94))
Object1 =  pygame.transform.scale(pygame.image.load("Tree.png"), (34, 70))
Object2 =  pygame.transform.scale(pygame.image.load("2 tree.png"), (69, 70))
Object3 = pygame.transform.scale(pygame.image.load("3 tree.png"), (102, 70))
OBJECT_IMAGES = [Object1, Object2, Object3]


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Wakfu dino Game")
clock = pygame.time.Clock()
GAME_FONT = pygame.font.SysFont("Courier", 20)

VELOCITY_X = -8 
VELOCITY_Y = -10
GRAVITY= 0.4


dino = Block((50, GAME_HEIGHT - DINOSAUR.get_height()), DINOSAUR.get_size(), DINOSAUR)
object_list = []
last_place_object_time = 0
game_over = False
score = 0
high_score = 0  


def place_object():
    random_object_image = random.choice(OBJECT_IMAGES)
    random_object = Block((GAME_WIDTH, GAME_HEIGHT - random_object_image.get_height()),
                          random_object_image.get_size(),
                          random_object_image)
    random_object.velocity_x = VELOCITY_X
    object_list.append(random_object)


def move():
    global object_list, game_over, score, high_score
    score += 1

    dino.velocity_y += GRAVITY
    dino.y += dino.velocity_y 
    if dino.y >= GAME_HEIGHT - dino.height:
        dino.y = GAME_HEIGHT - dino.height

    for object in object_list:
        object.x += object.velocity_x
        if dino.colliderect(object):
            game_over = True
            dino.image = DEAD_DINOSAUR
            if score > high_score:      
                high_score = score
    
    object_list = [object for object in object_list if object.x + object.width > 0]
#Player
def draw():
    window.fill((0, 100, 0))
    window.blit(dino.image, dino)

    for object in object_list:
        window.blit(object.image, object)

#points
    score_text = GAME_FONT.render(str(score // 5), True, (255, 255, 255))
    window.blit(score_text, (20, 20))
#High Score
    high_text = GAME_FONT.render("High Score:" + str(high_score // 5), True, (255, 255, 255))
    window.blit(high_text, (20, 45))

#loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    object_list.clear()
                    game_over = False
                    score = 0
                    dino.y = GAME_HEIGHT - dino.height
                    dino.velocity_y = 0
                    dino.image = DINOSAUR

                elif dino.y >= GAME_HEIGHT - dino.height:
                    dino.velocity_y = VELOCITY_Y
#how the objects are placed  
    now = pygame.time.get_ticks()
    if now - last_place_object_time > 1000:
        place_object()
        last_place_object_time = now

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)
    else:
        draw()                
        pygame.display.update()
        clock.tick(60)