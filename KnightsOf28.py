import simplegui

#Importing the vector class
from user305_o32FtUyCKk_0 import Vector

#Constants for the size of the canvas (temporarily set to 800 x 600 - we can change this)
WIDTH = 800
HEIGHT = 600

#This variable indicates whether the game has started
started = False

#This variable stores the position of a mouse click
pos = ""

#Boolean variables to store status of gameplay
mapScene = False
fightScene = False

#Boolean for fight scene
CurrentTurn = True

#This class handles the information of image objects, more attributes will be added as we code more image objects
class ImageInfo:
    def __init__(self, center, size):
        self.center = center
        self.size = size

    def getCenter(self):
        return self.center

    def getSize(self):
        return self.size
    
class Mouse:
    
    def __init__(self, lastpos):
        self.lastpos = None
   
    def mouse_handler(self, positionmouse):
        global started

        if (not started):
            started = True
            startGame()
            
        self.lastpos = positionmouse
        
    def click_pos(self):  
        newpos = self.lastpos
        self.lastpos = None
        return newpos

class FightBut:
    
    def __init__(self, fightButPos, buttonInfo, TheMouse):
        self.position = fightButPos
        self.info = buttonInfo
        self.Mouse = TheMouse
        
    def updatePos(self, newpos):
        self.position = Vector(newpos[0], newpos[1])
    
    
    def checkClick(self, canvas):
        currentclick = TheMouse.click_pos()
        if currentclick != None:
            if ((currentclick[0]  >= (self.position.x - 75)) and (currentclick[0] <= (self.position.x + 75))
                and (currentclick[1] <= self.position.y + 25) and (currentclick[1] >= self.position.y - 25)):
                Skeleton.setjump()
                
            else:
                self.position = Vector(200,400)

class DefendBut:
    
    def __init__(self, defendButPos, buttonInfo, TheMouse):
        self.position = defendButPos
        self.info = buttonInfo
        self.Mouse = TheMouse
        
    def updatePos(self, newpos):
        self.position = Vector(newpos[0], newpos[1])
    
    
    def checkClick(self):
        currentclick = TheMouse.click_pos()
        if currentclick != None:
            if (currentclick[0]  >= (self.position.x - 75)  and currentclick[0] <= (self.position.x + 75)
                and currentclick[1] >= (self.position.y - 25) and currentclick[1] <= (self.position.x + 25)):
                self.position = Vector(500, 400)

                
            else:
                self.position = Vector(200, 400)         
                
class character:
    
    def __init__(self, initialPos, Info, TheMouse):
        self.position = initialPos
        self.info = Info
        self.Mouse = TheMouse
        self.jumping = False
        self.jumpswitch = False
        self.jump = Vector(0,0)
        
    def setjump(self):
        self.jump = Vector(0, -15)
        self.jumping = True
        
    def action(self):
        self.position.add(self.jump)
        if self.jump.y == 0:
            self.jumpswitch = True
        if self.jump.y == 15:
            self.jumpswitch = False
            self.jumping = False
            return None
        elif self.jump.y < 0 and self.jumpswitch == False:
            self.jump.add(Vector(0, 1))
        if self.jumpswitch == True and self.jump.y < 15:
            self.jump.add(Vector(0, 1))
                          
#THIS IS SO THE CODE MAY RUN SEPERATELY, THIS SHOULD BE DELETED WHEN THIS SYSTEM IS IMPLEMENTED
class Classes:
    def __init__(self, name, attack, defence, movement):
        self.name = name
        self.attack = attack
        self.defence = defence
        self. movement = movement


    def getclass(self):
        return self.attack, self.defence, self.movement
        
class Character:
    def __init__(self, CharacterType, health, position):
        self.CharacterType = CharacterType
        self.health = health
        self.position = position

    def getstats(self):
        Number1, Number2, Number3 = self.CharacterType.getclass()
        return self.health, Number1, Number2, Number3

    def move(self, newposition):
        self.position = newposition

    def fight(self, opponent):
        self.health = self.health
        
def startGame():
    global mapScene
    global fightScene
    
    mapScene = True
        
#Character objects
Warrior = Classes("Warrior", 3, 2, 3)
Knight = Classes ("Knight", 3, 4, 2)
RedTeamWarrior1 = (Warrior, 10, (0,0))
BlueTeamKnight1 = (Knight, 10, (0,0))

#Menu assets
splashImage = simplegui.load_image("https://i.imgur.com/tNLif1i.png")

#Map assets
mapImage = simplegui.load_image("https://i.imgur.com/9uWJd6D.png")

#Fight screen assets
fightButton = simplegui.load_image("https://i.imgur.com/kY7X6UJ.png")
defendButton = simplegui.load_image("https://i.imgur.com/K5TFMgE.png")
battleBackground = simplegui.load_image("https://i.imgur.com/PK0x3nV.png")
skeleton = simplegui.load_image("https://i.imgur.com/EYRg0xO.png")

#Image information of image objects
buttonInfo = ImageInfo([75, 25], [150, 50])
backgroundInfo = ImageInfo([400, 300], [800, 600])
skeletonInfo = ImageInfo([97.5, 100], [195, 200])
splashInfo = ImageInfo([400, 300], [800, 600])
mapInfo = ImageInfo([400, 300], [800, 600])

#Initialising positions
skeletonPos = Vector(200, 200)
fightButPos = Vector(200, 400)
defendButPos = Vector(200, 460)

#Create mouse object
TheMouse = Mouse(Vector(0,0))

#Handler to draw on canvas
def draw(canvas):
    global started
    global mapScene
    global fightScene
    
    if (not started):
        # Drawing the splash screen on the canvas
        canvas.draw_image(splashImage, splashInfo.getCenter(), 
                          splashInfo.getSize(), [WIDTH/2, HEIGHT/2], 
                          splashInfo.getSize())

    if mapScene == True:
        canvas.draw_image(mapImage, mapInfo.getCenter(), 
                          mapInfo.getSize(), [WIDTH/2, HEIGHT/2], 
                          mapInfo.getSize())
        
    if fightScene == True:
        if CurrentTurn == True:
            DefendButton.updatePos([200, 460])
        else:
            FightButton.updatePos([600, 400])
            FightButton.updatePos([600, 460])

        if Skeleton.jumping == True:
            Skeleton.action()

        canvas.draw_image(battleBackground, backgroundInfo.getCenter(),
                          backgroundInfo.getSize(), (WIDTH/2, HEIGHT/2),
                          backgroundInfo.getSize())
        canvas.draw_image(fightButton, buttonInfo.getCenter(), 
                          buttonInfo.getSize(), (FightButton.position.x, FightButton.position.y),
                          buttonInfo.getSize())
        canvas.draw_image(defendButton, buttonInfo.getCenter(), 
                          buttonInfo.getSize(), (DefendButton.position.x, DefendButton.position.y),
                          buttonInfo.getSize())
        canvas.draw_image(skeleton, skeletonInfo.getCenter(), 
                          skeletonInfo.getSize(), (Skeleton.position.x, Skeleton.position.y),
                          skeletonInfo.getSize())
        FightButton.checkClick(canvas)
        DefendButton.checkClick()

#Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)

#Register drawing handler
frame.set_draw_handler(draw)

#Register handler for mouse click events 
frame.set_mouseclick_handler(TheMouse.mouse_handler)

#Start the frame animation
frame.start()
