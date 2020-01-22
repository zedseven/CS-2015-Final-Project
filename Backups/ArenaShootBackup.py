# Name: Zacchary Dempsey-Plante
# Date started: Jan. 15, 2016
# Description: A driving arena shooter.

import pygame, sys, os, math, random
from pygame.locals import *
os.environ['SDL_VIDEODRIVER'] = 'windib'

#allSprites = pygame.sprite.Group()
allSprites = pygame.sprite.LayeredUpdates()

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



###########################
## End of Sprite class code - don't touch code above
###########################

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Storing the width and height of the screen.
width = screen.get_width()
height = screen.get_height()
print ("The width is " + str(width))
print ("The height is " + str(height))

# Create a clock to keep track of time
clock = pygame.time.Clock()
lastFrameTime = 0

background = Sprite("ground.png","Ground",(0,0))
background.setSpeed(0)

playerScale = (80,40)

playerBase = Sprite("playerBase.png","PlayerBase",(width/2,height-60))
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
##playerBlaster.rect.width = playerScale[0]
##playerBlaster.rect.height = playerScale[1]
playerBlaster.colliderect = playerBlaster.rect
playerBlaster.setDirection(270)
playerBlaster.setSpeed(0)

running = 1

font = pygame.font.Font(None, 18)

#enemy variables
#enemy1 variables
lastEnemy1Spawn = 0
lastEnemy1Shot = 0
lastEnemy1Move = 0
enemy1MoveTimer = 500
numEnemy1s = 0
enemy1Cap = 6
enemy1Scale = (30,30)
enemy1Speed = 5

#enemy3 variables
lastEnemy3Spawn = 0
lastEnemy3Shot = 0
lastEnemy3Move = 0
enemy3MoveTimer = 300
numEnemy3s = 0
enemy3Cap = 2
enemy3Scale = (40,40)
enemy3Speed = 6

#player variables
playerSpeed = 4
playerShotSpeed = 35
lastPlayerShot = 0
currentScore = 0
currentHealth = 100

while running:
    
    # Sets the frame rate to 30 frames/second.
    clock.tick(30)
    
    event = pygame.event.poll()
    
    if event.type == pygame.QUIT:
        running = 0

    # Color the whole screen with a solid color.
    screen.fill((255,255,255))

    #########################################
    # Add your code here.
    #########################################

    #enemies
    #spawn enemy1s
    if pygame.time.get_ticks() - lastEnemy1Spawn >= 1500 and numEnemy1s < enemy1Cap:
        #print("Spawned enemy1!")
        lastEnemy1Spawn = pygame.time.get_ticks()
        #implement random spawn positions, both vertical and horizontal
        if random.random() > 0.5:
            print("horizontal")
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
            if random.random() > 0.5:
                enemy1.rect.y = 0
                enemy1.setDirection(180)#90)
            else:
                enemy1.rect.y = height - enemy1.rect.height
                enemy1.setDirection(0)#270)
            #set the speed
            enemy1.setSpeed(0)
        else:
            print("vertical")
            numEnemy1s += 1
            enemy1 = Sprite("enemy1.png","Enemy1",(0,0))
            enemy1.image = pygame.transform.scale(enemy1.image, enemy1Scale)
            enemy1.image0 = pygame.transform.scale(enemy1.image0, enemy1Scale)
            enemy1.rect.width = enemy1Scale[0]
            enemy1.rect.height = enemy1Scale[1]
            enemy1.colliderect = enemy1.rect
            #set the position
            if random.random() > 0.5:
                enemy1.rect.x = 0
                enemy1.setDirection(90)#0)
            else:
                enemy1.rect.x = width - enemy1.rect.width
                enemy1.setDirection(270)#180)
            enemy1.rect.y = (height - enemy1.rect.height) * random.random()
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
        enemyLaser.storedValue1 = 10

    #make the enemy1s move
    if pygame.time.get_ticks() - lastEnemy1Move >= enemy1MoveTimer:
        lastEnemy1Move = pygame.time.get_ticks()
        for enemy1 in getListOf("Enemy1"):
            if random.random() < 0.25:
                enemy1.movingTime = (random.random() * 4000) + 1000
                if random.random() > 0.5:
                    enemy1.setSpeed(enemy1Speed)
                else:
                    enemy1.setSpeed(-enemy1Speed)

    #spawn enemy3s
    if pygame.time.get_ticks() - lastEnemy3Spawn >= 1500 and numEnemy3s < enemy3Cap:
        #print("Spawned enemy3!")
        lastEnemy3Spawn = pygame.time.get_ticks()
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
        if random.random() > 0.5:
            enemy3.rect.y = 0
            enemy3.setDirection(180)#90)
        else:
            enemy3.rect.y = height - enemy3.rect.height
            enemy3.setDirection(0)#270)
        #set the speed
        enemy3.setSpeed(0)

    #make the enemy3s shoot
    if pygame.time.get_ticks() - lastEnemy3Shot >= 1500 and numEnemy3s > 0:
        lastEnemy3Shot = pygame.time.get_ticks()
        enemy3s = getListOf("Enemy3")
        shooterIndex = round(random.random() * len(enemy3s))
        if shooterIndex == len(enemy3s):
            shooterIndex -= 1
        print("Enemy3, shoot!")
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
            enemyLaser.storedValue1 = 5

    #make the enemy3s move
    if pygame.time.get_ticks() - lastEnemy3Move >= enemy3MoveTimer:
        lastEnemy3Move = pygame.time.get_ticks()
        for enemy3 in getListOf("Enemy3"):
            if random.random() < 0.25:
                newDir = 359 * random.random()
                enemy3.setDirection(newDir)
                enemy3.setSpeed(5)
                enemy3.storedValue2 = newDir

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
        laser = Sprite("laser1.png","Laser",(playerBlaster.rect.centerx-5,playerBlaster.rect.centery-20))
        laser.image = pygame.transform.scale(laser.image, (30,30))
        laser.image0 = pygame.transform.scale(laser.image0, (30,30))
        laser.rect.centerx = playerBlaster.rect.centerx
        laser.rect.centery = playerBlaster.rect.centery
        laser.setDirection(playerBlaster.getDirection())
        #laser.setDirectionTowards(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        #move the laser forward
        laser.setSpeed(playerShotSpeed)
        laser.update() #by updating the laser individually and only once, the laser moves 20 pixels in the set direction.
        #set the movement speed
        laser.setSpeed(7)

    #set the direction to move in
    for enemy3 in getListOf("Enemy3"):
        enemy3.storedValue1 = enemy3.getDirection()
        enemy3.setDirection(enemy3.storedValue2)
    
    allSprites.update()

    #set the aesthetic direction value
    for enemy3 in getListOf("Enemy3"):
        enemy3.setDirection(enemy3.storedValue1)
        enemy3.turn(3)

    #stop the player and enemies from going off-screen
    #stop the player
    if playerBase.rect.centerx < 0:
        playerBase.rect.centerx = 0
    if playerBase.rect.centerx > width:# - (playerBase.rect.height / 2):
        playerBase.rect.centerx = width# - (playerBase.rect.height / 2)
    if playerBase.rect.centery < 0:
        playerBase.rect.centery = 0
    if playerBase.rect.centery > height:# - (playerBase.rect.width / 2):
        playerBase.rect.centery = height# - (playerBase.rect.width / 2)

    #stop the enemies
    for enemy1 in getListOf("Enemy1"):
        if enemy1.rect.centerx < 0 + (enemy1.rect.width / 2):
            enemy1.rect.centerx = 0 + (enemy1.rect.width / 2)
            enemy1.setSpeed(-enemy1.getSpeed())
        if enemy1.rect.centerx > width - (enemy1.rect.width / 2):
            enemy1.rect.centerx = width - (enemy1.rect.width / 2)
            enemy1.setSpeed(-enemy1.getSpeed())
        if enemy1.rect.centery < 0 + (enemy1.rect.height / 2):
            enemy1.rect.centery = 0 + (enemy1.rect.height / 2)
            enemy1.setSpeed(-enemy1.getSpeed())
        if enemy1.rect.centery > height - (enemy1.rect.height / 2):
            enemy1.rect.centery = height - (enemy1.rect.height / 2)
            enemy1.setSpeed(-enemy1.getSpeed())

    for enemy3 in getListOf("Enemy3"):
        if enemy3.rect.centerx < 0 + (enemy3.rect.width / 2):
            enemy3.rect.centerx = 0 + (enemy3.rect.width / 2)
            enemy3.setSpeed(-enemy3.getSpeed())
        if enemy3.rect.centerx > width - (enemy3.rect.width / 2):
            enemy3.rect.centerx = width - (enemy3.rect.width / 2)
            enemy3.setSpeed(-enemy3.getSpeed())
        if enemy3.rect.centery < 0 + (enemy3.rect.height / 2):
            enemy3.rect.centery = 0 + (enemy3.rect.height / 2)
            enemy3.setSpeed(-enemy3.getSpeed())
        if enemy3.rect.centery > height - (enemy3.rect.height / 2):
            enemy3.rect.centery = height - (enemy3.rect.height / 2)
            enemy3.setSpeed(-enemy3.getSpeed())

    #tdest for collisions
    for laser in getListOf("Laser"):
        if laser.isTouchingSprite("EnemyLaser",True):
            laser.goodbye(0)
        
        #if the laser is touching an enemy1, kill it and the laser
        if laser.isTouchingSprite("Enemy1",True):
            numEnemy1s -= 1
            currentScore += 3
            laser.goodbye(0)

        #if the laser is touching an enemy3, kill it and the laser
        if laser.isTouchingSprite("Enemy3",True):
            numEnemy3s -= 1
            currentScore += 6
            laser.goodbye(0)

    for enemyLaser in getListOf("EnemyLaser"):
        if enemyLaser.isTouchingSprite("PlayerBase",False):
            print("Player has been hit!!")
            currentHealth -= enemyLaser.storedValue1
            enemyLaser.goodbye(0)
                

    #center the blaster
    playerBlaster.rect.centerx = playerBase.rect.centerx
    playerBlaster.rect.centery = playerBase.rect.centery

    # Draws all the sprites to the screen.
    allSprites.draw(screen)

    # Update the window.
    pygame.display.update()

    #store the last frame
    lastFrameTime = pygame.time.get_ticks()

    print("Health: " + str(currentHealth) + " Score: " + str(currentScore))

# Close the window.
pygame.quit()
