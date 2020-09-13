# Python Class 2406
# Lesson 12 Problem 1
# Author: snowapple (471208)

class Game:
	def __init__(self, n):
		'''__init__(n) -> Game
        creates an instance of the Game class'''
		if n% 2 == 0:                               #n has to be odd
			print('Please enter an odd n!')
			raise ValueError
		self.n = n #size of side of board
		self.board = [[0 for x in range(self.n)] for x in range(self.n)] #holds current state of the board, list of columns
		self.is_won = 0#is_won is 0 if game is not won, and 1 or 2 if won by player 1 or 2 respectively
	def __str__(self):
		'''__str__() -> str
        returns a str representation of the current state of the board'''
		ans = ""
	
		print_dict = {0:'. ', 1:'X ', 2:'O '}       #On the board, these numbers represent the pieces
		for i in range(self.n):#row
			row = ""
			for j in range(self.n):#column
				row += print_dict[self.board[j][i]]  #prints the board piece to where the player puts it
			ans = row + "\n" + ans
		title = ""
		for i in range(self.n):
			title += str(i) + " "
		ans = '\n' + title + '\n' +ans 
		return ans

	def clear_board(self):
		'''clear_board() -> none
        clears the board by setting all entries to 0'''
		self.is_won = 0         
		self.board = [[0 for x in range(self.n)] for x in range(self.n)]

	def put(self,player_num,column):#takes care of errors 
		'''put(player_num,column) -> boolean
        puts a piece of type player_num in the specified column, 
        returns boolean which is true if the put was successful, otherwise false'''
		if self.is_won != 0:             #if the game has been won
			print('Please start a new game as player ' + str(self.is_won) + ' has already won!')
			return False
		if player_num not in [1,2]:        #if a valid player number is not entered
			print('Please enter 1 or 2 for the player number!')
			return False
		if column < 0 or column >= self.n:   #if a valid column is not entered
			print('Please enter a valid column!')
			return False                      
		try:
			row = self.board[column].index(0)
			self.board[column][row]= player_num
			self.is_won = self.win_index(column,row) 
			return True
		except ValueError:
			print('Column is full!')
			return False

	def win_index(self,column_index,row_index):
		'''win_index(column_index,row_index) -> int
		checks if piece at (column_index, row_index) is part of a connect 4
		returns player_num if the piece is part of a connect4, and 0 otherwise'''

		#uses axis_check to check all of the axes 
		player_num = self.board[column_index][row_index]
		
		#check up/down axis
		col = self.board[column_index]
		col_win = self.axis_check(col,row_index,player_num)  #checks the row since it goes up/down
		if col_win != 0:      #checks to see if won                       
			return col_win
		#check left/right axis
		row = [self.board[i][row_index] for i in range(self.n)]
		row_win = self.axis_check(row,column_index,player_num)  #checks column since it goes left/right
		if row_win != 0:  #checks to see if won
			return row_win

		#down-left/up-right diagonal axis
		axis = [player_num]
		index = 0

		#down-left part
		curr_col_index = column_index - 1    #goes left so subtract one
		curr_row_index = row_index - 1       #goes down so subtract one
		while curr_row_index >= 0 and curr_col_index >= 0:             #until you go to the most down-left part of the board
			axis =  [self.board[curr_col_index][curr_row_index]] + axis
			curr_col_index -= 1
			curr_row_index -= 1 
			index += 1



		#up-right part
		curr_col_index = column_index + 1 #goes right so add one
		curr_row_index = row_index + 1     #goes up so add one
		while curr_row_index < self.n and curr_col_index < self.n:  #until you go to the most up-right part of the board
			axis = axis +[self.board[curr_col_index][curr_row_index]] 
			curr_col_index += 1
			curr_row_index += 1 
		diag_win = self.axis_check(axis,index,player_num)
		if diag_win != 0:   #checks to see if won
			return diag_win  

		#up-left/down-right diagonal axis
		axis = [player_num]
		index = 0

		
		#up-left part
		curr_col_index = column_index - 1 #goes left so minus one
		curr_row_index = row_index + 1    #goes up so plus one
		while curr_row_index < self.n and curr_col_index >= 0:  #until you go to the most up-left part of the board
			axis =  [self.board[curr_col_index][curr_row_index]] + axis
			curr_col_index -= 1
			curr_row_index += 1 
			index += 1



		#down-right part
		curr_col_index = column_index + 1 #goes right so plus one
		curr_row_index = row_index - 1    # goes down so minus one
		while curr_row_index >= 0 and curr_col_index < self.n:        #until you go to the most down-right part of the board
			axis = axis +[self.board[curr_col_index][curr_row_index]] 
			curr_col_index += 1
			curr_row_index -= 1 
		diag_win = self.axis_check(axis,index,player_num)
		if diag_win != 0:         #checks to see if won
			return diag_win


		return 0
		

	def axis_check(self,axis, index, player_num):
		'''axis_check(axis, index, player_num) -> int
		checks if index in axis (list) is part of a connect4
		returns player_num if the index is indeed part of a connect4 and 0 otherwise'''

		#takes the index and sees if the piece is part of a connect four and generalizes it for the four axes(up/down, left/right, two diagonals)
		down = index
		up = index
		for i in range(index,-1, -1):
			if axis[i] == player_num:
				down = i
			else:
				break
		for i in range(index,len(axis)):
			if axis[i] == player_num:
				up = i
			else:
				break
		
		if up - down + 1 >= 4:
			# print('Player ' + str(player_num) + ' has won the game!')
			return player_num

		return 0


game = Game(7)     
labels = {1:'X', 2:'O'}

play = True

while play:
    #setting up the board and players   
	game.clear_board()
	name1 = input('Player ' + labels[1] + ' , enter your name: ')
	name2 = input('Player ' + labels[2] + ' , enter your name: ')
	names = {1:name1, 2:name2}
	print(game)
	turn = 1
	while game.is_won == 0:   
		success = False
		while not success:
			#until someone wins each player takes turns
			col_choice = int(input(names[turn] + ", you're " + labels[turn] + ". What column do you want to play in? "))
			success = game.put(turn,col_choice)
		print(game)
		turn = turn % 2 +1  #to take turns between players

	print("Congratulations, " + names[game.is_won]+", you won!")
	#if players want to play again	
	play_another = ""
	while play_another not in ['y','n']:
		play_another = input("Do you want to play another game? [Enter 'y' for yes, 'n' for no]: ")

	if play_another == 'n':
		play = False






