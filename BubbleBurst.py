"""
BubbleBurst
CS1822 Python Games Project
Authors: Sazmina Sandia, Davit Gevorgyan, Ahmed Hassan and Joseph Salter
Royal Holloway, University of London
"""

import simplegui
import random
import math

class Game:
    
    # Canvas dimensions
    WIDTH = 1000
    HEIGHT = 750
    
    # Class to store information about sprite images
    class SpriteInfo:
        def __init__(self, centerOfSprite, sizeOfSprite, radiusOfSprite = 0, lifespan = None, animated = False, grid = None):
            self.center = centerOfSprite
            self.size = sizeOfSprite
            self.radius = radiusOfSprite
            if lifespan:
                self.lifespan = lifespan
            else:
                self.lifespan = float('inf')
            self.animated = animated
            self.grid = grid

        def getCenter(self):
            return self.center

        def getSize(self):
            return self.size

        def getRadius(self):
            return self.radius

        def getGrid(self):
            return self.grid

        def getAnimated(self):
            return self.animated

        def getLifespan(self):
            return self.lifespan
    
    
    # Class to store information about sprite objects
    class Sprite:
        def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
            self.image = image
            self.imageCenter = info.getCenter()
            self.imageCenterTemp = info.getCenter()
            self.imageSize = info.getSize()
            self.radius = info.getRadius()
            self.lifespan = info.getLifespan()
            self.grid = info.getGrid()
            self.animated = info.getAnimated()
            self.pos = pos
            self.vel = vel
            self.angle = ang
            self.angleVelocity = ang_vel
            self.age = 0
            if sound:
                sound.rewind()
                sound.play()      

        def getVelocity(self):
            return self.vel

        def getRadius(self):
            return self.radius  
        
        def getImage(self):
            return self.image

        def getCenter(self):
            return self.imageCenter

        def getPosition(self):
            return self.pos

        # Check for any collisions
        def collide(self, otherObj):
            if Game.Vector.calculateDistance(self.pos, otherObj.pos) <= self.radius + otherObj.getRadius():
                return True
            False

        def update(self):
            # Update the age
            self.age += 1

            # Return condition of object's life
            if self.age > self.lifespan:
                return True
            False

            # Update the angle
            self.angle += self.angleVelocity

            # Update the position
            self.pos.x = ((self.vel.x + self.pos.x) % Game.WIDTH)
            self.pos.y = ((self.vel.y + self.pos.y) % Game.HEIGHT)
            
        def draw(self, canvas):
            verticalOffset, horizontalOffset = 0, 0
            if self.animated:
                horizontalOffset = self.imageSize[0]*(self.age%self.grid)
                verticalOffset = self.imageSize[1]*(self.age // self.grid)

            canvas.draw_image(self.image, [self.imageCenter[0] + horizontalOffset, \
                                           self.imageCenter[1] + verticalOffset], \
                              self.imageSize, self.pos.get_p(), self.imageSize, self.angle)


    # Class to initialise submarine object
    class Player:
        def __init__(self, positionOfSubmarine, velOfSubmarine, angleOfSubmarine, image, info, sound = None):
            self.image = image
            self.imageCenter = info.getCenter()
            self.imageCenterThrust = (info.getCenter()[0] * 3, info.getCenter()[1])
            self.imageSize = info.getSize()
            self.radius = info.getRadius()
            self.sound = sound
            self.pos = positionOfSubmarine
            self.vel = velOfSubmarine
            self.thrust = False
            self.angle = angleOfSubmarine
            self.angleVelocity = 0
            
        def rotateLeft(self):
            self.angleVelocity = -.06

        def rotateRight(self):
            self.angleVelocity = .06

        def rotateStop(self):
            self.angleVelocity = 0

        def getPosition(self):
            return self.pos

        def getVelocity(self):
            return self.vel

        def getRadius(self):
            return self.radius

        def submarineEngineOn(self):
            self.thrust = True
            if self.sound:
                self.sound.play()

        def submarineEngineOff(self):
            self.thrust = False
            if self.sound:
                self.sound.rewind()

        # Function to handle water bullets
        def shoot(self, waterBulletNum):
            waterBulletPosition = Game.Vector(self.pos.x + self.radius * Game.forward_vector.x, self.pos.y + self.radius * Game.forward_vector.y)
            waterBulletVelocity = Game.Vector(self.vel.x + (6 * Game.forward_vector.x), self.vel.y + (6 * Game.forward_vector.y))
            bullets = Game.waterBulletsImg
            bulletsInfo = Game.waterBulletsInfo

            Game.game.waterBulletsGroup.add(Game.Sprite(waterBulletPosition, waterBulletVelocity, self.angle, 0, \
                               bullets, bulletsInfo, Game.waterBulletSound))

        # Key up handler      
        def keyUp(key):
            if key == simplegui.KEY_MAP["left"]:
                Game.theSubmarine.rotateStop()
            elif key == simplegui.KEY_MAP["right"]:
                Game.theSubmarine.rotateStop()
            elif key == simplegui.KEY_MAP["up"]:
                Game.theSubmarine.submarineEngineOff()

        # Key down handler     
        def keyDown(key):
            if Game.game.lives > 0:
                if key == simplegui.KEY_MAP["left"]:
                    Game.theSubmarine.rotateLeft()
                elif key == simplegui.KEY_MAP["right"]:
                    Game.theSubmarine.rotateRight()

                elif key == simplegui.KEY_MAP["up"]:
                    Game.theSubmarine.submarineEngineOn()

                elif key == simplegui.KEY_MAP["space"]:
                    Game.theSubmarine.shoot(0)   

                elif key == simplegui.KEY_MAP["c"]:
                    Game.theSubmarine.shoot(1)

            if key == simplegui.KEY_MAP["s"]:
                Game.frame.stop()

        def draw(self,canvas):
            if self.thrust:
                imageCenter = self.imageCenterThrust
            else:
                imageCenter = self.imageCenter

            canvas.draw_image(self.image, imageCenter, self.imageSize, self.pos.get_p(), self.imageSize, self.angle)

        def update(self):
            global forward_vector

            # Update the angle
            self.angle += self.angleVelocity

            # Update the velocity
            Game.forward_vector = Game.Vector.convertAngleToVector(self.angle)
            self.vel.x *= .975
            self.vel.y *= .975

            if self.thrust:
                self.vel.x += (Game.forward_vector.x) * .10
                self.vel.y += (Game.forward_vector.y) * .10

            # Update the position
            self.pos.x = ((self.vel.x + self.pos.x) % Game.WIDTH)
            self.pos.y = ((self.vel.y + self.pos.y) % Game.HEIGHT)


    class Interaction:
        def __init__(self, score=0):
            self.bubbleGroup = set([])
            self.bubbleBurstGroup = set([])
            self.waterBulletsGroup = set([]) 
            self.started = False
            self.score = score
            self.oxygen = 10
            self.oxygenLoseCurrent = 0
            self.oxygenLose = 100
            self.alarmCooldown = False
            self.lives = 3
            self.backgroundTime = 0.5
            self.difficulty = 0
            
        # Handler that spawns a bubble    
        def bubbleSpawner(): 

            if Game.game.started:
                bubblePosition = Game.Vector(random.randrange(0, Game.WIDTH), random.randrange(0, Game.HEIGHT))
                bubbleVelocity = Game.Vector(random.random() * (.8 + Game.game.difficulty) - (.2 + Game.game.difficulty),
                            random.random() * (.8 + Game.game.difficulty) - (.2 + Game.game.difficulty))
                newBubbleVelocity = random.random() * .2 - .1
                bubbleNum = random.randint(0, 2)
                newBubble = Game.Sprite(bubblePosition, bubbleVelocity, 0, newBubbleVelocity, Game.bubbleImg, Game.bubbleInfo)
                if len(Game.game.bubbleGroup) < 10 and bubblePosition.subtract(Game.theSubmarine.pos).x > (newBubble.radius + Game.theSubmarine.radius) * 1.5:
                    Game.game.bubbleGroup.add(newBubble)
        
        # Function to handle a group of sprites, deleting them once they have been processed
        def handleSpriteGroup(spriteSet, canvas):
            temporarySet = spriteSet.copy()
            for object in temporarySet:
                object.draw(canvas)
                if object.update():
                    spriteSet.remove(object)

        def groupCollision(spriteSet, otherObj):
            temporarySet = spriteSet.copy()
            for object in temporarySet:
                if object.collide(otherObj):
                    if otherObj.getRadius() > 3:
                        Game.game.bubbleBurstGroup.add(Game.Sprite(object.getPosition(), object.getVelocity(), 0, 0, \
                                                     Game.secondBubbleBurstImg, \
                                                     Game.secondBubbleBurstInfo, Game.bubbleBurstSound))

                    else:
                        Game.game.bubbleBurstGroup.add(Game.Sprite(object.getPosition(), object.getVelocity(), 0, 0, \
                                                     Game.bubbleBurstImg, \
                                                     Game.bubbleBurstInfo, Game.bubbleBurstSound))
                    if Game.game.lives <= 1 and otherObj.getRadius() > 30:
                        Game.game.bubbleBurstGroup.add(Game.Sprite(otherObj.getPosition(), otherObj.getVelocity(), 0, 0, \
                                                     Game.submarineCrashImg, \
                                                     Game.submarineCrashInfo, Game.bubbleBurstSound))
                    spriteSet.remove(object)
                    return True
                False

        def collisionBetweenGroups(spriteGroupOne, spriteGroupTwo):
            # Copy sprite groups into temporary variables
            tempGroupOne = spriteGroupOne.copy()
            tempGroupTwo = spriteGroupTwo.copy()

            # Remove object from real group when collision has occurred
            for object in tempGroupOne:
                if Game.Interaction.groupCollision(spriteGroupTwo, object):
                    spriteGroupOne.remove(object)
                    return True
                return False
           
        def draw(self, canvas):
            global lives, backgroundTime, score, bubbleGroup, bubbleBurstGroup, started, difficulty

            # If player dies, reset game
            if len(self.bubbleBurstGroup) == 0 and self.lives <= 0:
                Game.soundtrack.rewind()
                self.bubbleGroup = set([])
                self.started = False

            # Code to make bubble background move
            self.backgroundTime += 1
            wtime = (self.backgroundTime / 4) % Game.WIDTH
            center = Game.backgroundBubblesInfo.getCenter()
            size = Game.backgroundBubblesInfo.getSize()
            canvas.draw_image(Game.underwaterBgImg, Game.underwaterBgInfo.getCenter(), Game.underwaterBgInfo.getSize(), [Game.WIDTH / 2, Game.HEIGHT / 2], [Game.WIDTH, Game.HEIGHT])
            canvas.draw_image(Game.backgroundBubblesImg, center, size, (wtime - Game.WIDTH / 2, Game.HEIGHT / 2), (Game.WIDTH, Game.HEIGHT))
            canvas.draw_image(Game.backgroundBubblesImg, center, size, (wtime + Game.WIDTH / 2, Game.HEIGHT / 2), (Game.WIDTH, Game.HEIGHT))

            # Draw submarine
            Game.theSubmarine.draw(canvas)

            # Update submarine
            Game.theSubmarine.update()

            # Draw the group of sprites and update the group of sprites
            Game.Interaction.handleSpriteGroup(self.bubbleGroup, canvas)
            Game.Interaction.handleSpriteGroup(self.waterBulletsGroup, canvas)
            Game.Interaction.handleSpriteGroup(self.bubbleBurstGroup, canvas)

            # Check to see if there are any collisions
            if Game.Interaction.groupCollision(self.bubbleGroup, Game.theSubmarine) and self.lives > 0:
                Game.game.lives -= 1

            if Game.Interaction.collisionBetweenGroups(self.waterBulletsGroup, self.bubbleGroup):
                Game.game.score += 1
                Game.game.difficulty += .15
                if Game.game.oxygen < 10:
                    Game.game.oxygen += 1
                Game.game.oxygenLose = 100 - (Game.game.score)
                if Game.game.oxygenLose < 70:
                    Game.game.oxygenLose = 70

            if Game.game.oxygen < 4:
                canvas.draw_text("OXYGEN LOW!", [415, 90], 24, "Red")
                if Game.game.alarmCooldown == False:
                    Game.lowOxygenSound.play()
                    Game.game.alarmCooldown = True
                    Game.alarm_cooldown_timer.start()
                    
            
            for i in range(Game.game.oxygen):
                canvas.draw_image(Game.oxygenBubbleImg, Game.oxygenBubbleInfo.getCenter(),
                                Game.oxygenBubbleInfo.getSize(), Game.oxygenMeter[i], [30, 30])
            
            # If the game has not started, the splash screen is drawn
            if not self.started:
                canvas.draw_image(Game.splashScreenImg, Game.splashScreenInfo.getCenter(), 
                                  Game.splashScreenInfo.getSize(), [Game.WIDTH / 2, Game.HEIGHT / 2], 
                                  Game.splashScreenInfo.getSize())

            # Drawing Lives and Score Text
            canvas.draw_text("Lives", [45, 50], 24, "White")
            canvas.draw_text("Score", [875, 50], 24, "White")
            canvas.draw_text("Oxygen:", [455, 25], 24, "White")
            canvas.draw_text(str(self.lives), [45, 80], 24, "White")
            canvas.draw_text(str(self.score), [875, 80], 24, "White")
            
        def oxygenDecrease():
            if Game.game.started:
                if Game.game.oxygenLoseCurrent < Game.game.oxygenLose:
                    Game.game.oxygenLoseCurrent += 1
                else:
                    Game.game.oxygenLoseCurrent = 0
                    if Game.game.oxygen == 0:
                        Game.game.lives -= 1
                        Game.game.oxygen = 10
                    Game.game.oxygen -= 1
                
        def resetAlarm():
            Game.game.alarmCooldown = False
            Game.alarm_cooldown_timer.stop()
    
    # Vector class
    class Vector:
        
        # Initialiser
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        # Returns a tuple with the point corresponding to the vector
        def get_p(self):
            return (self.x, self.y)

        # Adds another vector to this vector
        def add(self, other):
            self.x += other.x
            self.y += other.y
            return self

        def __add__(self, other):
            return self.copy().add(other)

        # Subtracts another vector from this vector
        def subtract(self, other):
            x = self.x - other.x
            y = self.y - other.y
            return self

        def __sub__(self, other):
            return self.copy().subtract(other)

        # Returns the length of the vector
        def length(self):
            return math.sqrt(self.x**2 + self.y**2)

        # Function to determine the calculate distance between two objects
        def calculateDistance(p,q):
            distance = Game.Vector(p.x - q.x, p.y - q.y)
            return distance.length()
            
        # Function to handle transformations
        def convertAngleToVector(ang):
            return Game.Vector(math.cos(ang), math.sin(ang))      

        
    # Mouse handler
    # The game is reset when the splash screen is drawn
    def click(pos):

        center = [Game.WIDTH / 2, Game.HEIGHT / 2]
        size = Game.splashScreenInfo.getSize()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (Game.game.started == False) and inwidth and inheight:
            Game.game.started = True
            Game.game.lives = 3
            Game.game.score = 0
            Game.game.oxygen = 10
            Game.game.difficulty = 0
            Game.soundtrack.play()
            theSubmarine = Game.Player([Game.WIDTH / 2, Game.HEIGHT / 2], [0, 0], 0, \
                                  Game.submarineImg, Game.submarineInfo, Game.submarineEngineSound)
    
    
    """
    Assets for the game
    Credits are given where necessary
    """
    # Splash Screen
    splashScreenInfo = SpriteInfo([500, 375], [1000, 750])
    splashScreenImg = simplegui.load_image("https://i.imgur.com/golt9YC.png")

    # Underwater Background Asset
    # CREDIT: ansimuz @ https://ansimuz.itch.io
    underwaterBgInfo = SpriteInfo([600, 315], [1200, 630])
    underwaterBgImg = simplegui.load_image("https://i.imgur.com/oeQhVQd.png")

    # Bubble Backdrop Asset
    backgroundBubblesInfo = SpriteInfo([320, 240], [640, 480])
    backgroundBubblesImg = simplegui.load_image("https://i.imgur.com/cfv1CpL.png")

    # Submarine Asset
    # CREDIT: Desix @ yoyogames.com
    submarineInfo = SpriteInfo([45, 45], [90, 90], 35)
    submarineImg = simplegui.load_image("https://i.imgur.com/xjsWjIc.png")
    submarineCrashInfo = SpriteInfo([160, 116], [320, 232], 1, 25, True, 5)
    submarineCrashImg = simplegui.load_image("https://i.imgur.com/jKiwLOt.png")

    # Water Bullets Asset
    waterBulletsInfo = SpriteInfo([9,9], [18, 18], 3, 50)
    waterBulletsImg = simplegui.load_image("https://i.imgur.com/PFKbZw7.png")

    # Bubble Asset
    # CREDIT: https://www.dreamstime.com
    bubbleInfo = SpriteInfo([37, 37], [75, 75], 40)
    bubbleImg = simplegui.load_image("https://i.imgur.com/Fccnvd0.png")

    # Bubble Burst Sprite Sheets
    bubbleBurstInfo = SpriteInfo([64, 64], [128, 128], 1, 24, True, 24)
    bubbleBurstImg = simplegui.load_image("https://i.imgur.com/L9GzAN2.png")

    secondBubbleBurstInfo = SpriteInfo([50, 50], [100, 100], 1, 81, True, 9)
    secondBubbleBurstImg = simplegui.load_image("https://i.imgur.com/SE1aa51.png")
    
    oxygenBubbleInfo = SpriteInfo([37, 37], [75, 75], 40)
    oxygenBubbleImg = simplegui.load_image("https://i.imgur.com/n4kEMkT.png")
    
    
    """
    Sound Track Assets
    Credits are given where necessary
    """
    # CREDIT: JuliusH @ https://pixabay.com
    soundtrack = simplegui.load_sound("https://www.mboxdrive.com/magic-pearl.mp3")

    # CREDIT: https://www.zapsplat.com
    waterBulletSound = simplegui.load_sound("https://www.mboxdrive.com/water-bullet.mp3")
    waterBulletSound.set_volume(.5)

    # CREDIT: https://mixkit.co
    submarineEngineSound = simplegui.load_sound("https://www.mboxdrive.com/splash.mp3")
    submarineEngineSound.set_volume(.4)

    # CREDIT: https://mixkit.co
    bubbleBurstSound = simplegui.load_sound("https://www.mboxdrive.com/QKTA234-pop.mp3")
    
    # CREDIT: https://mixkit.co
    lowOxygenSound = simplegui.load_sound("https://www.mboxdrive.com/Ship-alarm.mp3")

    # When the frame is on, the soundtrack will play         
    def frameCheck():
        if Game.frame.get_canvas_textwidth("BubbleBurst", 100) == 0:
            Game.soundtrack.pause()
            Game.frame_timer.stop()

    # Initialisation of the submarine object
    theSubmarine = Player(Vector(WIDTH/2, HEIGHT/2), Vector(0, 0), 0, \
                   submarineImg, submarineInfo, submarineEngineSound)
    
    oxygenMeter = [[365, 50], [395, 50], [425, 50], [455, 50], [485, 50],
                   [515, 50], [545, 50], [575, 50], [605, 50], [635, 50]]

    # Initialising text to add to the frame
    frame = simplegui.create_frame("BubbleBurst", WIDTH, HEIGHT)
    instructionsText = "Instructions:"
    frameTextOne = "Use your keyboard arrows to move the submarine"
    frameTextTwo = "Use the spacebar to shoot bubbles"
    frameTextThree = "Pop bubbles to increase your oxygen. Make sure you don't run out!"
    frameTextFour = "Have fun and thank you for playing!"

    # Adding text to the frame
    frame.add_label(instructionsText, 140)
    frame.add_label("", 140)
    frame.add_label(frameTextOne, 140)
    frame.add_label("", 140)
    frame.add_label(frameTextTwo, 140)
    frame.add_label("", 140)
    frame.add_label(frameTextThree, 140)
    frame.add_label("", 140)
    frame.add_label(frameTextFour, 140)
    
    # Initialising game 
    game = Interaction()

    # Registering the handlers
    frame.set_draw_handler(game.draw)
    frame.set_keydown_handler(lambda key: Game.Player.keyDown(key))
    frame.set_keyup_handler(lambda key: Game.Player.keyUp(key))
    frame.set_mouseclick_handler(click)

    # Timers to spawn the bubbles and pause/play sounds and soundtrack
    timer = simplegui.create_timer(1000.0, Interaction.bubbleSpawner)
    frame_timer = simplegui.create_timer(1000, frameCheck)
    oxygen_timer = simplegui.create_timer(10, Interaction.oxygenDecrease)
    alarm_cooldown_timer = simplegui.create_timer(4000, Interaction.resetAlarm)

    # Starting the frame
    frame.start()
    timer.start()
    frame_timer.start()
    oxygen_timer.start()
