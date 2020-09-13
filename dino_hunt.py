# Python Class 2344
# Lesson 6 Problem 5
# Author: snowapple (471208)

import random

### Die class that we previously wrote ###

class Die:
    '''Die class'''

    def __init__(self,sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides,int):
            self.numSides = sides
            self.sides = list(range(1,sides+1))
        else:  # use the list/tuple provided 
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+' die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value

### end Die class ###

class DinoDie(Die):
    '''implements one die for Dino Hunt'''
    ### you need to add the code ###
    def __init__(self,color,sides):
        Die.__init__(self)
        self.color = color
        self.side_labels = sides #{1:"leaves", 2:"leaves"}
        

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+ self.color +' Dino die with a '+\
               str(self.get_top_label())+' on top.'

    def get_top_label(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.side_labels[self.top]


class DinoPlayer:
    '''implements a player of Dino Hunt'''
    def __init__(self, name):
        self.name = name
        self.points = 0

    def __str__(self):
        return str(self.name) + ' has ' + str(self.points) + ' points.'
class DinoGame:
    def __init__(self):
        self.reset()

    def reset(self):
        greenSides = {1:'dinosaur', 2:'dinosaur', 3:'dinosaur', 4: 'leaf', 5: 'leaf', 6: 'foot'}
        yellowSides = {1:'dinosaur', 2:'dinosaur', 3:'foot', 4: 'leaf', 5: 'leaf', 6: 'foot'}
        redSides = {1:'dinosaur', 2:'foot', 3:'foot', 4: 'leaf', 5: 'leaf', 6: 'foot'}
        self.dice = []
        for _ in range(6):
            self.dice.append(DinoDie('green', greenSides))
        for _ in range(4):
            self.dice.append(DinoDie('yellow', yellowSides))
        for _ in range(3):
            self.dice.append(DinoDie('red', redSides))

    def __str__(self):
        message = "You have " + str(len(self.dice)) + " dice"
        message += "\nGreen: " + str(len([die for die in self.dice if die.color == "green"]))
        message += ", Yellow: " + str(len([die for die in self.dice if die.color == "yellow"]))
        message += ", Red: " + str( len([die for die in self.dice if die.color == "red"]))
        return message

    def select(self):
        numDice = list(range(len(self.dice)))

        if len(numDice) < 3:
            dice2roll = numDice
        else:
            dice2roll = random.sample(numDice, 3)
        results = []
        for die in dice2roll:
            self.dice[die].roll()
            print(self.dice[die])
            results.append(self.dice[die].get_top_label())

        dinos = 0
        feet = 0
        for i in range(len(dice2roll)):
            if results[i] == 'dinosaur':
                dinos += 1
                self.dice.pop(dice2roll[i])
            elif results[i] == 'foot':
                feet += 1
                self.dice.pop(dice2roll[i])

        return dinos, feet

def play_dino_hunt(numPlayers,numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
    players = []
    for i in range(numPlayers):
        players.append(DinoPlayer(input("Player "+str(i)+', enter your name: ')))
    turn = DinoGame()
    for i in range(numRounds):
        print('=====================================================================')
        print("ROUND "+ str(i))
        for player in players:
            print(player.name + " has "+ str(player.points)+ " points.")
        print("")
        for player in players:
            print("------------------------------------------------")
            print(player.name +", it's your turn!")
            #turn starts
            turn.reset()
            currPoints = 0
            currFeet = 0
            firstTurn = True
            while True:
                print(turn)
                if firstTurn:
                    input("Please enter to select dice and roll.")
                    firstTurn = False
                else:
                    continueAns = input("Please enter 'y' if you wish to continue rolling: ") 
                    if continueAns != 'y':
                        break
                dinos, feet = turn.select()
                currFeet += feet
                currPoints += dinos
                if currFeet >= 3:
                    currPoints = 0
                    print("Too bad -- you got stomped!")
                    break 
                elif len(turn.dice) == 0:
                    print("No more dice remaining!")
                    break
                print("This turn so far: " + str(currPoints) + " dinos and " + str(currFeet) + " feet.")
            player.points += currPoints
    endPoints = [player.points for player in players]
    maxPoint = max(endPoints)
    winners = []
    for player in players:
        if player.points == maxPoint:
            winners.append(player)

    if len(winners) == 1:
        print("We have a winner!")
        print(str(player.name) +" won with " + str(player.points) + " points!")
    else:
        print("It was a tie..")
        for player in winners:
            print(str(player.name) +" tied with " + str(player.points) + " points.")
    return

while True:
    try:
        numPlayers = int(input("How many players? "))
        break
    except ValueError:
        print("Please enter a valid number.")

while True:
    try:
        numRounds = int(input("How many rounds? "))
        break
    except ValueError:
        print("Please enter a valid number.")

play_dino_hunt(numPlayers,numRounds)
