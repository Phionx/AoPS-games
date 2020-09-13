# Python Class 2344
# Lesson 5 Problem 4
# Author: snowapple (471208)

'''
Problem:	Report Error
Using object-oriented programming, write a Python program to play dominoes.

A domino set consists of 28 tiles: each tile has two numbers from 0 to 6, 
and every possible combination appears once. Note that a set includes 7 "double" 
dominoes (from 0-0 through 6-6) and 21 dominos with two different numbers.

The game is for 4 players: each player gets 7 dominoes. The player with the 
double-6 domino goes first and must play it -- that starts the chain. Then, 
in turn, each player must play a domino to add to the chain; the new domino 
can match either end of the chain. For example, if the chain is 1-2,2-6,6-6,6-5, 
then the player can play any domino with a 1 (on the left side of the chain) or 
a 5 (on the right side of the chain). A player who cannot play must pass. The 
player who plays his/her final domino wins; if the game is blocked so that no 
one can play, then the last player who was able to play wins.

Implement the game as a solitaire game with a single human player and three 
computer-controlled opponents. The player should be able to see his/her own 
dominoes, and the entire chain, but naturally cannot see the computer players' dominoes.
'''

import random

class domino:
	def __init__(self, numL,numR): 
		self.numL = numL
		self.numR = numR

	def __str__(self):
		symbols = {0:"   ", 1:" . ", 2:" : ", 3:". :",4:": :",5:".::", 6:":::"}
		return "[" + symbols[self.numL] + "|" + symbols[self.numR] + "]"

	def matches(self, other, side):
		if side == "R":
			if self.numR == other.numL:
				return True
			return False
		elif side == "L":
			if self.numL == other.numR:
				return True
			return False

		return False

	def __eq__(self,other):
		if (self.numL == other.numL  and self.numR == other.numR) or (self.numL == other.numR  and self.numR == other.numL):
			return True
		return False

	def rotate(self):
		temp = self.numL
		self.numL = self.numR
		self.numR = temp
		return self



class dominoDeck:
	def __init__(self):
		self.reset_deck()

	def reset_deck(self):
		self.deck = []
		for i in range(7):
			for j in range(i,7):
				self.deck.append(domino(i,j))

	def remove_domino(self,dom):
		self.deck.remove(dom)

	def __str__(self):
		string = "You have " + str(len(self.deck)) + " domino(es) left in your deck. Here they are: " 
		for i in range(len(self.deck)):
			if i % 6 == 0:
				string += "\n"
			string += str(i) + ": " + str((self.deck[i])) + "\t"
		return string

class dominoPlayer:
	def __init__(self):
		self.reset_player()

	def reset_player(self):
		self.dom_deck = dominoDeck()

	def valid_dominoes(self,domLine, side):
		combo_domino = domLine.ends_combo_domino()
		if len(combo_domino) == 0:
			return self.dom_deck.deck
		combo_domino = combo_domino[0]

		valid_dominoes = []
		for dom in self.dom_deck.deck:
			if combo_domino.matches(dom, side):
				valid_dominoes.append(dom)
			elif combo_domino.matches(dom.rotate(), side):
				valid_dominoes.append(dom)
				dom.rotate()#good practice, but unnecessary

		return valid_dominoes

	def place_dom(self, dom, domLine, side):
		success = domLine.add(dom, side)
		if success:
			self.dom_deck.remove_domino(dom)
		return success

class dominoLine:
	def __init__(self):
		self.reset_line()

	def reset_line(self):
		self.line = []

	def __str__(self):
		string = "(LEFT) "
		for i in range(len(self.line)):
			string += str(self.line[i])
		return string + " (RIGHT)\n"

	def ends_combo_domino(self):
		if len(self.line) == 0:
			return []
		if len(self.line) == 1:
			return [self.line[0]]
		return [domino(self.line[0].numL, self.line[-1].numR)]

	def add(self, dom, side):
		combo_domino = self.ends_combo_domino()
		if len(combo_domino) == 0:
			self.add_line(dom, side)
			return True

		combo_domino = combo_domino[0]
		if combo_domino.matches(dom, side):
			self.add_line(dom, side)
			return True

		dom.rotate()
		if combo_domino.matches(dom, side):
			self.add_line(dom, side)
			return True

		dom.rotate()#rotate back, unnecessary but good practice
		return False

	def add_line(self,dom,side):
		if side == "L":
			self.line.insert(0,dom)
		elif side == "R":
			self.line.append(dom)
		return


def print_array_dominoes(doms):#helper function
	string = "{"
	for dom in doms:
		string += str(dom) +", "
	string += "}"
	print(string)

game = dominoLine()

valid_choice = False
while not valid_choice:
	try:
		num_real_players = abs(int(input('Number of real people playing: ')))
		num_comp_players = abs(int(input('Number of computers playing: ')))
		valid_choice = True
	except ValueError:
		print("Please enter valid integers.")

names = []
for i in range(num_real_players):
	names.append(input('Real player ' + str(i) + ', please enter your name: '))

print("There are " + str(num_comp_players) + " computer players in this game.")

real_players = [dominoPlayer() for i in range(num_real_players)]
comp_players = [dominoPlayer() for i in range(num_comp_players)]

is_won = False 
last_person = ""
while not is_won:
	can_anyone_make_a_move = False

	for i in range(num_real_players):
		print("\n===========================================================")
		print("Here is the current domino line: ")
		print(game)
		print("It's " + names[i] + "'s turn. Calculating valid moves ... ")
		print("-------------------------------------------------------")
		valid_dominoes = {"L": real_players[i].valid_dominoes(game, "L"), "R":real_players[i].valid_dominoes(game, "R")}
		if len(valid_dominoes["L"]) == 0 and len(valid_dominoes["R"]) ==0:
			print("Sorry bud, you don't have any valid moves.")
			continue
		can_anyone_make_a_move = True
		last_person = names[i]
		if input('It seems like you have some valid moves left, do you want to see your valid moves (y/n): ') == 'y':
			print("Valid dominoes to place on the left of the line: ")
			print_array_dominoes(valid_dominoes["L"])
			print("Valid dominoes to place on the right of the line: ")
			print_array_dominoes(valid_dominoes["R"])
			print("-------------------------------------------------------\n")
		
		print("Alright, please pick a valid dominoe from below and where to place it.")
		print(str(real_players[i].dom_deck))
		print("-------------------------------------------------------")
		valid_choice = False
		while not valid_choice:
			try:
				print("Please make a valid choice.")
				num_choices = len(real_players[i].dom_deck.deck)
				domino_choice = int(input('Domino number (0-' + str(num_choices-1) +"): "))
				if 0 > domino_choice or domino_choice >= num_choices:
					raise ValueError
				side_choice = input("Please pick which side you want to add to (L/R): ")
				if side_choice not in ("L","R"):
					raise ValueError
				dom = real_players[i].dom_deck.deck[domino_choice]
				valid_choice = real_players[i].place_dom(dom, game, side_choice)
			except ValueError:
				valid_choice = False
		print("Domino has been placed.")
		print("===========================================================\n")
		if len(real_players[i].dom_deck.deck) == 0:
			is_won = names[i]
			break
		

	for i in range(num_comp_players):
		print("\n===========================================================")
		print("Here is the current domino line: ")
		print(game)
		print("It's Computer " + str(i) + "'s turn. Calculating valid moves ... ")
		valid_dominoes = {"L": comp_players[i].valid_dominoes(game, "L"), "R":comp_players[i].valid_dominoes(game, "R")}
		if len(valid_dominoes["L"]) == 0 and len(valid_dominoes["R"]) ==0:
			print("Sorry bud, you don't have any valid moves.")
			continue
		can_anyone_make_a_move = True
		last_person = "COMP " + str(i)

		if len(valid_dominoes["L"]) == 0:
			side = "R"
		elif len(valid_dominoes["R"]) == 0:
			side = "L"
		else: 
			side = random.choice(["L","R"])
		dom = random.choice(valid_dominoes[side])#Random choice strategy
		print(side)
		print(dom)
		comp_players[i].place_dom(dom, game, side)
		print("Domino has been placed.")
		print("===========================================================\n")
		if len(comp_players[i].dom_deck.deck) == 0:
			is_won = "COMP " + str(i)
			break
		
	if not can_anyone_make_a_move:
		is_won = last_person

print("===========================================================\n")
print(is_won + " won the game.")












