# Braden Katzman - bmk2137 - Columbia University Summer 2016 (Session 1)
# COMS 4701 Artificial Intelligence
# Professor Ansaf Salled-Aouissi
# HW1 - N-puzzle solver and evaluations using search algorithms:
#	- Breadth-First Search
#	- Depth-First Search
#	- A* Search
#	- Iterative Deepening A* Search
#
# All code implemented was written solely by Braden Katzman. The following resources aided
# me in the completion of this assignment:
# - Artificial Intelligence: A Modern Approach (3rd Edition) - pg: 71, 
# - https://n-puzzle-solver.appspot.com/ (used to conceptualize problem)
# 


# imports
import time
import random
import pdb

# global variables
easy_3x3 = [[1,2,3],[4,5,6],[0,7,8]]
hw_example = [[1,2,5],[3,4,0],[6,7,8]]


# this class represents a node in the N-puzzle game tree. A single contains the following components:
# - state: the state in the state space to which the node corresponds -> the worldy instance of the board i.e. configuration
# - parent: the node in the search tree that generated this node 
# - action: the action (tile shift) that was applied to the parent to generate the node
# - path_cost: the cost of the path from the initial state to the node (indicated by parent pointers)
# - children: the successor (child nodes) that represent legal state changes from this state
class N_Puzzle_Node:


	def generate_terminal_states(self):
		terminal_state_1 = []
		terminal_state_2 = []

		row1 = []
		row2 = []

		counter1 = 0
		counter2 = 1
		for i in range(self.n):
			for j in range(self.n):
				if i == self.n-1 and j == self.n-1:
					row1.append(counter1)
					row2.append(0)
				else:
					row1.append(counter1)
					row2.append(counter2)

				counter1 += 1
				counter2 += 1

			# append the rows to the state configurations
			terminal_state_1.append(row1)
			terminal_state_2.append(row2)
			row1 = []
			row2 = []


		# set the states to class wide variables
		self.terminal_state_1 = terminal_state_1
		self.terminal_state_2 = terminal_state_2
		return

	# params: n, the dimension of the n x n puzzle to be generated
	def __init__(self, n, parent):
		self.n = n
		self.generate_terminal_states() # generate the two terminal states given the dimensions of the board
		
		if parent is None:
			self.parent = None
			self.path_cost = 0
		else:
			self.parent = parent
			self.path_cost = parent.path_cost + 1 # the depth of this state in the game tree

		self.successors = [] # the list of legal successors (child nodes) of this state
		self.state = [] # the configuration of the board

		# populate the board by looping through the terminal_state configuration and filling each tile
		for i in range(self.n):
			self.state.append(self.terminal_state_2[i][:])

	# replaces the current state configuration with the passed state (called by generate_copy())
	def replace_state(self, state):
		if state is not None and len(self.state) == len(state):
			for i in range(self.n):
				for j in range(self.n):
					self.state[i][j] = state[i][j]


	def generate_successor(self, action):
		if action == "UP":
			successor = self.generate_copy()

			# find the blank tile in the successor
			i, j = successor.indices_of(0)

			# swap the blank with the tile directly above
			successor.swap_tiles(i, j, i-1, j)

		elif action == "DOWN":
			successor = self.generate_copy()

			i, j = successor.indices_of(0)

			# swap the blank with the tile directly below
			successor.swap_tiles(i, j, i+1, j)

		elif action == "LEFT":
			successor = self.generate_copy()

			i, j = successor.indices_of(0)

			# swap the blank with the tile directly to the left
			successor.swap_tiles(i, j, i, j-1)

		elif action == "RIGHT":
			successor = self.generate_copy()

			i, j = successor.indices_of(0)

			# swap the blank with the tile directly to the right
			successor.swap_tiles(i, j, i, j+1)

		return successor

	def add_successor(self, successor):
		if successor is not None:
			self.successors.append(successor)

	def is_terminal_state(self):
		return self.state == self.terminal_state_1 or self.state == self.terminal_state_2

	# finds the coordiantes of the target value
	def indices_of(self, target):
		for i in range(self.n):
			for j in range(self.n):
				if target == self.state[i][j]:
					return i,j

		return -1

	# swaps two tiles on the board
	# params:
	#	- a: the row index of the first value
	#	- b: the col index of the first value
	#	- c: the row index of the second value
	#	- d: the col index of the second value
	def swap_tiles(self, a, b, c, d):
		# temporarily save the first value
		temp = self.state[a][b]

		# write the second value to the location of the first
		self.state[a][b] = self.state[c][d]

		# write the temp valie to the origin second value location
		self.state[c][d] = temp

		return

	# generate a copy of the current node (only the board configuration) to build an action i.e. moving the blank tile
	def generate_copy(self):
		# generate a new node
		new_node = N_Puzzle_Node(self.n, self)
			
		# replace the default state config with the configuration of the current node
		new_node.replace_state(self.state)

		return new_node

	# class which generates all successors (child nodes) that represent legal state changes from the current state
	# abstract: this class generates all child nodes of the current node in the tree
	def generate_successors(self):
		# first find the indices
		i,j = self.indices_of(0)

		# make sure the blank is on the board
		if i != -1:

			# in a case when the blank isn't on a border, all actions are available (UP, DOWN, LEFT, RIGHT)
			if (i < self.n-1 and j < self.n-1) and (i > 0 and j > 0):
				return [self.generate_successor("UP"), self.generate_successor("DOWN"), self.generate_successor("LEFT"), self.generate_successor("RIGHT")]
			else:
				# determine which border(s) the blank tile is on to rule an that action
				if i == 0 and j == 0: # top left corner
					return [self.generate_successor("DOWN"), self.generate_successor("RIGHT")]

				elif i == 0 and j == self.n-1: # top right corner
					return [self.generate_successor("DOWN"), self.generate_successor("LEFT")]

				elif i == self.n-1 and j == 0: # bottom left corner
					return [self.generate_successor("UP"), self.generate_successor("RIGHT")]

				elif i == self.n-1 and j == self.n-1: # bottom right corner
					return [self.generate_successor("UP"), self.generate_successor("LEFT")]

				elif i == 0 and (j > 0 and j < self.n-1): # top border (not corners)
					return [self.generate_successor("DOWN"), self.generate_successor("LEFT"), self.generate_successor("RIGHT")]

				elif i == self.n-1 and (j > 0 and j < self.n-1): # bottom border (not corners)
					return [self.generate_successor("UP"), self.generate_successor("LEFT"), self.generate_successor("RIGHT")]		

				elif (i > 0 and i < self.n-1) and j == 0: # left border (not corners)
					return [self.generate_successor("UP"), self.generate_successor("DOWN"), self.generate_successor("RIGHT")]

				elif (i > 0 and i < self.n-1) and j == self.n-1: # right border (not corners)
					return [self.generate_successor("UP"), self.generate_successor("DOWN"), self.generate_successor("LEFT")]

	# shuffles the board which is by default configured to the terminal_state
	def shuffle_board(self):
		# initialize a 1D list to hold the board elements
		temp = []

		# add the elements to the list
		for i in range(self.n):
			for j in range(self.n):
				temp.append(self.state[i][j])

		# shuffle the list
		random.shuffle(temp)

		# add the shuffled elements to a 2D list
		shuffled_state = []
		row = []
		iterator = 0
		for i in range(len(temp)):

			# if the length of a row hasn't been reached, append the next value
			if iterator < self.n:
				row.append(temp[i])
			
			# append the row to the new state configuration and start the next row
			else:
				shuffled_state.append(row)
				iterator = 0
				row = []
				row.append(temp[i])

			iterator += 1

		# append the final row
		shuffled_state.append(row)

		# set the state to the shuffled configuration
		self.state = shuffled_state
		return

	def board_to_list(self):
		l = []
		for i in range(self.n):
			for j in range(self.n):
				l.append(self.state[i][j])
		return l

	def board_to_string(self):
		return str(self.state)


	def print_board(self):
		board = ""
		
		# loop through the rows
		for i in range(self.n):
			board += "[ "

			# loop through the columns
			for j in range(self.n):
				board += str(self.state[i][j]) + " "

			board += "]\n"

		print board
		return

	def print_path(self):
		child = self
		parent = child.parent

		while parent is not None:
			child.print_board()
			print "   ^"
			print "   |"
			print "   |"
			child = parent
			parent = child.parent

		child.print_board()





########### END CLASS OBJECT #################

def isEmpty(l):
	return len(l) < 1

def bfs(n):
	# pdb.set_trace()
	bfs_puzzle = N_Puzzle_Node(n, None)
	# bfs_puzzle.shuffle_board()
	bfs_puzzle.replace_state(hw_example)


	if bfs_puzzle.is_terminal_state():
		return bfs_puzzle

	print "\nInitial configuration"
	bfs_puzzle.print_board()
	print "******\n"

	# create a set to track visited nodes
	visited_nodes = set()

	# create a queue to keep track of fringe (?)
	queue = []
	queue.append(bfs_puzzle)


	while True:
		if isEmpty(queue):
			return None
		
		# choose the shallowest node in frontier
		node = queue.pop(0)
		
		# mark the node as visited
		visited_nodes.add(node.board_to_string())

		# iterate over legal moves
		for s in node.generate_successors():
			# is child has not be visited and is not in the frontier
			if s.board_to_string() not in visited_nodes and s not in queue:
				# check if node is terminal state
				if s.is_terminal_state():
					return s
				
				# insert the child at the end of the fronteir
				queue.append(s)
				
	print "returning without solution"

def dfs(n):
	dfs_puzzle = N_Puzzle_Node(n, None)
	dfs_puzzle.replace_state(easy_3x3)
	# dfs_puzzle.shuffle_board()

	if dfs_puzzle.is_terminal_state():
		return dfs_puzzle

	print "\nInitial configuration"
	dfs_puzzle.print_board()
	print "******\n"

	visited_nodes = set()

	stack = []
	stack.append(dfs_puzzle)

	while True:
		if isEmpty(stack):
			return None

		node = stack[len(stack)-1]

		visited_nodes.add(node.board_to_string())

		for s in node.generate_successors():
			# is child has not be visited and is not in the frontier
			if s.board_to_string() not in visited_nodes and s not in stack:
				# check if node is terminal state
				if s.is_terminal_state():
					return s
				
				# insert the child at the end of the fronteir
				stack.append(s)

def A_star(n):


def debug():
	puzzle = N_Puzzle_Node(3)
	puzzle.print_board()
	print puzzle.is_terminal_state()
	puzzle.generate_successors()
	
	puzzle.shuffle_board()
	puzzle.print_board()
	print puzzle.is_terminal_state()
	puzzle.generate_successors()
	return

def main():
	print "\nstart"
	start_time = time.time()

	# debug()
	n1 = dfs(3)
	n1.print_path()




	print "\nprogram execution = {t} seconds".format(t=(time.time()-start_time))
	print "exiting...\n"



if __name__ == "__main__":
    main()
