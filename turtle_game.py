# Python Class 2344
# Lesson 7 Problem 5 Part (b)
# Author: snowapple (471208)

import turtle

class SuperAwesomeTurtle(turtle.Turtle):  #SuperAwesomeTurle is a subclass of turtle.Turtle and inherits all of its methods
    '''a super awesome turtle!'''
    
    def __init__(self):
        '''SuperAwesomeTurtle() -> Turtle
        creates a turtle that moves with the given speed and angle'''
        turtle.Turtle.__init__(self)
        self.speed = 25
        self.angle = 0
        # listeners for keypress
        self.getscreen().onkey(self.increase, 'i')
        self.getscreen().onkey(self.decrease, 'k')
        self.getscreen().onkey(self.stop, 's')
        self.getscreen().onkey(self.close, 'q')
        self.getscreen().onkey(self.turnLeft, 'j')
        self.getscreen().onkey(self.turnRight, 'l')
        self.move()

    def move(self):
        '''SuperAwesomeTurtle.move()
        tells the turtle to move at a
        certain speed and angle'''
        self.forward(self.speed/25)#tells the turtle how much to move forward
        self.left(self.angle)#tells the turle how much to turn
        self.angle = 0#sets the angle back to 0
        self.getscreen().ontimer(self.move, 40)

    def increase(self):
        '''SuperAwesomeTurtle.increase()
        increases the speed by 25 units/second'''
        self.speed += 25

    def decrease(self):
        '''SuperAwesomeTurtle.decrease()
        decreases the speed by 25 units/second'''
        self.speed -= 25

    def stop(self):
        '''SuperAwesomeTurtle.stop()
        stops the turtle from moving by setting the speed to zero'''
        self.speed = 0

    def close(self):
        '''SuperAwesomeTurtle.close()
        closes the window and ends the program'''
        self.getscreen().bye()

    def turnLeft(self):
        '''SuperAwesomeTurtle.turnLeft()
        makes the turtle turn left by changing the angle to 90'''
        self.angle = 90

    def turnRight(self):
        '''SuperAwesomeTurtle.turnRight()
        makes the turtle turn right by changing the angle to -90'''
        self.angle = -90
        


wn = turtle.Screen()
pete = SuperAwesomeTurtle()
wn.listen()
wn.mainloop()
