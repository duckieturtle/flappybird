# Example file showing a basic pygame "game loop"
import pygame
import random

pygame.init()

# configuration
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PIPE_SPACING= 200
BIRD_RADIUS = 20

YOU_LOSE_IMAGE = pygame.image.load("gameover.png")
SCORE_FONT = pygame.font.SysFont("Arial", 24)

PLAY_AGAIN_FONT = pygame.font.SysFont("Arial", 45)
PLAY_AGAIN_IMAGE = PLAY_AGAIN_FONT.render("Play Again", False, "orange")

FLAPPY_BIRD_IMAGE_DOWN = pygame.image.load("yellowbird-downflap.png")
FLAPPY_BIRD_IMAGE_UP = pygame.image.load("yellowbird-upflap.png")
FLAPPY_BIRD_IMAGE_MID = pygame.image.load("yellowbird-midflap.png")

PIPE_IMAGE = pygame.image.load("pipe-green.png")
PIPE_IMAGE_FLIPPED = pygame.transform.flip(PIPE_IMAGE, False, True)

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
score = 0

# functions
def draw_play_again_button():
    pygame.draw.rect(screen, "white", (
        SCREEN_WIDTH/2 - PLAY_AGAIN_IMAGE.get_width()/2 - 10,
        SCREEN_HEIGHT/2 + PLAY_AGAIN_IMAGE.get_height()/2 - 10,
        PLAY_AGAIN_IMAGE.get_width() + 20,
        PLAY_AGAIN_IMAGE.get_height() + 20
    ))

    screen.blit(PLAY_AGAIN_IMAGE, (
        SCREEN_WIDTH/2 - PLAY_AGAIN_IMAGE.get_width()/2,
        SCREEN_HEIGHT/2 + PLAY_AGAIN_IMAGE.get_height()/2
    ))

# classes
class Bird:
    def __init__(self):
        self.y = SCREEN_HEIGHT / 2
        self.score = 0
        self.velocity = 0
        self.died = False
        self.frames_jumping = 0
    
    def die(self):
        self.died = True
    
    def jump(self):
        self.velocity = -5
        self.frames_jumping = 10
    
    def draw(self):
        # pygame.draw.circle(screen, "yellow", (180, self.y), BIRD_RADIUS)
        if self.frames_jumping > 5:
            bird_image = FLAPPY_BIRD_IMAGE_DOWN
            self.frames_jumping -= 1
        elif self.frames_jumping > 0:
            bird_image = FLAPPY_BIRD_IMAGE_MID
            self.frames_jumping -= 1
        else:
            bird_image = FLAPPY_BIRD_IMAGE_UP

        screen.blit(bird_image, (180 - bird_image.get_width()/2, self.y - bird_image.get_height()/2))
 
    def movement(self):
        self.velocity += 0.25
        self.y += self.velocity

class Pipe:
    def __init__(self, x_coordinate):
        self.x = x_coordinate
        self.y = random.randint(SCREEN_HEIGHT - 25 - 462 - PIPE_SPACING / 2, 462)

    def move(self):
        global score
        self.x -= 3
        if self.x <= -75:
            self.x = 1425
            score = score + 1
            self.y = random.randint(SCREEN_HEIGHT - 25 - 462 - PIPE_SPACING / 2, 462)

    def draw(self):
        # pygame.draw.rect(screen, "green", (self.x, self.y + PIPE_SPACING / 2, 75, SCREEN_HEIGHT-self.y-PIPE_SPACING/2))
        # pygame.draw.rect(screen, "green", (self.x, 0, 75, self.y - PIPE_SPACING / 2))
        screen.blit(PIPE_IMAGE_FLIPPED, (self.x, (self.y - PIPE_SPACING / 2) - 462))
        screen.blit(PIPE_IMAGE, (self.x, self.y + PIPE_SPACING / 2))
    
    def collide_with_bird(self, the_bird):
        # bottom pipe
        if (
            180 + BIRD_RADIUS > self.x and
            180 - BIRD_RADIUS < self.x + 75 and
            the_bird.y + BIRD_RADIUS > self.y + PIPE_SPACING / 2 and
            the_bird.y - BIRD_RADIUS < self.y + PIPE_SPACING / 2 + SCREEN_HEIGHT-self.y-PIPE_SPACING/2
        ):
            the_bird.die()
        # top pipe
        if (
            180 + BIRD_RADIUS > self.x and
            180 - BIRD_RADIUS < self.x + 75 and
            the_bird.y + BIRD_RADIUS > 0 and
            the_bird.y - BIRD_RADIUS < 0 + self.y - PIPE_SPACING / 2
        ):
            the_bird.die()

pipes = [Pipe(300), Pipe(550), Pipe(800), Pipe(1050), Pipe(1300), Pipe(1550)]
bird = Bird()
space_pressed = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bird.died == False:
            space_pressed = True
            bird.jump()
        if event.type == pygame.MOUSEBUTTONDOWN and bird.died == True:
            mouse_position = pygame.mouse.get_pos()
            if (
                mouse_position[0] > SCREEN_WIDTH/2 - PLAY_AGAIN_IMAGE.get_width()/2 - 10 and
                mouse_position[0] < SCREEN_WIDTH/2 - PLAY_AGAIN_IMAGE.get_width()/2 - 10 + PLAY_AGAIN_IMAGE.get_width() + 20 and
                mouse_position[1] > SCREEN_HEIGHT/2 + PLAY_AGAIN_IMAGE.get_height()/2 - 10 and
                mouse_position[1] < SCREEN_HEIGHT/2 + PLAY_AGAIN_IMAGE.get_height()/2 - 10 + PLAY_AGAIN_IMAGE.get_height() + 20
            ):
                pipes = [Pipe(300), Pipe(550), Pipe(800), Pipe(1050), Pipe(1300), Pipe(1550)]
                bird = Bird()
                space_pressed = False
                score = 0
 
    if space_pressed == True:
        bird.movement()        

    for pipe in pipes:
        if bird.died == False and space_pressed == True:
            pipe.move()
            pipe.collide_with_bird(bird)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#40A4FF")

    # too low, screen height - grass height - bird radius
    if bird.y > SCREEN_HEIGHT - 25 - BIRD_RADIUS:
        bird.y = SCREEN_HEIGHT - 25 - BIRD_RADIUS
        bird.velocity = 0
        bird.die()
    # too high, bird radius
    if bird.y < BIRD_RADIUS:
        bird.y = BIRD_RADIUS
        bird.velocity = 0
        bird.die()

    # DRAW YOUR GAME HERE

    # cloud
    pygame.draw.circle(screen, "white", (800, 300), 50)
    pygame.draw.circle(screen, "white", (845, 270), 50)
    pygame.draw.circle(screen, "white", (895, 300), 50)
    pygame.draw.rect(screen, "white", (800, 300, 95, 50))
    # bird and pipe
    bird.draw()
    for pipe in pipes:
        pipe.draw()
    pygame.draw.rect(screen, "#558022", (0, SCREEN_HEIGHT - 25, SCREEN_WIDTH, 25))

    if bird.died == True:
        draw_play_again_button()

    #score
    score_image = SCORE_FONT.render(str(score), False, "white")
    screen.blit(score_image, (10, 10))

    if bird.died:
        screen.blit(YOU_LOSE_IMAGE, (
            SCREEN_WIDTH/2 - YOU_LOSE_IMAGE.get_width()/2,
            SCREEN_HEIGHT/2 - YOU_LOSE_IMAGE.get_height()/2 - PLAY_AGAIN_IMAGE.get_height()
        ))
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()