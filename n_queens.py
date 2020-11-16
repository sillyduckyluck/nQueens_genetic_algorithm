"""
Sasha Niehorster-Cook
NQueens Genetic Algorithm Application
2/27/17
"""

import random
import collections
from collections import Counter

"""
you can change the variables of the program here, including the nxn board size, the number of survivors (non-culled) per
generation, the population size, and how many generations the program will iterate through before a reset.
"""

board_size = 14
number_of_survivors = 900
population_size = 5000
generations_before_reset = 60
mutation_percent_chance = 10

class Population():
    def __init__(self, population):
        self.size = population_size
        self.population = []
        self.basket = {}

        i = 0
        if population == None:
            while i < self.size:
                self.population.append(NQueensBoard(board_size, None, None))
                i += 1
        else:
            self.population = population
        i = 0

        while i < self.size:
            self.basket[self.population[i]] = self.population[i].fitness
            i += 1

        max = 0
        min = 100
        for nqueenboard in self.population:
            if nqueenboard.fitness > max:
                self.best_board = nqueenboard
                max = nqueenboard.fitness
            elif nqueenboard.fitness < min:
                self.worst_board = nqueenboard
                min = nqueenboard.fitness


    def next_generation(self):
        survivors = []
        self.basket = dict(Counter(self.basket).most_common(number_of_survivors))
        for key in self.basket:
            survivors.append(key)
            #survivors.append(key.fitness)
        self.population = []
        while len(self.population) < self.size:
            father_random_indexer = random.randint(0, len(survivors) - 1)
            mother_random_indexer = random.randint(0, len(survivors) - 1)
            father = survivors[father_random_indexer]
            mother = survivors[mother_random_indexer]
            self.population.append(NQueensBoard(board_size, father, mother))
        return Population(self.population)



class NQueensBoard():
    def __init__(self, size, father, mother):
        self.size = size
        self.board = [] * size
        if mother != None:
            self.board = self.breed_board(father, mother)
        else:
            self.board = self.generate_random_board()
        self.clashes = self.fitness_function()
        self.fitness = 100 - self.clashes #this makes the fitness positive so it's easier for the program to track. Just
        #the amount of clashes vs an arbitrary value


    def fitness_function(self):
        """
        Takes a board and returns how fit it is. The fitness is determined by how many queens attack each other. I

        """
        clashes = 0  #Number of clashes initialized to 0, then we figure out how many row, diagonal, and column clashes there are
        clashes += self.row_column_clashes()
        clashes += self.diagonal_clashes()
        return clashes

    def diagonal_clashes(self):
        """
        diagonal clashes are a bit harder to calculate, but it's still not that hard- simply calculate the change in x
        and the change in y from the file (x) and height(y). If that value is equal, then the slope is 1 and it means
        the queens are diagonal to one another. At the end, divide by 2 to keep the program from counting the same
        queens attacking each other twice.
        """
        diagonal_clashes = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if (i != j):
                    dx = abs(i-j)
                    dy = abs(self.board[i] - self.board[j])
                    if(dx == dy):
                        diagonal_clashes += 1
        return diagonal_clashes / 2

    def row_column_clashes(self):
        """
        Returns the number of clashes in the rows and columns of a board. Simple to calculate- you just want the number
        of unique values in the list. If there are two queens in the same row, they will be attacking each other and the
        values will be nonunique.
        """

        row_col_clashes = abs(len(self.board) - self.num_unique(self.board))
        return row_col_clashes

    def num_unique(self, a_list):
        """
        Takes a list and returns the number of unique values in that list
        """
        return len(set(a_list))

    def generate_random_board(self):
        """

        """
        i = 0
        while i < self.size:
            self.board.append(random.randint(1, self.size))
            i += 1
        return self.board

    def breed_board(self, father, mother):
        """
        takes two boards and returns their child. The child is made by splitting the father and mother at a random point
        k and using 0-k from the father and k-board_size from the mother. The mutation also occurs here- for every
        inhereted value there is a 2.5% chance of it increasing and a 2.5% chance of it decreasing.
        :param father: the father board
        :param mother: the mother board
        :return: child board
        """
        k = random.randint(0,self.size)

        i = 0
        child = []
        while i < k:
            roll = random.randint(0,100)
            if roll == 1 or roll == 0:
                if father.board[i] == board_size:
                    child.append(father.board[i] - 1)
                else:
                    child.append(father.board[i] + 1)

            elif roll == 2 or roll == 3:
                if father.board[i] == 1:
                    child.append(father.board[i] + 1)
                else:
                    child.append(father.board[i] - 1)
            else:
                child.append(father.board[i])
            i += 1

        while i < self.size:
            roll = random.randint(0,100)
            if roll == 1 or roll == 0 or roll == 3 or roll ==4 or roll == 5:
                if mother.board[i] == board_size:
                    child.append(mother.board[i] - 1)
                else:
                    child.append(mother.board[i] + 1)
            elif roll == 6 or roll == 7 or roll == 8 or roll == 9 or roll ==10:
                if mother.board[i] == 1:
                    child.append(mother.board[i] + 1)
                else:
                    child.append(mother.board[i] - 1)
            else:
                child.append(mother.board[i])
            i += 1
        return child

    def goal_test(self):
        if self.clashes == 0:
            return True



def main():

    y = Population(None)

    exit = False
    generation = 0
    restarts = 0


    while exit == False:
        avg_fitness = 0
        for nqueenboard in y.population:
            avg_fitness += nqueenboard.clashes
            if nqueenboard.goal_test():
                exit = True
                print("ANSWER:", nqueenboard.board)


        #prints the relevant statistics for this generation
        print("AVG FITNESS: ", avg_fitness / y.size, "| ", "GENERATION: ", generation, "| ",
              "BEST BOARD: ", y.best_board.board,  "FITNESS: ", y.best_board.fitness_function(), "| ",
              "WORST BOARD: ", y.worst_board.board, "FITNESS: ", y.worst_board.fitness_function())

        y = y.next_generation()
        generation += 1

        #I had a problem that the fitness values would converge but never find an answer, so I implemented another
        #technique discussed in the textbook- restarts. After there are a certain amount of generations the population
        #will be reset and randomly generated to start over again.
        if generation == generations_before_reset:
            generation = 0
            restarts += 1
            print("RESTART NUM: ", restarts)
            y = Population(None)


main()