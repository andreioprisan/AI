# Braden Katzman - bmk2137 - Columbia University Summer 2016 (Session 1)
# COMS W4701 Artificial Intelligence
# Professor Ansaf Salleb-Aouissi
# HW1 - N-puzzle solver and evaluations using search algorithms:
#	- Breadth-First Search
#	- Depth-First Search
#	- A* Search
#	- Iterative Deepening A* Search
#
# All code implemented was written solely by Braden Katzman. The following resources aided
# me in the completion of this assignment:
# - Artificial Intelligence: A Modern Approach (3rd Edition) - pg: 71
# - https://n-puzzle-solver.appspot.com/ (used to conceptualize problem)
# - http://pythonforbiologists.com/index.php/measuring-memory-usage-in-python/ (memory requirements)


# imports
import sys
import time
import random
import pdb
import resource

# GLOBAL VARS
delim = ","

# - tables 
easy_3x3 = [[1,2,5],[3,4,0],[6,7,8]]
hard_3x3 = [[0,8,7],[6,5,4],[3,2,1]]

hw_example = [[1,2,5],[3,4,0],[6,7,8]]
piazza_example = [[1,4,2],[3,7,5],[6,0,8]]

# - strings
_bfs = "Breadth-First Search"
_dfs = "Depth-First Search"
_a_star = "A* Search"
_id_a_star = "Iterative Deepening A*"

# **** END GLOBAL VARS


# this class represents a node in the N-puzzle game tree. A single node contains the following components:
# - n: the dimension of the board
# - state: the state in the state space to which the node corresponds -> the worldy instance of the board i.e. configuration
# - parent: the node in the search tree that generated this node 
# - depth: depth = the cost of the path from the initial state to the node (indicated by parent pointers)
# - children: the successor (child nodes) that represent legal state changes from this state
# - heuristic_function_value: h(n) for this configuration (only used by A* and Iterative Deepening A*)

class N_Puzzle_Node:

	# generates the two end states (o bottom right, 0 top left) based on the nxn dimensions
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
	def __init__(self, n):
		self.n = n
		self.generate_terminal_states() # generate the two terminal states given the dimensions of the board

		self.parent = None
		self.depth = 0
		self.heuristic_function_value = 0

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
		return

	# finds the coordiantes of the target value
	def indices_of(self, target):
		for i in range(self.n):
			for j in range(self.n):
				if target == self.state[i][j]:
					return i,j

		return -1

	# returns the value at the specified row (i) and column (j)
	def value_at(self, i, j):
		return self.state[i][j]


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
		new_node = N_Puzzle_Node(self.n)

		# set the parent and the path cost
		new_node.parent = self
		new_node.depth = new_node.parent.depth + 1
			
		# replace the default state config with the configuration of the current node
		new_node.replace_state(self.state)

		return new_node

	# generates a single successor node given an action. Clones the original node and swaps tiles
	# based on the given action UP, DOWN, LEFT, RIGHT
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

		# print action
		# successor.print_board()
		return successor

	# method which generates all successors (child nodes) that represent legal state changes from the current state
	# abstract: this class generates all child nodes of the current node in the tree
	def generate_successors(self):
		# first find the indices
		i,j = self.indices_of(0)
		# self.print_board()

		# make sure the blank is on the board
		if i != -1:

			# in a case when the blank isn't on a border, all actions are available (UP, DOWN, LEFT, RIGHT)
			if (i < self.n-1 and j < self.n-1) and (i > 0 and j > 0):
				# print "all actions"
				return [self.generate_successor("RIGHT"), self.generate_successor("LEFT"), self.generate_successor("DOWN"), self.generate_successor("UP")]
			else:
				# determine which border(s) the blank tile is on to rule an that action
				if i == 0 and j == 0: # top left corner
					# print "down and right"
					return [ self.generate_successor("RIGHT"), self.generate_successor("DOWN")]

				elif i == 0 and j == self.n-1: # top right corner
					# print "down and left"
					return [self.generate_successor("LEFT"), self.generate_successor("DOWN")]

				elif i == self.n-1 and j == 0: # bottom left corner
					# print "up and right"
					return [self.generate_successor("RIGHT"), self.generate_successor("UP")]

				elif i == self.n-1 and j == self.n-1: # bottom right corner
					# print "up and left"
					return [self.generate_successor("LEFT"), self.generate_successor("UP")]

				elif i == 0 and (j > 0 and j < self.n-1): # top border (not corners)
					# print "down left right"
					return [ self.generate_successor("RIGHT"), self.generate_successor("LEFT"), self.generate_successor("DOWN")]

				elif i == self.n-1 and (j > 0 and j < self.n-1): # bottom border (not corners)
					# print "up left right"
					return [self.generate_successor("RIGHT"),  self.generate_successor("LEFT"), self.generate_successor("UP")]	

				elif (i > 0 and i < self.n-1) and j == 0: # left border (not corners)
					# print "up down right"
					return [self.generate_successor("RIGHT"), self.generate_successor("DOWN"), self.generate_successor("UP")]

				elif (i > 0 and i < self.n-1) and j == self.n-1: # right border (not corners)
					# print "up down left"
					return [self.generate_successor("LEFT"), self.generate_successor("DOWN"), self.generate_successor("UP")]


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

	# returns True if node's board configuration is equal to a terminal state, False otherwise
	def is_terminal_state(self):
		# concatenate each tile as a string to a list
		state_list = []
		for i in self.state:
			for j in i:
				state_list += [str(j)]

		terminal_state_1_list = []
		for k in self.terminal_state_1:
			for m in k:
				terminal_state_1_list += [str(m)]

		terminal_state_2_list = []
		for k in self.terminal_state_2:
			for m in k:
				terminal_state_2_list += [str(m)]

		# convert the lists to strings and compare them
		return ''.join(state_list) == ''.join(terminal_state_1_list) or ''.join(state_list) == ''.join(terminal_state_2_list)

	# a list representation of the configuration of the board
	def board_to_list(self):
		l = []
		for i in range(self.n):
			for j in range(self.n):
				l.append(self.state[i][j])
		return l

	# a string representation of the board for optimization on searching
	def board_to_string(self):
		state_list = []
		for i in self.state:
			for j in i:
				state_list += [str(j)]

		return ''.join(state_list)

	# print the board configured like a nxn table
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

	def find_action(self, child):
		i, j = self.indices_of(0)

		k, l = child.indices_of(0)

		if k != i: # k,i are rows, so difference means UP or DOWN action
			if k > i:
				return "DOWN"
			else:
				return "UP"
		elif l != j: # l, j are cols, so difference means LEFT or RIGHT
			if l > j:
				return "RIGHT"
			else:
				return "LEFT"

	def results(self, search_algorithm, nodes_expanded, running_time):
		child = self
		parent = child.parent


		solution_path = []
		cost_of_path = 0
		depth_of_db = 0
		while parent is not None:
			solution_path.insert(0, parent.find_action(child))
			# move up a node
			child = parent
			parent = child.parent

			# increment cost counter
			cost_of_path += 1

			# increment depth_counter
			depth_of_db += 1

		# add the root node level to the depth counter
		depth_of_db += 1

		print "***** Results for {search_algorithm} on {n}x{n} puzzle *****".format(search_algorithm=search_algorithm, n=self.n)
		print " - Solution: {solution}".format(solution=str(solution_path))
		print " - Cost of Path = {cost_of_path}".format(cost_of_path=cost_of_path)
		print " - # Nodes Expanded = {num_nodes}".format(num_nodes=nodes_expanded)
		print " - Max depth of stack/queue = {max_depth}".format(max_depth=depth_of_db)
		print " - Memory Requirements = {mem_requirements} mb".format(mem_requirements=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)) # SEE SLIDE 9 and 14 TUES LECTURE FOR GENERAL VIEW
		print " - Running Time = {running_time}".format(running_time=running_time)


	# print the path from the current node to the root
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
def containsState(l, elem):
	if l is None or elem is None:
		return False

	elem_list = []
	for i in elem.state:
		for j in i:
			elem_list += [str(j)]


	for item in l:
		item_list = []
		for k in item.state:
			for m in k:
				item_list += [str(m)]

		if ''.join(elem_list) == ''.join(item_list):
			return True

	return False

def isEmpty(l):
	return len(l) < 1

def bfs(start):
	# pdb.set_trace()
	# node.shuffle_board()

	if start.is_terminal_state():
		return start

	print "\nInitial configuration"
	start.print_board()
	print "******\n"

	# create a running sum of visited nodes as string with delim
	nodes_expanded = 0
	visited_nodes = ""

	# create a queue to keep track of fringe nodes
	queue = []
	queue.append(start)

	while True:
		if isEmpty(queue):
			return None
		
		# choose the shallowest node in fringe
		node = queue.pop(0)
		
		# mark the node as visited
		visited_nodes += (node.board_to_string() + delim)
		nodes_expanded += 1

		# iterate over legal moves
		for s in node.generate_successors():
			# is child has not be visited and is not in the frontier
			if visited_nodes.find(s.board_to_string()) == -1 and containsState(queue, s) is False:
				# check if node is terminal state
				if s.is_terminal_state():
					return s, nodes_expanded
				else:
					# insert the child at the end of the fronteir
					queue.append(s)
			else:
				del s

def dfs(start):
	# pdb.set_trace()
	# start.shuffle_board()

	if start.is_terminal_state():
		return start

	print "\nInitial configuration"
	start.print_board()
	print "******\n"

	nodes_expanded = 0
	visited_nodes = ""

	stack = []
	stack.append(start)

	while True:
		if isEmpty(stack):
			return None

		node = stack.pop()

		visited_nodes += (node.board_to_string() + delim)
		nodes_expanded += 1

		for s in node.generate_successors():
			# if child has not be visited and is not in the frontier
			if visited_nodes.find(s.board_to_string()) == -1 and containsState(stack, s) is False:
				# check if node is terminal state
				if s.is_terminal_state():
					return s, nodes_expanded
				else:
					stack.append(s)
			else:
				del s

# A* using Manhattan Distance heuristic
def A_star(start):
	# pdb.set_trace()
	# start.shuffle_board()

	if start.is_terminal_state():
		return start

	print "\nInitial configuration"
	start.print_board()
	print "******\n"

	nodes_expanded = 0
	visited_nodes = []

	fringe = []
	fringe.append(start)

	while True:
		if isEmpty(fringe):
			return None

		# always pop the front node --> the node with the lowest f(n)
		node = fringe.pop(0)

		# check if goal state
		if node.is_terminal_state():
			return node, nodes_expanded

		# increment nodes_expanded counter
		nodes_expanded += 1

		for s in node.generate_successors():
			# calculate the heuristic function value for this node using manhattan distance
			heuristic_function_value = manhattan_distance_heuristic(s)

			# f(n) = g(n) + h(n) --> estimated cost of the cheapest solution through n
			# g(n) = the path cost from the state node to n
			# h(n) = heuristic function value i.e. estimated cost of the cheapest path from n to goal
			f_of_n = s.depth + heuristic_function_value

			# if the moves is totally unseen, set its heuristic value and add it to the fringe
			if containsState(visited_nodes, s) is False and containsState(fringe, s) is False:
				s.heuristic_function_value = heuristic_function_value
				fringe.append(s)

			# else if the move is unvisited but resides in the fringe, see if this has better heuristic value
			elif containsState(visited_nodes, s) is False and containsState(fringe, s) is True:
				for n in fringe:
					if n.state == s.state:
						# check if improved f(n)
						if f_of_n < (n.depth + n.heuristic_function_value):
							# update the node
							n.parent = node
							n.depth = n.parent.depth + 1
							n.heuristic_function_value = heuristic_function_value

			# else if the move is visited and therefore not in the fringe
			elif containsState(visited_nodes, s) is True and containsState(fringe, s) is False:
				for n in visited_nodes:
					if n.state == s.state:
						if f_of_n < (n.depth + n.heuristic_function_value):
							# update the heuristic function value
							s.heuristic_function_value = heuristic_function_value

							# remove the node from the list of visited and place back in fringe
							visited_nodes.remove(n)
							fringe.append(n)

		# append the node to the list of visisted nodes
		visited_nodes.append(node)

		# sort the fringe to next pop the value with the smallest f(n)
		fringe = sorted(fringe, key=lambda x: x.depth + x.heuristic_function_value)

	print "returning without solution :("
	return None

# Iterative Deepening A* using Manhattan Distance heuristic
def ID_A_star(start):
	# pdb.set_trace()
	# start.shuffle_board()
	current_limit = 0

	print "\nInitial configuration"
	start.print_board()
	print "******\n"

	nodes_expanded = 0
	visited_nodes = []

	fringe = []
	fringe.append(start)

	while True:
		if isEmpty(fringe):
			return None

		# always pop the front node --> the node with the lowest f(n)
		node = fringe.pop(0)

		# check if goal state
		if node.is_terminal_state():
			return node, nodes_expanded

		# only generate the next layer if below the current limit
		if node.depth < current_limit:
			# increment nodes_expanded counter
			nodes_expanded += 1

			for s in node.generate_successors():
				# calculate the heuristic function value for this node using manhattan distance
				heuristic_function_value = manhattan_distance_heuristic(s)

				# f(n) = g(n) + h(n) --> estimated cost of the cheapest solution through n
				# g(n) = the path cost from the state node to n
				# h(n) = heuristic function value i.e. estimated cost of the cheapest path from n to goal
				f_of_n = s.depth + heuristic_function_value

				# if the moves is totally unseen, set its heuristic value and add it to the fringe
				if containsState(visited_nodes, s) is False and containsState(fringe, s) is False:
					s.heuristic_function_value = heuristic_function_value
					fringe.append(s)

				# else if the move is unvisited but resides in the fringe, see if this has better heuristic value
				elif containsState(visited_nodes, s) is False and containsState(fringe, s) is True:
					for n in fringe:
						if n.state == s.state:
							# check if improved f(n)
							if f_of_n < (n.depth + n.heuristic_function_value):
								# update the node
								n.parent = node
								n.depth = n.parent.depth + 1
								n.heuristic_function_value = heuristic_function_value

				# else if the move is visited and therefore not in the fringe
				elif containsState(visited_nodes, s) is True and containsState(fringe, s) is False:
					for n in visited_nodes:
						if n.state == s.state:
							if f_of_n < (n.depth + n.heuristic_function_value):
								# update the heuristic function value
								s.heuristic_function_value = heuristic_function_value

								# remove the node from the list of visited and place back in fringe
								visited_nodes.remove(n)
								fringe.append(n)

			# append the node to the list of visisted nodes
			visited_nodes.append(node)

			# sort the fringe to next pop the value with the smallest f(n)
			fringe = sorted(fringe, key=lambda x: x.depth + x.heuristic_function_value)

		# if the current limit has been reached
		else:
			# check if there are still items in the fringe
			if isEmpty(fringe):
				# increase the current_limit and add the root node
				current_limit += 1
				fringe.append(start)
				del visited_nodes[:]
				nodes_expanded = 0
				# print current_limit

	print "returning without solution :("
	return None

# This heuristic sums the number of rows away from the target row with the number of columns
# away from the target column for every tile on the board
def manhattan_distance_heuristic(node):
	# for each tile, find the row and coordinate in the goal state and compute the distance
	# keep a running total of the distances from each tile to their goal position and use this total as heuristic function value

	total_distance = 0
	for i in range(node.n):
		for j in range(node.n):
			# get the current value at the coordinates
			value = node.value_at(i, j)

			# check if the value is the blank tile --> 0
			if value == 0:
				goal_row = goal_col = node.n-1

			else:
				# the goal row corresponds to value -1 divided by the n dimension
				# e.g. value = 1 --> goal location is i = 0/n = 0, j = 0%n = 0
				goal_row = (value-1) / node.n

				# the goal column corresponds to value modulus the n dimension
				goal_col = (value-1) % node.n

			# find the distance between the current location and goal location (absolute value)
			distance = abs(goal_row - i) + abs(goal_col - j)

			# add to sum of distances
			total_distance += distance

	# return the heuristic function value
	return total_distance

def main():
	print "\nstart"
	start_time = time.time()

	if len(sys.argv) != 2:
		print "Usage: python <hw1_bmk2137.py> <search alg: bfs, dfs, a*, id_a*>"
	else:
		n = len(hw_example) # *************** CHANGE THE TABLE INSTANCE HERE : Lines 27-31 *************
		node = N_Puzzle_Node(n) # *************** CHANGE THE TABLE INSTANCE HERE if the dimensions change *************
		node.replace_state(hw_example) # *************** CHANGE THE TABLE INSTANCE HERE : Lines 27-31 *************

		search_algorithm = sys.argv[1]
		if search_algorithm.lower() == "dfs":
			search_algorithm = _dfs
			goal, nodes_expanded = dfs(node)
		elif search_algorithm.lower() == "bfs":
			search_algorithm = _bfs
			goal, nodes_expanded = bfs(node)
		elif search_algorithm.lower() == "a*":
			search_algorithm = _a_star
			goal, nodes_expanded = A_star(node)
		elif search_algorithm.lower() == "id_a*":
			search_algorithm = _id_a_star
			goal, nodes_expanded = ID_A_star(node)

	running_time = time.time()-start_time
	if goal is not None:
		goal.print_path()
		goal.results(search_algorithm, nodes_expanded, running_time)

	print "\ntotal program execution = {t} seconds".format(t=(time.time()-start_time))
	print "exiting...\n"

if __name__ == "__main__":
    main()