import random
import pygame
import os
from time import gmtime, strftime

# Window properties
os.environ['SDL_VIDEO_CENTERED'] = '1'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

FPS = 60

# Key Variables

absfactor = 1           # number by which the random energy absorption factor is multiplied
reprochance = 0.002     # reproduction chance
reproage = 20           # reproduction min age
senescence = 150        # senescence age (maximum age)
reproen = 3000          # minimum reproduction energy
deathchance = 0.005     # chance of random death (1.0 = always)
popcap = 300            # population cap

# Classes

class plant(object):

    def __init__(self, plantid, alive, energy,
                 xpos, ypos, move_speed,
                 red, green, blue, age, absorptionfactor):
        self.plantid = plantid
        self.alive = 0
        self.energy = 0
        self.xpos = 0
        self.ypos = 0
        self.move_speed = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.age = 0
        self.absorptionfactor = 0

    def __call__(self):
        return self

    def isalive(self):
        if self.alive == 1:
            print('Plant # %s is alive' %(self.plantid))
        else:
            print('Plant # %s is dead' %(self.plantid))

    def kill(self):
        self.alive = 0

    def resurrect(self):
        self.alive = 1
		
    def currentpos(self):
        print('Plant # %s, Position (x, y) = (%s,%s)'
              %(self.plantid, self.xpos, self.ypos))

    def stats(self):
        if self.alive == 1:
            print('Living Plant # %s, Position (x, y) = (%s,%s), Energy = %s, Age = %s'
                  %(self.plantid, self.xpos, self.ypos, self.energy, self.age))
        else:
            print('Dead Plant # %s, Position (x, y) = (%s,%s), Energy = %s, Age = %s'
                  %(self.plantid, self.xpos, self.ypos, self.energy, self.age))
		
    def add_energy(self, energyinput):
        self.energy = self.energy + energyinput

    def remove_energy(self, energydrain):
        self.energy = self.energy - energydrain

    def setpos(self, x, y):
        self.xpos = x
        self.ypos = y

    def move_x(self, x):
        self.xpos = self.xpos + x
        self.xpos = max(0, min(self.xpos, SCREEN_WIDTH))

    def move_y(self, y):
        self.ypos = self.ypos + y
        self.ypos = max(0, min(self.ypos, SCREEN_HEIGHT))

    def setcolour(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def agetick(self):
        a = self.age
        self.age = (a + 1)

    def radius(self):
        rad = int(round((self.energy / 100)))
        return rad

# Functions

def currtime():
    ct = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('Simulation started: %s' %(ct))

def debug():
    [plant.stats() for plant in plants]

def feed():
    plant.energy = plant.energy + (1 * plant.absorptionfactor)

def reproduce():
    # Define generation colour
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    for plant in plants:
        # reproduction condition
        if (plant.age > reproage) and (plant.energy > reproen) and ((random.random() <= reprochance)):
            # get new plant id by finding the id of the last plant
            np_plantid = len(plants)
            # add 1 to global total plants counter
            global tot_plants
            tot_plants = (tot_plants + 1)
            # initiate new plant instance
            np = plant.__class__(np_plantid, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            # generate new plant (np) characteristics from parent
            np.plantid = np_plantid
            np.alive = 1
            en = random.randint(200, 800)
            np.energy = en
            xdelta = random.choice([-20, 20])
            np.xpos = plant.xpos + int(xdelta)
            np.xpos = max(0, min(np.xpos, SCREEN_WIDTH))
            ydelta = random.choice([-20, 20])
            np.ypos = plant.ypos + int(ydelta)
            np.ypos = max(0, min(np.ypos, SCREEN_HEIGHT))
            np.move_speed = plant.move_speed
            np.red = red
            np.green = green
            np.blue = blue
            np.absorptionfactor = absfactor * random.randint(1, 100)
            # remove some energy from the parent
            plant.remove_energy(en)
            # add new plant (np) to plants and total
            plants.append(np)

        else:
            continue

# Create plant number based on input and give them random positions

num_plants = input("Number of plants to spawn:")
num_plants = int(num_plants)
tot_plants = num_plants
plants = [plant(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) for i in range(0, num_plants)]

for plant in plants:
    plant.alive = 1
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    plant.setpos(x, y)
    plant.move_speed = 0
    plant.energy = random.randint(0, 5000)
    plant.setcolour(0, 255, 0)
    plant.absorptionfactor = absfactor * random.randint(1, 100)

# Pygame module start, screen defined and clock active
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
cycle = 0 
font = pygame.font.SysFont(None, 25)
RUNNING, PAUSE, END = 0, 1, 2
state = RUNNING
pause_text = pygame.font.SysFont(
                'Consolas', 32).render(
                'Pause, press E for debug', True, pygame.color.Color('White'))

# Print simstart time
currtime()

# Gameloop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if state == RUNNING:
                    state = PAUSE
                elif state == PAUSE:
                    state = RUNNING
            if event.key == pygame.K_SPACE: state = END

    else:
        # RUNNING LOOP
        if state == RUNNING:

            # Increase cycle number
            cycle = cycle + 1
            
            # count number of plants in list
            listsize = int(len(plants))

            # setup current and deleted plants lists
            deadplants = []            

            # kill plants with low energy, add plants to list depending on if alive or dead
            for plant in plants:
                if plant.alive == 1:
                    plant.agetick() #increase plant age

                # find plant position
                x = plant.xpos
                y = plant.ypos

                # energy change
                feed()

                # render
                red = plant.red
                green = plant.green
                blue = plant.blue
                r = plant.radius()
                pygame.draw.circle(screen, (red, green, blue), (x, y), r)

                # reproduction - now working!
                reproduce()

                # kill old plants, low energy plants
                if plant.age > senescence:
                    plant.kill()
                if plant.energy <= 100:  # 100 as radius of plant is energy/100 - so that plant is visible
                    plant.kill()

                # random chance of death
                if random.random() <= deathchance:
                    plant.kill()

                # population cap
                if len(plants) > popcap:
                    plant.kill()

                if plant.alive == 0:
                    deadplants.append(plant)
                    plants.remove(plant)

            # set num_plants to be the number of plants in alive list
            num_aliveplants = len(plants)
            num_deadplants = len(deadplants)
            
            # keypressing
            pressed = pygame.key.get_pressed()

            # Show cycle number
            strcycle = str(cycle) # convert cycle to a string so can make text
            text = font.render(("Cycle: %s" % strcycle), True, (255, 0, 0)) # set text and colour
            screen.blit(text, (5, 5)) # writes the text render to the screen

            # Show number of plants
            strnum_aliveplants = str(num_aliveplants)
            strnum_totplants = str(tot_plants)
            text = font.render(("Alive Plants: %s" % strnum_aliveplants), True, (255, 0, 0))
            screen.blit(text, (5, 25))
            text = font.render(("Total Plants: %s" % strnum_totplants), True, (255, 0, 0))
            screen.blit(text, (5, 45))
            #clear number of plants for next loop
            num_deadplants = 0
            num_aliveplants = 0
            
            # press p to print stats
            if pressed[pygame.K_p]:
                print('Plants list:')
                [plant.stats() for plant in plants]
                print('xxxxx')
            elif pressed[pygame.K_d]:
                print('Dead list:')
                [plant.stats() for plant in deadplants]
                print('xxxxx')


        # PAUSE LOOP
        elif state == PAUSE:
            screen.blit(pause_text, (100, 100))
            if event.key == pygame.K_e:
                debug()
            
        # END
        elif state == END:
            break

        # necessary to provide screen updates                    
        pygame.display.flip()

        # fps clock
        clock.tick(FPS)

        # clear screen (each tick)
        screen.fill((0, 0, 0))             

        continue
    break

pygame.quit()

# Ideas - get plants to combine by adding energy?
# Plants can still render over each other!
# Set better reproduction conditions
        

