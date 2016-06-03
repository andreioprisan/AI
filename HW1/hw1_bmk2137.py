# Braden Katzman - bmk2137 - Columbia University Summer 2016 (Session 1)
# COMS 4701 Artificial Intelligence
# Professor Ansaf Salled-Aouissi
# HW1 - 8-puzzle solver and evaluations using search algorithms:
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


# global variables
terminal_state_1 = [[1,2,3], [4,5,6], [7,8,0]] # blank in bottom right corner
terminal_state_2 = [[0,1,2], [3,4,5], [6,7,8]] # blank in top left corner




# this class will represent a node for game. The contains the following 4 components:
# - state: the state in the state space to which the node corresponds -> the worldy instance of the board i.e. configuration
# - parent: the node in the search tree that generated this node 
# - action: the action (tile shift) that was applied to the parent to generate the node
# - path_cost: the cost of the path from the initial state to the node (indicated by parent pointers)
class Eight_Puzzle_Node:

	
	# params: n, the dimension of the n x n puzzle to be generated
	def __init__(self, n):
		self.n = n
		self.parent = None
		self.state = [] # the configuration of the board

		# populate the board by looping through the terminal_state configuration and filling each tile
		for i in range(self.n):
			self.state.append(terminal_state_1[i][:])


	def set_parent_node(self, p):
		self.parent = p

	# finds the coordiantes of the target value
	def index_of(self, target):
		for i in range(self.n):
			for j in range(self.n):
				if target == self.state[i][j]:
					return i,j

		return -1

	# shuffles the board which is by default configured to the terminal_state
	def shuffle_board(self):
		i,j = self.index_of(0)

		print i,j


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

def main():
	puzzle = Eight_Puzzle_Node(3)
	puzzle.print_board()
	puzzle.shuffle_board()



if __name__ == "__main__":
    main()
