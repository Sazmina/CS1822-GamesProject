
import simplegui




# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
        
        
WIDTH = 800
HEIGHT = 600


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
                          
        
        
        

def draw(canvas):
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

Warrior = Classes("Warrior", 3, 2, 3)

Knight = Classes ("Knight", 3, 4, 2)

RedTeamWarrior1 = (Warrior, 10, (0,0))

BlueTeamKnight1 = (Knight, 10, (0,0))

#Replace this image with better graphics
fightButton = simplegui.load_image("https://i.imgur.com/kY7X6UJ.png")
defendButton = simplegui.load_image("https://i.imgur.com/K5TFMgE.png")
battleBackground = simplegui.load_image("https://i.imgur.com/PK0x3nV.png")
skeleton = simplegui.load_image("https://i.imgur.com/EYRg0xO.png")

#Splash screen menu info
buttonInfo = ImageInfo([75, 25], [150, 50])
backgroundInfo = ImageInfo([400, 300], [800, 600])
skeletonInfo = ImageInfo([97.5, 100], [195, 200])
skeletonPos = Vector(200, 200)
fightButPos = Vector(200, 400)
defendButPos = Vector(200, 460)


#END OF TEMPORARY CODE
    
TheMouse = Mouse(Vector(0,0))
FightButton = FightBut(fightButPos, buttonInfo, TheMouse)
DefendButton = DefendBut(defendButPos, buttonInfo, TheMouse)
Skeleton = character(skeletonPos, skeletonInfo, TheMouse)

CurrentTurn = True
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_mouseclick_handler(TheMouse.mouse_handler)
frame.set_draw_handler(draw)
frame.start()
