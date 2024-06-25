import neat.population
import pygame
import neat
import pickle
import os
import random

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 30)

#Screen resolution
WIN_WIDTH = 600
WIN_HEIGHT = 800

GEN = 0  #Generation counter

# Objects Sprites
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('img/bird1.png')), pygame.transform.scale2x(pygame.image.load('img/bird2.png')), pygame.transform.scale2x(pygame.image.load('img/bird3.png'))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('img/pipe.png'))
BG_IMG = pygame.transform.scale2x(pygame.image.load('img/bg.png'))
GROUND_IMG = pygame.transform.scale2x(pygame.image.load('img/ground.png'))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 #time between each frame of animation

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    #Moves the bird on y and rotate it as it is going up or down
    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y += d

        #if the bird is going up rotate it upward
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        #else make it look downward
        else:
            #makes the bird dont rotate more than 90 degrees
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    #bird render
    def draw(self, win):
        self.img_count += 1 #animation frame counter

        #switches between the animation frames
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #if the bird is rotated for less than -80 stops the animation on frame 2
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        #draws the rotated bird properly
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rect) #render the bird

    #gets the bird mask for hitbox use
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200 #y gap between pipes
    VEL = 5 #y velocity

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #flips the pipe sprite on y axis
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False 
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    #checks if the bird and the pipe collided
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        #True if the bird and the pipe overlap
        t_point = bird_mask.overlap(top_mask, top_offset) 
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False
    
class Ground:
    VEL = 5
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self):
        #move the ground left
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #if the platform1 leaves the screen move it to the far right of the screen
        if self.x1 + self.WIDTH == 0:
            self.x1 = self.x2 + self.WIDTH

        #if the platform2 leaves the screen move it to the far right of the screen
        if self.x2 + self.WIDTH == 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, ground, score, GEN):
    win.blit(pygame.transform.scale(BG_IMG, (600,800)), (0,0))

    #draw a pipe for each element on pipes
    for pipe in pipes:
        pipe.draw(win)

    #render the texts
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render("Gen: " + str(GEN), 1, (255,255,255))
    win.blit(text, (10, 10))

    #draw a bird for each genome on birds
    ground.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()#updates the screem

def main(genomes, config, training = True):
    global GEN
    GEN += 1

    nets = []
    ge = []
    birds = []    

    #create a bird and network for each genome
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    score = 0
    ground = Ground(730)
    pipes = [Pipe(650)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)

        #quits the simulation if X button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0

        #runs if there is at least one bird
        if len(birds) > 0:
            #checks if the bird has passed the first pipe
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        #for each existent bird
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 #rewards the bird for staying alive

            #sets the output for the network as:
            # the bird y position, the bird distance to the top pipe and the bird distance to the bottom pipe.
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom) ))

            #if the bird y is greater than 0.5, jump
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = [] #pipes to be removed from scene
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1 #punish the bird for hitting a pipe
                    
                    #deletes the bird data
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
                #execute when the bird passes a pipe for the first time
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            #if the pipe leaves the screen append the pipe to remove list
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        #creates a new pipe and rewards the bird for passing a pipe
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(650))
        
        #deletes all passed pipes
        for r in rem:
            pipes.remove(r)

        #deletes bird and bird data if it leave the screen on y axis or hit the ground
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        ground.move()
        draw_window(win, birds, pipes, ground, score, GEN)

        #If a bird gets past 10 pipes it probably got the best a 
        #model could get in the game so it will probably gor forever
        #as so, breaks the loop if birds score get past 10
        if training:
            if score > 5:
                break

#Runs the game and trains a model
def run(config_path):
    #NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #gets the best running bird
    winner = p.run(main, 10)

    #Saves the model as the best running bird
    with open("winner.p", "wb") as f:
        pickle.dump(winner, f)
        f.close()

#Used if you want to replay a past model
def replay_genome(config_path, genome_path="winner.p"):
    # Load NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)
    
    # Unpickle genome
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded game into required data structure
    genomes = [(1, genome)]

    # Run game with loaded genomes
    main(genomes, config, training = False)


if __name__ == "__main__":
    #if false it will run replay_games() and use the prefered model
    #if true will run run() and train a new model, overwriting the "winner.p" model
    train = True

    #gets NEAT configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join("config-feedForward.txt")

    #checks if you want to train a new model or use a past one
    if train:
        run(config_path)
    else:
        replay_genome(config_path)