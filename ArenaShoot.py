# Name: Zacchary Dempsey-Plante
# Date started: Jan. 15, 2016
# Date finished: Jan. 28, 2016
# Description: A driving arena shooter.

import pygame, sys, os, math, random, datetime
from pygame.locals import *
os.environ['SDL_VIDEODRIVER'] = 'windib'

#allSprites = pygame.sprite.Group()
backgroundSprites = pygame.sprite.LayeredUpdates()
allSprites = pygame.sprite.LayeredUpdates()
uiSprites = pygame.sprite.LayeredUpdates()

###########################
## Sprite class code - don't touch
###########################
class Sprite(pygame.sprite.Sprite):
    # What has to be passed when you create a sprite.
    #   image_file: The filename of the image.
    #   name: The name you want to call the Sprite for id purposes.
    #   lacation: The (x,y) initial location of where to draw the image.
    def __init__(self, image_file, name,  location):
        pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image0 = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.lastX = self.rect.x # The x from the last frame.
        self.lastY = self.rect.y # The y from the last frame.
        self.rect.left, self.rect.top = location
        self.xSpeed = 10 # The default xSpeed
        self.ySpeed = 10 # The default ySpeed
        self.name = name
        self.speed = 10
        self.direction = 0
        self.lastDirection = self.direction
        self.done = False
        self.doneTime = 0
        self.doneTimer = 0
        self.removeWhenOffScreen = True
        self.movingTime = 0
        self.nextMove = random.random() * -1000
        self.useMovingTime = False
        self.storedValue1 = 0
        self.storedValue2 = 0
        self.storedValue3 = 0
        allSprites.add(self)

    # Gets rid of the sprite after "time" ticks.
    def goodbye(self, time):
        if(self.done==False):
            self.done = True
            self.doneTime = time
            self.doneTimer = 0

    # Moves the sprite in the direction it's facing at the current speed it's set for.
    def update(self):

        # Update the location using the x and y speeds.
        self.rect.x = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed

        if((self.rect.x > width or self.rect.x + self.rect.width < 0 or self.rect.y > height or self.rect.y + self.rect.height < 0) and self.removeWhenOffScreen == True):        
           self.kill()
           #print(self.name + " is gone")

        # See if the sprite has been told to die.
        if(self.done==True):
            self.doneTimer=self.doneTimer+1
            if(self.doneTimer >= self.doneTime):
                # Remove the sprite.
                self.kill()

        if self.useMovingTime == True:
            self.movingTime -= (pygame.time.get_ticks() - lastFrameTime)
            if self.movingTime < 0:
                self.setSpeed(0)
                #print(self.movingTime)

    # Sets the x position of the Sprite.
    def setX(self, x):
        self.rect.x = x

    # Returns the current x location of the Sprite.
    def getX(self):
        return self.rect.x

    # Returns the x location of the Sprite from the last frame.
    def getLastX(self):
        return self.lastX

    def setLastPosition(self):
        self.setX(self.lastX)
        self.setY(self.lastY)
        self.setDirection(self.lastDirection)

    # Sets the y position of the Sprite.
    def setY(self, y):
        self.rect.y = y

    # Returns the current y location of the Sprite.
    def getY(self):
        return self.rect.y

    # Returns the y location of the Sprite from the last frame.
    def getLastY(self):
        return self.lastY

    # Records the x and y of the last frame.
    # Record the position before we start moving.
    def recordLast(self):
        self.lastX = self.rect.x
        self.lastY = self.rect.y
        self.lastDirection = self.direction

    # Sets the speed of the Sprite.
    def setSpeed(self, speed):
        self.speed = speed
        self.calcXYSpeeds()

    # Returns the speed of the Sprite.
    def getSpeed(self):
        return self.speed

    # Returns the current direction of the Sprite
    def getDirection(self):
        return self.direction

    # Sets the direction of the Sprite.
    def setDirection(self, direction):
        self.direction = direction
        self.calcXYSpeeds()

        # Store the current center so that we can use it to set the center of the new rotated image.
        oldCenterX = self.rect.centerx
        oldCenterY = self.rect.centery

        # Rotate the original image.
        self.image = pygame.transform.rotate(self.image0, -self.direction)

        # Update the sprites rect with the new width and height after the rotate.
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

        # Change the center of the new rotated image to be the same center as the old image
        self.rect.centerx = oldCenterX
        self.rect.centery = oldCenterY

    def turn(self, amount):
        self.direction = self.direction + amount
        self.calcXYSpeeds()

        # Store the current center so that we can use it to set the center of the new rotated image.
        oldCenterX = self.rect.centerx
        oldCenterY = self.rect.centery

        # Rotate the original image.
        self.image = pygame.transform.rotate(self.image0, -self.direction)

        # Update the sprites rect with the new width and height after the rotate.
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

        # Change the center of the new rotated image to be the same center as the old image
        self.rect.centerx = oldCenterX
        self.rect.centery = oldCenterY

    def setDirectionTowards(self, x, y):
        self.direction = math.degrees(math.atan2((self.rect.x - x), (self.rect.y - y)))
        self.direction = 270 - self.direction
        self.calcXYSpeeds()

        # Store the current center so that we can use it to set the center of the new rotated image.
        oldCenterX = self.rect.centerx
        oldCenterY = self.rect.centery

        # Rotate the original image.
        self.image = pygame.transform.rotate(self.image0, -self.direction)

        # Update the sprites rect with the new width and height after the rotate.
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

        # Change the center of the new rotated image to be the same center as the old image
        self.rect.centerx = oldCenterX
        self.rect.centery = oldCenterY

    # Calculate the x and y speeds based on the current angle.
    def calcXYSpeeds(self):
        angleRadians = math.radians(self.direction) # Convert the direction to radians.
        self.xSpeed= self.speed*math.cos(angleRadians)
        self.ySpeed = self.speed*math.sin(angleRadians)

    def setXSpeed(self, newXSpeed):
        self.xSpeed = newXSpeed
        self.direction = round(math.degrees(math.atan2(self.ySpeed,self.xSpeed)))

        if(self.direction<0):
            self.direction=self.direction+360

    def setYSpeed(self, newYSpeed):
        self.ySpeed = newYSpeed
        self.direction = round(math.degrees(math.atan2(self.ySpeed,self.xSpeed)))

        if(self.direction<0):
            self.direction=self.direction+360

    def getXSpeed(self):
        return self.xSpeed

    def getYSpeed(self):
        return self.ySpeed

    def isAtRightEdge(self):
        if(self.rect.x + self.rect.width > width):
            return True
        else:
            return False

    def isAtLeftEdge(self):
        if(self.rect.x < 0):
            return True
        else:
            return False

    def isAtBottomEdge(self):
        if(self.rect.y + self.rect.height > height):
            return True
        else:
            return False

    def isAtTopEdge(self):
        if(self.rect.y < 0):
            return True
        else:
            return False

    def isTouchingSprite(self, otherName, removeSprite):
        touchingSprite = None
        allCollided = pygame.sprite.spritecollide(self, allSprites, False)

        for touching in allCollided:
               if(touching.name == otherName):
                    touchingSprite = touching
                    #print("Hit " + touching.name)

        if(removeSprite==True):
            allSprites.remove(touchingSprite)

        return touchingSprite

    def isTouchingSpriteCircle(self, otherName, removeSprite):
        touchingSprite = None
        allCollided = pygame.sprite.spritecollide(self, allSprites, False, pygame.sprite.collide_circle)

        for touching in allCollided:
               if(touching.name == otherName):
                    touchingSprite = touching
                    #print("Hit " + touching.name)

        if(removeSprite==True):
            allSprites.remove(touchingSprite)

        return touchingSprite

def getListOf(spriteName):
    spriteList = []
    for sprite in allSprites:
        if(sprite.name == spriteName):
            spriteList.append(sprite)
    return spriteList

def damagePlayer(damage):
    global sPowerActive
    global currentHealth
    global damageQueue
    #if the shield is active, halve the damage to deal
    if sPowerActive == True:
        damage = int(damage / 2)
    currentHealth -= damage
    damageQueue.append(str(damage) + "," + str(pygame.time.get_ticks()))

def spawnPowerUp(powerUp):
    global screenOffset
    global edgesPadding
    powerUp.rect.x = (((width - powerUp.rect.width) - (edgesPadding * 2)) * random.random()) + (edgesPadding * 1) #I am aware * 1 is useless, but is allows for me to see only one is added
    powerUp.rect.y = ((((height - screenOffset) - powerUp.rect.height) - (edgesPadding * 2)) * random.random()) + (screenOffset + (edgesPadding * 1))
 



###########################
## End of Sprite class code - don't touch code above
###########################

pygame.init()

screen = pygame.display.set_mode((800, 640))

# Storing the width and height of the screen.
width = screen.get_width()
height = screen.get_height()
print ("The width is " + str(width))
print ("The height is " + str(height))

# Create a clock to keep track of time
clock = pygame.time.Clock()
lastFrameTime = 0

background = Sprite("ground.png","Ground",(0,40))
background.setSpeed(0)
allSprites.remove(background)
backgroundSprites.add(background)

topBar = Sprite("topBackgroundColour.png","TopBar",(0,0))
topBar.image = pygame.transform.scale(topBar.image, (width,40))
allSprites.remove(topBar)
uiSprites.add(topBar)

healthBarPos = (600,7)
healthBarSize = (125,25)

healthBackground = Sprite("healthbarGray.png","HealthBackground",healthBarPos)
healthBackground.image = pygame.transform.scale(healthBackground.image, healthBarSize)
allSprites.remove(healthBackground)
uiSprites.add(healthBackground)

healthRed = Sprite("healthbarRed.png","HealthBackground",healthBarPos)
healthRed.image = pygame.transform.scale(healthRed.image, healthBarSize)
allSprites.remove(healthRed)
uiSprites.add(healthRed)

healthGreen = Sprite("healthbarGreen.png","HealthBackground",healthBarPos)
healthGreen.image = pygame.transform.scale(healthGreen.image, healthBarSize)
allSprites.remove(healthGreen)
uiSprites.add(healthGreen)

playerScale = (80,40)

playerBase = Sprite("playerBase.png","PlayerBase",(width / 2 - (playerScale[0] / 2),height / 2 - (playerScale[1] / 2)))
playerBase.image = pygame.transform.scale(playerBase.image, playerScale)
playerBase.image0 = pygame.transform.scale(playerBase.image0, playerScale)
#playerBase.rect = playerScale
playerBase.rect.width = playerScale[0]
playerBase.rect.height = playerScale[1]
playerBase.colliderect = playerBase.rect
playerBase.setDirection(270)
playerBase.setSpeed(0)

playerBlaster = Sprite("playerBlasterTEST.png","PlayerBlaster",(width/2,height-60))
playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)
playerBlaster.colliderect = playerBlaster.rect
playerBlaster.setDirection(270)
playerBlaster.setSpeed(0)

running = 1

# Setup the font use for drawing to the screen.
font=pygame.font.Font(None,50)
fontMed=pygame.font.Font(None,65)
fontBig=pygame.font.Font(None,100)

#miscellaneous variables
screenOffset = 40
edgesPadding = 30

#enemy variables
#enemy1 variables
sinceEnemy1Spawn = 0
enemy1SpawnBaseTime = 1000
enemy1SpawnRandomTime = 1000
enemy1CurrentSpawnTime = enemy1SpawnBaseTime + (enemy1SpawnRandomTime * random.random())
lastEnemy1Shot = 0
lastEnemy1Move = 0
enemy1MoveTimer = 500
numEnemy1s = 0
enemy1Cap = 6
enemy1Scale = (30,30)
enemy1Speed = 5
enemy1Damage = 10
enemy1ScoreValue = 1

#enemy2 variables
sinceEnemy2Spawn = 0
enemy2SpawnBaseTime = 7000
enemy2SpawnRandomTime = 8000
enemy2CurrentSpawnTime = enemy2SpawnBaseTime + (enemy2SpawnRandomTime * random.random())
lastEnemy2Move = 0
enemy2MoveTimer = 500
numEnemy2s = 0
enemy2Cap = 1
enemy2Scale = (40,40)
enemy2Speed = 15
enemy2Damage = 2
enemy2DamageIncrement = 100
enemy2TrailColour = (98,255,194)
enemy2TrailCutoff = 1000
enemy2ScoreValue = 1

#enemy3 variables
sinceEnemy3Spawn = 0
enemy3SpawnBaseTime = 1000
enemy3SpawnRandomTime = 1000
enemy3CurrentSpawnTime = enemy3SpawnBaseTime + (enemy3SpawnRandomTime * random.random())
lastEnemy3Shot = 0
lastEnemy3Move = 0
enemy3MoveTimer = 300
numEnemy3s = 0
enemy3Cap = 2
enemy3Scale = (40,40)
enemy3Speed = 5
enemy3Damage = 5
enemy3ScoreValue = 2

#power-up variables
#laser
sinceLPowerUpSpawn = 0
lPowerExists = False
lPowerDuration = 15000
lPowerActive = False
lPowerActiveTime = 0
lPowerSpawnBaseTime = 10000
lPowerSpawnRandomTime = 20000
lPowerCurrentSpawnTime = lPowerSpawnBaseTime + (lPowerSpawnRandomTime * random.random())

#shield
sinceSPowerUpSpawn = 0
sPowerExists = False
sPowerDuration = 15000
sPowerActive = False
sPowerActiveTime = 0
sPowerSpawnBaseTime = 10000
sPowerSpawnRandomTime = 20000
sPowerCurrentSpawnTime = sPowerSpawnBaseTime + (sPowerSpawnRandomTime * random.random())

#healing
hPowerUpInterval = 30 #0 makes constant spawns
hPowerUpIntervalBoost = 5
nextHPowerUpSpawn = hPowerUpInterval
hPowerExists = False
hPowerDuration = 6000
hPowerActive = False
hPowerActiveTime = 0
hPowerUpNetHeal = 60
healIncrement = round(hPowerDuration / hPowerUpNetHeal)
lastHealTime = 0

#player variables
playerSpeed = 4
playerShotSpeed = 35
lastPlayerShot = 0
maxHealth = 100
currentHealth = maxHealth
damageQueue = []
healthBarDamageTime = 1000

currentScore = 0
scoreTextColour = (255,255,255)
score_text = font.render("Score: " + str(currentScore),1, scoreTextColour)
gameOver = False
savedHighscore = False
newScoreIndex = -1

highscoresFile = "Highscores.txt"

pygame.display.set_caption("Arena Shooter!")

while running:
    
    # Sets the frame rate to 30 frames/second.
    clock.tick(30)
    
    event = pygame.event.poll()
    
    if event.type == pygame.QUIT:
        running = 0

    pygame.event.pump() # Get the current state of events.
    key=pygame.key.get_pressed()  # Get a list of what keys are being pressed.

    # Color the whole screen with a solid color.
    screen.fill((255,255,255))

    #draw the backgrounds so they are drawn over every time
    backgroundSprites.draw(screen)

    #########################################
    # Add your code here.
    #########################################

    #check if the player has lost
    if currentHealth <= 0 and savedHighscore == False:
        playerBase.kill()
        playerBlaster.kill()
        gameOver = True
        print("Final Score: " + str(currentScore))

    if key[pygame.K_F2]: # Restart the game
        # Initialize all the sprites and variables

        allSprites.empty() # Remove all current Sprites.

        #reload the player
        playerBase = Sprite("playerBase.png","PlayerBase",(width/2,height-60))
        playerBase.image = pygame.transform.scale(playerBase.image, playerScale)
        playerBase.image0 = pygame.transform.scale(playerBase.image0, playerScale)
        playerBase.rect.width = playerScale[0]
        playerBase.rect.height = playerScale[1]
        playerBase.colliderect = playerBase.rect
        playerBase.setDirection(270)
        playerBase.setSpeed(0)

        playerBlaster = Sprite("playerBlasterTEST.png","PlayerBlaster",(width/2,height-60))
        playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
        playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)
        playerBlaster.colliderect = playerBlaster.rect
        playerBlaster.setDirection(270)
        playerBlaster.setSpeed(0)

        #set the values appropriately
        gameOver = False
        savedHighscore = False
        currentScore = 0
        currentHealth = maxHealth

        #set the spawn-tracking values back to what they should start as
        sinceEnemy1Spawn = 0
        lastEnemy1Shot = 0
        lastEnemy1Move = 0
        sinceEnemy2Spawn = 0
        lastEnemy2Move = 0
        sinceEnemy3Spawn = 0
        lastEnemy3Shot = 0
        lastEnemy3Move = 0
        sinceLPowerUpSpawn = 0
        sinceSPowerUpSpawn = 0

        lastPlayerShot = 0
        damageQueue = []

        numEnemy1s = 0
        numEnemy2s = 0
        numEnemy3s = 0

        #update the score currently displayed on-screen
        score_text=font.render("Score: " + str(currentScore),1, scoreTextColour)

    if gameOver == False:
    
        #enemies
        if numEnemy1s != enemy1Cap:
            sinceEnemy1Spawn += (pygame.time.get_ticks() - lastFrameTime)

        if numEnemy2s != enemy2Cap:
            sinceEnemy2Spawn += (pygame.time.get_ticks() - lastFrameTime)

        if numEnemy3s != enemy3Cap:
            sinceEnemy3Spawn += (pygame.time.get_ticks() - lastFrameTime)

        if lPowerExists == False:
            sinceLPowerUpSpawn += (pygame.time.get_ticks() - lastFrameTime)

        if sPowerExists == False:
            sinceSPowerUpSpawn += (pygame.time.get_ticks() - lastFrameTime)

        #enemy1s
        #spawn enemy1s
        if sinceEnemy1Spawn >= enemy1CurrentSpawnTime and numEnemy1s < enemy1Cap:
            enemy1CurrentSpawnTime = enemy1SpawnBaseTime + (enemy1SpawnRandomTime * random.random())
            sinceEnemy1Spawn = 0
            #implement random spawn positions, both vertical and horizontal
            if random.random() > 0.5:
                print("Spawned enemy1 horizontally!")
                numEnemy1s += 1
                enemy1 = Sprite("enemy1.png","Enemy1",(0,0))
                enemy1.image = pygame.transform.scale(enemy1.image, enemy1Scale)
                enemy1.image0 = pygame.transform.scale(enemy1.image0, enemy1Scale)
                enemy1.rect.width = enemy1Scale[0]
                enemy1.rect.height = enemy1Scale[1]
                enemy1.colliderect = enemy1.rect
                enemy1.useMovingTime = True
                #set the position
                enemy1.rect.x = (width - enemy1.rect.width) * random.random()
                #roughly half of the enemy1s spawn top and half on the bottom
                if random.random() > 0.5:
                    enemy1.rect.y = screenOffset
                    enemy1.setDirection(180)
                else:
                    enemy1.rect.y = height - enemy1.rect.height
                    enemy1.setDirection(0)
                #set the speed
                enemy1.setSpeed(0)
            else:
                print("Spawned enemy1 vertically!")
                numEnemy1s += 1
                enemy1 = Sprite("enemy1.png","Enemy1",(0,0))
                enemy1.image = pygame.transform.scale(enemy1.image, enemy1Scale)
                enemy1.image0 = pygame.transform.scale(enemy1.image0, enemy1Scale)
                enemy1.rect.width = enemy1Scale[0]
                enemy1.rect.height = enemy1Scale[1]
                enemy1.colliderect = enemy1.rect
                #set the position
                enemy1.rect.y = (height - enemy1.rect.height) * random.random()
                #roughly half of the enemy1s spawn left and half on the right
                if random.random() > 0.5:
                    enemy1.rect.x = 0
                    enemy1.setDirection(90)
                else:
                    enemy1.rect.x = width - enemy1.rect.width
                    enemy1.setDirection(270)
                #set the speed
                enemy1.setSpeed(0)

        #make the enemy1s shoot
        if pygame.time.get_ticks() - lastEnemy1Shot >= 1500 and numEnemy1s > 0:
            lastEnemy1Shot = pygame.time.get_ticks()
            enemy1s = getListOf("Enemy1")
            shooterIndex = round(random.random() * len(enemy1s))
            if shooterIndex == len(enemy1s):
                shooterIndex -= 1
            print("Enemy1, shoot!")
            #spawn the laser to be shot and set the position
            enemyLaser = Sprite("laser2.png","EnemyLaser",(enemy1s[shooterIndex].rect.centerx,enemy1s[shooterIndex].rect.centery))
            enemyLaser.image = pygame.transform.scale(enemyLaser.image, (30,30))
            enemyLaser.image0 = pygame.transform.scale(enemyLaser.image0, (30,30))
            enemyLaser.rect.centerx = enemy1s[shooterIndex].rect.centerx
            enemyLaser.rect.centery = enemy1s[shooterIndex].rect.centery
            enemyLaser.setDirection(enemy1s[shooterIndex].getDirection() - 90)
            #move the laser forward
            enemyLaser.setSpeed(20)
            enemyLaser.update()
            #set the movement speed
            enemyLaser.setSpeed(7)
            #set the damage
            enemyLaser.storedValue1 = enemy1Damage

        #make the enemy1s move
        if pygame.time.get_ticks() - lastEnemy1Move >= enemy1MoveTimer:
            lastEnemy1Move = pygame.time.get_ticks()
            for enemy1 in getListOf("Enemy1"):
                #1 in 4 as to whether this specific enemy moves
                if random.random() < 0.25:
                    enemy1.movingTime = (random.random() * 4000) + 1000
                    #1 in 2 as to which direction the enemy1 moves
                    if random.random() > 0.5:
                        enemy1.setSpeed(enemy1Speed)
                    else:
                        enemy1.setSpeed(-enemy1Speed)

        #enemy2s
        #spawn enemy2s
        if sinceEnemy2Spawn >= enemy2CurrentSpawnTime and numEnemy2s < enemy2Cap:
            print("Spawned enemy2!")
            enemy2CurrentSpawnTime = enemy2SpawnBaseTime + (enemy2SpawnRandomTime * random.random())
            sinceEnemy2Spawn = 0
            #implement random spawn positions, both vertical and horizontal
            numEnemy2s += 1
            enemy2 = Sprite("enemy2.png","Enemy2",(0,0))
            enemy2.image = pygame.transform.scale(enemy2.image, enemy2Scale)
            enemy2.image0 = pygame.transform.scale(enemy2.image0, enemy2Scale)
            enemy2.rect.width = enemy2Scale[0]
            enemy2.rect.height = enemy2Scale[1]
            enemy2.colliderect = enemy2.rect
            #set the position
            #roughly half of the time the enemy2 spawns left and half on the right
            if random.random() > 0.5:
                enemy2.rect.x = 0
                enemy2.setDirection(90)
            else:
                enemy2.rect.x = width - enemy2.rect.width
                enemy2.setDirection(270)
            enemy2.rect.y = (height - enemy2.rect.height) * random.random()
            #set the speed
            enemy2.setSpeed(0)
            #change storedValue1 to a list and add the starting point to the trail list
            enemy2.storedValue1 = []
            enemy2.storedValue1.append(str((enemy2.rect.centerx,enemy2.rect.centery)) + "/" + str(pygame.time.get_ticks()))

        #make the enemy2s move
        if pygame.time.get_ticks() - lastEnemy2Move >= enemy2MoveTimer:
            lastEnemy2Move = pygame.time.get_ticks()
            #added capacity for multiple enemy2s, though there should only ever be one at a time :/
            for enemy2 in getListOf("Enemy2"):
                enemy2.storedValue1.append(str((enemy2.rect.centerx,enemy2.rect.centery)) + "/" + str(pygame.time.get_ticks()))
                enemy2.setDirectionTowards(playerBase.rect.x, playerBase.rect.y)
                enemy2.setSpeed(enemy2Speed)

        #handle the enemy2s' trail
        for enemy2 in getListOf("Enemy2"):
            trailPositions = []
            for pivotPos in enemy2.storedValue1:
                pivotPosition = pivotPos.split("/")[0]
                timeTurned = pivotPos.split("/")[1]
                if pygame.time.get_ticks() - float(timeTurned) <= enemy2TrailCutoff:
                    newPoint = (pivotPosition.split(","))
                    trailPositions.append((int(newPoint[0][1:len(newPoint[0])]),int(newPoint[1][1:-1])))
                else:
                    enemy2.storedValue1.remove(pivotPos)
            #make sure there are enough points to draw the line
            if len(trailPositions) > 0:
                trailPositions.append((enemy2.rect.centerx,enemy2.rect.centery))
                pygame.draw.lines(screen, enemy2TrailColour, False, trailPositions, 5)

        #enemy3s
        #spawn enemy3s
        if sinceEnemy3Spawn >= enemy3CurrentSpawnTime and numEnemy3s < enemy3Cap:
            print("Spawned enemy3!")
            enemy3CurrentSpawnTime = enemy3SpawnBaseTime + (enemy3SpawnRandomTime * random.random())
            sinceEnemy3Spawn = 0
            #implement random spawn positions, both vertical and horizontal
            numEnemy3s += 1
            enemy3 = Sprite("enemy3.png","Enemy3",(0,0))
            enemy3.image = pygame.transform.scale(enemy3.image, enemy3Scale)
            enemy3.image0 = pygame.transform.scale(enemy3.image0, enemy3Scale)
            enemy3.rect.width = enemy3Scale[0]
            enemy3.rect.height = enemy3Scale[1]
            enemy3.colliderect = enemy3.rect
            #set the position
            enemy3.rect.x = (width - enemy3.rect.width) * random.random()
            #roughly half of the enemy1s spawn top and half on the bottom
            if random.random() > 0.5:
                enemy3.rect.y = screenOffset
                enemy3.setDirection(180)
            else:
                enemy3.rect.y = height - enemy3.rect.height
                enemy3.setDirection(0)
            #set the speed
            enemy3.setSpeed(0)
            enemy3.storedValue3 = 3 + (2 * random.random())

        #make the enemy3s shoot
        if pygame.time.get_ticks() - lastEnemy3Shot >= 1500 and numEnemy3s > 0:
            lastEnemy3Shot = pygame.time.get_ticks()
            enemy3s = getListOf("Enemy3")
            shooterIndex = round(random.random() * len(enemy3s))
            #prevent crashes
            if shooterIndex == len(enemy3s):
                shooterIndex -= 1
            print("Enemy3, shoot!")
            #spawn the 4 lasers to be shot and set the position and direction of each
            for shotNum in range(4):
                enemyLaser = Sprite("laser3.png","EnemyLaser",(enemy3s[shooterIndex].rect.centerx,enemy3s[shooterIndex].rect.centery))
                enemyLaser.image = pygame.transform.scale(enemyLaser.image, (30,30))
                enemyLaser.image0 = pygame.transform.scale(enemyLaser.image0, (30,30))
                enemyLaser.rect.centerx = enemy3s[shooterIndex].rect.centerx
                enemyLaser.rect.centery = enemy3s[shooterIndex].rect.centery
                enemyLaser.setDirection(enemy3s[shooterIndex].getDirection() - (360 / 4) * shotNum)
                #move the laser forward
                enemyLaser.setSpeed(20)
                enemyLaser.update()
                #set the movement speed
                enemyLaser.setSpeed(7)
                #set the damage
                enemyLaser.storedValue1 = enemy3Damage

        #make the enemy3s move
        if pygame.time.get_ticks() - lastEnemy3Move >= enemy3MoveTimer:
            lastEnemy3Move = pygame.time.get_ticks()
            #set a new direction for movement - enemy3s never stop moving
            for enemy3 in getListOf("Enemy3"):
                #1 in 4 as to whether this specific enemy3 changes direction or not
                if random.random() < 0.25:
                    newDir = 359 * random.random()
                    enemy3.setDirection(newDir)
                    enemy3.setSpeed(enemy3Speed)
                    enemy3.storedValue2 = newDir

        #power-ups
        
        #laser power-up
        #check if expired
        if lPowerActive == True:
            if lPowerActiveTime + lPowerDuration <= pygame.time.get_ticks():
                print("Laser power-up has worn off!")
                lPowerActive = False
                #set the blaster's image to the shielded image (both power-ups were active before expiration)
                if sPowerActive == True:
                    regularBlasterFile = "shieldedPlayerBlaster.png"
                else:
                    regularBlasterFile = "playerBlasterTEST.png"
                #set the blaster accordingly
                playerBlaster.image = pygame.image.load(regularBlasterFile)
                playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
                playerBlaster.image0 = pygame.image.load(regularBlasterFile)
                playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)
        
        #spawn the laser power-up
        if sinceLPowerUpSpawn >= lPowerCurrentSpawnTime and lPowerExists == False:
            print("Spawned laser power-up!")
            lPowerCurrentSpawnTime = lPowerSpawnBaseTime + (lPowerSpawnRandomTime * random.random())
            sinceLPowerUpSpawn = 0
            lPowerExists = True
            #implement random spawn positions, both vertical and horizontal
            lPower = Sprite("powerUpLaser.png","lPowerUp",(0,0))
            lPower.image = pygame.transform.scale(lPower.image, (30,60))
            lPower.image0 = pygame.transform.scale(lPower.image0, (30,60))
            lPower.rect.width = 30
            lPower.rect.height = 30
            lPower.colliderect = lPower.rect
            
            #set the position
            #if the power-up spawns on the player, try again. never spawn the power-up on the player.
            spawnedOnPlayer = True
            playerSpawnPadding = 30
            while spawnedOnPlayer == True:
                spawnPowerUp(lPower)
                playerDist = (lPower.rect.centerx - playerBase.rect.centerx,
                              lPower.rect.centery - playerBase.rect.centery)
                #get the magnitude of the distance vector (distance) and if not spawned on player, break the loop
                if math.sqrt(playerDist[0]**2 + playerDist[1]**2) > playerSpawnPadding:
                    spawnedOnPlayer = False
                else:
                    spawnedOnPlayer = True
            
            #set the speed
            lPower.setSpeed(0)

        #shield power-up
        #check if expired
        if sPowerActive == True:
            if sPowerActiveTime + sPowerDuration <= pygame.time.get_ticks():
                print("Shield power-up has worn off!")
                sPowerActive = False
                #set the blaster's image to the lPower-upped image (both power-ups were active before expiration)
                if lPowerActive == True:
                    regularBlasterFile = "playerBlasterLPowerUpped.png"
                else:
                    regularBlasterFile = "playerBlasterTEST.png"
                #set the blaster accordingly
                playerBlaster.image = pygame.image.load(regularBlasterFile)
                playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
                playerBlaster.image0 = pygame.image.load(regularBlasterFile)
                playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)
                #set the base accordingly
                regularBaseFile = "playerBase.png"
                playerBase.image = pygame.image.load(regularBaseFile)
                playerBase.image = pygame.transform.scale(playerBase.image, playerScale)
                playerBase.image0 = pygame.image.load(regularBaseFile)
                playerBase.image0 = pygame.transform.scale(playerBase.image0, playerScale)
                #reset the player image rotations to what they should be
                playerBlaster.turn(0)
                playerBase.turn(0)
        
        #spawn the shield power-up
        if sinceSPowerUpSpawn >= sPowerCurrentSpawnTime and sPowerExists == False:
            print("Spawned shield power-up!")
            sPowerCurrentSpawnTime = sPowerSpawnBaseTime + (sPowerSpawnRandomTime * random.random())
            sinceSPowerUpSpawn = 0
            sPowerExists = True
            #implement random spawn positions, both vertical and horizontal
            sPower = Sprite("powerUpShield.png","sPowerUp",(0,0))
            sPower.image = pygame.transform.scale(sPower.image, (30,60))
            sPower.image0 = pygame.transform.scale(sPower.image0, (30,60))
            sPower.rect.width = 30
            sPower.rect.height = 30
            sPower.colliderect = sPower.rect
            
            #set the position
            #if the power-up spawns on the player, try again. never spawn the power-up on the player.
            spawnedOnPlayer = True
            playerSpawnPadding = 30
            edgesPadding = 30
            while spawnedOnPlayer == True:
                spawnPowerUp(sPower)
                playerDist = (sPower.rect.centerx - playerBase.rect.centerx,
                              sPower.rect.centery - playerBase.rect.centery)
                #get the magnitude of the distance vector (distance) and if not spawned on player, break the loop
                if math.sqrt(playerDist[0]**2 + playerDist[1]**2) > playerSpawnPadding:
                    spawnedOnPlayer = False
                else:
                    spawnedOnPlayer = True
            
            #set the speed
            sPower.setSpeed(0)

        #healing power-up
        #check if expired
        if hPowerActive == True:
            if hPowerActiveTime + hPowerDuration <= pygame.time.get_ticks():
                print("Healing power-up has worn off!")
                hPowerActive = False

        #apply healing effect
        if hPowerActive == True:
            if lastHealTime + healIncrement <= pygame.time.get_ticks():
                lastHealTime = pygame.time.get_ticks()
                if currentHealth + 1 >= maxHealth:
                    currentHealth = maxHealth
                else:
                    currentHealth += 1
                
        #spawn the healing power-up
        if nextHPowerUpSpawn <= currentScore:
            print("Spawned healing power-up!")
            nextHPowerUpSpawn = currentScore + hPowerUpInterval
            hPowerUpInterval += hPowerUpIntervalBoost
            hPowerExists = True
            #implement random spawn positions, both vertical and horizontal
            hPower = Sprite("powerUpHealth.png","hPowerUp",(0,0))
            hPower.image = pygame.transform.scale(hPower.image, (38,38))
            hPower.image0 = pygame.transform.scale(hPower.image0, (38,38))
            hPower.rect.width = 30
            hPower.rect.height = 30
            hPower.colliderect = hPower.rect
            
            #set the position
            #if the power-up spawns on the player, try again. never spawn the power-up on the player.
            spawnedOnPlayer = True
            playerSpawnPadding = 30
            edgesPadding = 30
            while spawnedOnPlayer == True:
                spawnPowerUp(hPower)
                playerDist = (hPower.rect.centerx - playerBase.rect.centerx,
                              hPower.rect.centery - playerBase.rect.centery)
                #get the magnitude of the distance vector (distance) and if not spawned on player, break the loop
                if math.sqrt(playerDist[0]**2 + playerDist[1]**2) > playerSpawnPadding:
                    spawnedOnPlayer = False
                else:
                    spawnedOnPlayer = True
            
            #set the speed
            hPower.setSpeed(0)
            

        #player
        #deal with player input
        key=pygame.key.get_pressed()  # Get a list of what keys are being pressed.
        mouse=pygame.key.get_pressed()

        #forwards/accelerate
        if key[pygame.K_w]:
            playerBase.setSpeed(playerSpeed)
        #backwards/decelerate
        if key[pygame.K_s]:
            playerBase.setSpeed(-playerSpeed)
        #turn left
        if key[pygame.K_a]:
            playerBase.turn(-1)
        #turn right
        if key[pygame.K_d]:
            playerBase.turn(1)

        #set speed to 0 if no keys are pressed
        if key[pygame.K_w] != True and key[pygame.K_s] != True:
            playerBase.setSpeed(0)

        #playerBlaster.turn(1)
        playerBlaster.setDirectionTowards(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        #if the player clicks the mouse, shoot a laser
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.time.get_ticks() - lastPlayerShot >= 500:
            print("Shoot!")
            lastPlayerShot = pygame.time.get_ticks()
            #test for whether the laser power-up is active or not
            if lPowerActive == False:
                #handle the image
                laser = Sprite("laser1.png","Laser",(playerBlaster.rect.centerx-5,playerBlaster.rect.centery-20))
                laser.image = pygame.transform.scale(laser.image, (30,30))
                laser.image0 = pygame.transform.scale(laser.image0, (30,30))
                #store the fact that the laser is not powered up
                laser.storedValue1 = False
            else:
                #handle the image
                laser = Sprite("lPowerUppedLaser1.png","Laser",(playerBlaster.rect.centerx-5,playerBlaster.rect.centery-20))
                laser.image = pygame.transform.scale(laser.image, (60,30))
                laser.image0 = pygame.transform.scale(laser.image0, (60,30))
                #store the fact that the laser is powered up
                laser.storedValue1 = True
            laser.rect.centerx = playerBlaster.rect.centerx
            laser.rect.centery = playerBlaster.rect.centery
            laser.setDirection(playerBlaster.getDirection())
            #move the laser forward
            laser.setSpeed(playerShotSpeed)
            laser.update() #by updating the laser individually and only once, the laser moves 20 pixels in the set direction.
            #set the movement speed
            laser.setSpeed(7)

        #before the sprite update, set the enemy3 direction to the one for movement
        for enemy3 in getListOf("Enemy3"):
            enemy3.storedValue1 = enemy3.getDirection()
            enemy3.setDirection(enemy3.storedValue2)
        
        allSprites.update()

        #after the sprite update, set the enemy3 direction to the one for aesthetics
        for enemy3 in getListOf("Enemy3"):
            enemy3.setDirection(enemy3.storedValue1)
            enemy3.turn(enemy3.storedValue3)

        #stop the player and enemies from going off-screen
        #stop the player
        if playerBase.rect.centerx < 0 + edgesPadding:
            playerBase.rect.centerx = 0 + edgesPadding
        if playerBase.rect.centerx > width - edgesPadding:
            playerBase.rect.centerx = width - edgesPadding
        if playerBase.rect.centery < screenOffset + edgesPadding:
            playerBase.rect.centery = screenOffset + edgesPadding
        if playerBase.rect.centery > height - edgesPadding:
            playerBase.rect.centery = height - edgesPadding

        #stop the enemies and push them back in their opposite directions
        for enemy1 in getListOf("Enemy1"):
            if enemy1.rect.centerx < 0 + (enemy1.rect.width / 2):
                enemy1.rect.centerx = 0 + (enemy1.rect.width / 2)
                enemy1.setSpeed(-enemy1.getSpeed())
            if enemy1.rect.centerx > width - (enemy1.rect.width / 2):
                enemy1.rect.centerx = width - (enemy1.rect.width / 2)
                enemy1.setSpeed(-enemy1.getSpeed())
            if enemy1.rect.centery < screenOffset + (enemy1.rect.height / 2):
                enemy1.rect.centery = screenOffset + (enemy1.rect.height / 2)
                enemy1.setSpeed(-enemy1.getSpeed())
            if enemy1.rect.centery > height - (enemy1.rect.height / 2):
                enemy1.rect.centery = height - (enemy1.rect.height / 2)
                enemy1.setSpeed(-enemy1.getSpeed())

        for enemy2 in getListOf("Enemy2"):
            if enemy2.rect.centerx < 0 + (enemy2.rect.width / 2):
                enemy2.rect.centerx = 0 + (enemy2.rect.width / 2)
                enemy2.setSpeed(-enemy2.getSpeed())
            if enemy2.rect.centerx > width - (enemy2.rect.width / 2):
                enemy2.rect.centerx = width - (enemy2.rect.width / 2)
                enemy2.setSpeed(-enemy2.getSpeed())
            if enemy2.rect.centery < screenOffset + (enemy2.rect.height / 2):
                enemy2.rect.centery = screenOffset + (enemy2.rect.height / 2)
                enemy2.setSpeed(-enemy2.getSpeed())
            if enemy2.rect.centery > height - (enemy2.rect.height / 2):
                enemy2.rect.centery = height - (enemy2.rect.height / 2)
                enemy2.setSpeed(-enemy2.getSpeed())

        for enemy3 in getListOf("Enemy3"):
            if enemy3.rect.centerx < 0 + (enemy3.rect.width / 2):
                enemy3.rect.centerx = 0 + (enemy3.rect.width / 2)
                enemy3.setSpeed(-enemy3.getSpeed())
            if enemy3.rect.centerx > width - (enemy3.rect.width / 2):
                enemy3.rect.centerx = width - (enemy3.rect.width / 2)
                enemy3.setSpeed(-enemy3.getSpeed())
            if enemy3.rect.centery < screenOffset + (enemy3.rect.height / 2):
                enemy3.rect.centery = screenOffset + (enemy3.rect.height / 2)
                enemy3.setSpeed(-enemy3.getSpeed())
            if enemy3.rect.centery > height - (enemy3.rect.height / 2):
                enemy3.rect.centery = height - (enemy3.rect.height / 2)
                enemy3.setSpeed(-enemy3.getSpeed())

        #test for collisions
        for laser in getListOf("Laser"):
            if laser.isTouchingSprite("EnemyLaser",True):
                #if the laser is not powered up, no piercing
                if laser.storedValue1 == False:
                    laser.goodbye(0)
            
            #if the laser is touching an enemy1, kill it and the laser
            if laser.isTouchingSprite("Enemy1",True):
                numEnemy1s -= 1
                currentScore += enemy1ScoreValue
                score_text=font.render("Score: " + str(currentScore),1, scoreTextColour)
                #if the laser is not powered up, no piercing
                if laser.storedValue1 == False:
                    laser.goodbye(0)

            #if the laser is touching an enemy2, kill it and the laser
            if laser.isTouchingSprite("Enemy2",True):
                numEnemy2s -= 1
                currentScore += enemy2ScoreValue
                score_text=font.render("Score: " + str(currentScore),1, scoreTextColour)
                #if the laser is not powered up, no piercing
                if laser.storedValue1 == False:
                    laser.goodbye(0)

            #if the laser is touching an enemy3, kill it and the laser
            if laser.isTouchingSprite("Enemy3",True):
                numEnemy3s -= 1
                currentScore += enemy3ScoreValue
                score_text=font.render("Score: " + str(currentScore),1, scoreTextColour)
                #if the laser is not powered up, no piercing
                if laser.storedValue1 == False:
                    laser.goodbye(0)

        for enemyLaser in getListOf("EnemyLaser"):
            if enemyLaser.isTouchingSprite("PlayerBase",False):
                print("Player has been hit!!")
                damagePlayer(enemyLaser.storedValue1)
                enemyLaser.goodbye(0)

        if playerBase.isTouchingSprite("Enemy2",False):
            if pygame.time.get_ticks() - enemy2.storedValue2 >= enemy2DamageIncrement:
                enemy2.storedValue2 = pygame.time.get_ticks()
                damagePlayer(enemy2Damage)

        #test if the player is picking up any power-ups
        if playerBase.isTouchingSprite("lPowerUp",True):
            print("Player has picked up a laser power-up!")
            lPowerExists = False
            lPowerActive = True
            lPowerActiveTime = pygame.time.get_ticks()
            #set the blaster's image to the shielded laser power-upped image (both power-ups active)
            if sPowerActive == True:
                poweredUpBlasterFile = "shieldedPlayerBlasterLPowerUpped.png"
            else:
                poweredUpBlasterFile = "playerBlasterLPowerUpped.png"
            #set the blaster accordingly
            playerBlaster.image = pygame.image.load(poweredUpBlasterFile)
            playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
            playerBlaster.image0 = pygame.image.load(poweredUpBlasterFile)
            playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)

        if playerBase.isTouchingSprite("sPowerUp",True):
            print("Player has picked up a shield power-up!")
            sPowerExists = False
            sPowerActive = True
            sPowerActiveTime = pygame.time.get_ticks()
            #set the blaster's image to the shielded laser power-upped image (both power-ups active)
            if lPowerActive == True:
                shieldedBlasterFile = "shieldedPlayerBlasterLPowerUpped.png"
            else:
                shieldedBlasterFile = "shieldedPlayerBlaster.png"
            #set the blaster accordingly
            playerBlaster.image = pygame.image.load(shieldedBlasterFile)
            playerBlaster.image = pygame.transform.scale(playerBlaster.image, playerScale)
            playerBlaster.image0 = pygame.image.load(shieldedBlasterFile)
            playerBlaster.image0 = pygame.transform.scale(playerBlaster.image0, playerScale)
            #set the base accordingly
            shieldedBaseFile = "shieldedPlayerBase.png"
            playerBase.image = pygame.image.load(shieldedBaseFile)
            playerBase.image = pygame.transform.scale(playerBase.image, playerScale)
            playerBase.image0 = pygame.image.load(shieldedBaseFile)
            playerBase.image0 = pygame.transform.scale(playerBase.image0, playerScale)
            #reset the player image rotations to what they should be
            playerBlaster.turn(0)
            playerBase.turn(0)

        if playerBase.isTouchingSprite("hPowerUp",True):
            print("Player has picked up a healing power-up!")
            hPowerExists = False
            hPowerActive = True
            hPowerActiveTime = pygame.time.get_ticks()

        #handle the health bar
        #failsafe to prevent crashes between game states (gameover)
        if currentHealth >=0:
            healthGreen.image = pygame.transform.scale(healthGreen.image, (round(healthBarSize[0] * (currentHealth / maxHealth)), healthBarSize[1]))
            if currentHealth < maxHealth:
                redHealthBoost = 0
                for damage in damageQueue:
                    damageTaken = damage.split(",")[0]
                    timeTaken = damage.split(",")[1]
                    if pygame.time.get_ticks() - float(timeTaken) <= healthBarDamageTime:
                        redHealthBoost += int(damageTaken)
                    else:
                        damageQueue.remove(damage)

                if currentHealth + redHealthBoost <= maxHealth:
                    healthRed.image = pygame.transform.scale(healthRed.image, (round(healthBarSize[0] * ((currentHealth + redHealthBoost) / maxHealth)), healthBarSize[1]))
                else:
                    healthRed.image = pygame.transform.scale(healthRed.image, (healthBarSize[0], healthBarSize[1]))

        #center the blaster
        playerBlaster.rect.centerx = playerBase.rect.centerx
        playerBlaster.rect.centery = playerBase.rect.centery

        # Draws all the sprites to the screen.
        allSprites.draw(screen)
        uiSprites.draw(screen)

    else:

        #draw the score to the screen
        screen.fill((50,50,50))
        #draw the game over screen
        gameover_text = fontBig.render("Game Over",1, scoreTextColour)
        screen.blit(gameover_text,((width / 2) - (gameover_text.get_width() / 2),(height / 2) - 80))

        if savedHighscore == False:
            savedHighscore = True
            
            #open the file
            #highscores = open(highscoresFile)
            currentScore=22
            lineCount = 0
            numScores = 5
            lineOffset = 35
            highscoresList = []
            with open(highscoresFile,"r") as input:
                for line in input:
                    lineCount += 1
                    if(lineCount <= numScores):
                        highscoresList.append(line)

            #print("The length is: " + str(len(highscoresList)))

            #make a 'cloud' copy of the current highscores
            newHighscoresList = highscoresList

            #create the flag to prevent overwriting multiple highscores
            newScore = False
            
            for index in range(len(highscoresList)):
                currentLine = highscoresList[index]
                #isolate the score part of the line being read
                currentHighscore = currentLine.replace("\n","")
                currentHighScore = currentHighscore.split(" ")
                currentHighScore = currentHighScore[len(currentHighScore) - 1]
                #if this line is less than the new highscore and nothing else has been overidden
                if int(str(currentHighScore).strip()) < currentScore and newScore == False:
                    #set flags and values
                    newScore = True
                    newScoreIndex = index
                    #build and insert the new highscore to the list
                    now = datetime.datetime.now()
                    currentDate = str(now.strftime("%Y/%m/%d"))
                    newHighscoresList.insert(index, currentDate + " " + str(currentScore))

            #write the list back into the input file
            with open(highscoresFile,"r+") as output:
                text = ""
                for lineIndex in range(len(newHighscoresList)):
                    if lineIndex < numScores:
                        text += str(newHighscoresList[lineIndex]).strip()# + "\n"
                        #add a newline character unless it is the last line
                        if lineIndex < (numScores - 1):
                            text += "\n"
                output.seek(0)
                output.write(text)
                output.truncate()

        #draw the highscores table
        highscoreTitle = fontMed.render("Highscores:",1, scoreTextColour)
        screen.blit(highscoreTitle, ((width / 2) - (highscoreTitle.get_width() / 2), (height / 2) + 15))
        for blitIndex in range(len(newHighscoresList)):
            if blitIndex < numScores:
                if blitIndex == newScoreIndex:
                    highscore_text = font.render(str(newHighscoresList[blitIndex]).strip(),1, (122,208,255))
                else:
                    highscore_text = font.render(str(newHighscoresList[blitIndex]).strip(),1, scoreTextColour)
                screen.blit(highscore_text,((width / 2) - (highscore_text.get_width() / 2),((height / 2) + 100) + ((lineOffset * blitIndex) - lineOffset)))

    for sprite in allSprites:
            sprite.recordLast()

            #draw the score to the screen
            score_text = font.render("Score: " + str(currentScore),1, scoreTextColour)
            screen.blit(score_text,(10,4))

    # Update the window.
    pygame.display.update()

    #store the last frame
    lastFrameTime = pygame.time.get_ticks()

# Close the window.
pygame.quit()
