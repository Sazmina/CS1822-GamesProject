import simplegui

#Constants for the size of the canvas (temporarily set to 800 x 600 - we can change this)
WIDTH = 800
HEIGHT = 600

#This variable indicates whether the game has started
started = False

#This variable stores the position of a mouse click
pos = ""

#This class handles the information of image objects, more attributes will be added as we code more image objects
class ImageInfo:
    def __init__(self, center, size):
        self.center = center
        self.size = size

    def getCenter(self):
        return self.center

    def getSize(self):
        return self.size

#This class stores basic information about characters (Their attack, defence and movement) As these stats do not change between characters of the same type
class Classes:
    def __init__(self, name, attack, defence, movement):
        self.name = name
        #The name of the class (swordsman, archer, king etc.) This is for identifying what sprite should be used for the unit on the map and fight screen (STRING)
        self.attack = attack
        #The attack of the unit, this is used during the fight screen to calculate how much damage is dealt to the opponent (INTEGER)
        self.defence = defence
        #The defence of the unit, this is used during the fight screen to calculate how much damage is blocked (INTEGER)
        self. movement = movement
        #The movement characteristic of the unit, this determines how far the unit can move on the map. Movement is done horizontally and vertically, moving diagonally would cost 2 movement "points" (INTEGER)

    def getclass(self):
        return self.attack, self.defence, self.movement
        #Mainly used by the Character class to get the stats of the unit, as they are stored in the class type

        
class Character:
    def __init__(self, CharacterType, health, position):
        self.CharacterType = CharacterType
        #The class of the unit (OBJECT OF TYPE Classes)
        self.health = health
        #The current health of the unit, if this reaches 0 at any point, the unit must be removed from the game (INTEGER)
        self.position = position
        #The position of the unit on the map, this can either be the number of the square, or the unit's exact vector co-ordinates, it can be decided by whoever designs the map system (TO BE DECIDED)

    def getstats(self):
        Number1, Number2, Number3 = self.CharacterType.getclass()
        return self.health, Number1, Number2, Number3
        #Returns the health, attack, defence and movement of a character, in that order. Will be useful for displaying character's stats on the map and retrieving them for the fight screen
        #If you only need one of these stats specifcally, call the fucntion, store all the other stats in junk variables, and simply use the one you need to refer to
        #If this begins to mess up our code, we can make functions to call specfic stats only

    def move(self, newposition):
        self.position = newposition
        #Updates the character's position on the map, will be fleshed out more as the map and movement is coded

    def fight(self, opponent):
        self.health = self.health
        #I will write this out in more detail when I begin work on the fight screen, for now, do not mind this function, it is simply a placeholder and an indication of how fights will begin

def temp():
    pass

#Order of stats is as follows (ATTACK, DEFENCE, MOVEMENT)
Warrior = Classes("Warrior", 3, 2, 3)

Knight = Classes ("Knight", 3, 4, 2)

King = Classes ("King", 4, 2, 3)
#3 Very basic classes, we can add more variety in the future should we have the time, for now, we can just use these 3 as placeholders

RedTeamWarrior1 = (Warrior, 10, (0,0))
#A basic example of how a character is created, his class is referred to, health is set, and position on the map is set

#Replace this image with better graphics
splashImage = simplegui.load_image("https://i.imgur.com/joIcLFR.png")

#Splash screen menu info
splashInfo = ImageInfo([350, 200], [700, 400])

#Handler for a mouse click
def click(pos):
    global started

    if (not started):
        started = True
    
#Handler to draw on canvas
def draw(canvas):
    global started
    
    if not started:
        # Drawing the splash screen on the canvas
        # When replacing the 
        canvas.draw_image(splashImage, splashInfo.getCenter(), 
                          splashInfo.getSize(), [WIDTH/2, HEIGHT/2], 
                          splashInfo.getSize())

    canvas.draw_text("", [WIDTH/2,HEIGHT/2], 48, "Red")

#Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)

#Register drawing handler
frame.set_draw_handler(draw)

#Register handler for mouse click events 
frame.set_mouseclick_handler(click)

#We will only keep this button if we decide to implement AI
frame.add_button("Play with computer", temp, 140)

#Start the frame animation
frame.start()

#This is not very advanced code, but serves as a good start to the project as the very basics of the character class are defined, these will be added to and further developed later.
#For now, this should be enough to get started, feel free to add to these classes, but remember to add comments on GitHub to explain what you have updated
#I will be starting work on the fight screen when I have the time, this will likely be Friday afternoon and the weekend. Please ask me if there is anything you are confused on
