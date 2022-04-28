import copy
import random


class GeneticAlgorithm:
    def __init__(self, max_queens):
        self.max_queens = max_queens
        self.my_board = []
        for a in range(64):
            self.my_board.append(0)

    def get_queen_board(self):
        return self.my_board

    def get_random_board(self, random_board):
        y = self.max_queens
        for c in range(64):
            random_board.append(0)
        for a in range(y):
            z = random.randint(0, 63)
            if random_board[z] == 1:
                for j in range(64):
                    set_value = (z + j) % 64
                    if random_board[set_value] == 0:
                        random_board[set_value] = 1
                        break
            else:
                random_board[z] = 1

    @staticmethod
    def get_mutated_board(mut_board):
        y = random.randint(0, 63)
        if mut_board[y] == 0:
            mut_board[y] = 1
            a = y + 1
            for b in range(64):
                if mut_board[(b + a) % 64] == 1:
                    mut_board[(b + a) % 64] = 0
                    break
        else:
            mut_board[y] = 0
            a = y + 1
            for b in range(64):
                if mut_board[(b + a) % 64] == 0:
                    mut_board[(b + a) % 64] = 1
                    break

    def get_crossover(self, cross_board):
        queens = cross_board.count(1)
        if queens > self.max_queens:
            # remove queens
            a = 0
            while queens != self.max_queens:
                random_num = random.randint(0, 63)
                if cross_board[random_num] == 1:
                    cross_board[random_num] = 0
                    queens -= 1
                a += 1
        elif queens < self.max_queens:
            # add queens
            a = 0
            while queens != self.max_queens:
                random_num = random.randint(0, 63)
                if cross_board[random_num] == 0:
                    cross_board[random_num] = 1
                    queens += 1
                a += 1

    @staticmethod
    def get_diagonals(matrix):
        n = len(matrix)
        diagonals_1 = []  # lower-left-to-upper-right diagonals
        diagonals_2 = []  # upper-left-to-lower-right diagonals
        for p in range(2 * n - 1):
            diagonals_1.append([matrix[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
            diagonals_2.append([matrix[n - p + q - 1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
        return diagonals_1, diagonals_2

    def get_fitness(self, board):
        count = 0
        hor_board = []
        for a in range(8):
            # horizontal check
            hor_board.append(board[a * 8: (a + 1) * 8])
            if 1 in hor_board[a]:
                count += hor_board[a].count(1) - 1
            # vertical check
            ver_board = board[a: 57 + a: 8]
            if 1 in ver_board:
                count += ver_board.count(1) - 1
        dia1, dia2 = self.get_diagonals(hor_board)
        for a in range(15):
            if 1 in dia1[a]:
                count += dia1[a].count(1) - 1
            if 1 in dia2[a]:
                count += dia2[a].count(1) - 1
        return count


def print_board(board):
    for a in range(8):
        print(board[a * 8:((a + 1) * 8)])


rand_board = [1, 0, 0, 0, 0, 0, 0, 0,
              0, 1, 0, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 0, 1, 0, 0, 0, 0,
              0, 0, 0, 0, 1, 0, 0, 0,
              0, 0, 0, 0, 0, 1, 0, 0,
              0, 0, 0, 0, 0, 0, 1, 0,
              0, 0, 0, 0, 0, 0, 0, 1]

my_ga = GeneticAlgorithm(8)
population_size = int(1000)
advance_generation = int(200)
mutated_generation = int(400)
crossover_generation = int(400)
max_generations = int(1000)

# generating a random population
n_generation = []
n1_generation = []
for i in range(population_size):
    rand_board = []
    my_ga.get_random_board(rand_board)
    fitness_board = my_ga.get_fitness(rand_board)
    n_generation.append((fitness_board, rand_board))

for counter in range(max_generations):
    n_generation.sort()
    print(f"Best solution in generation {counter} has score: {n_generation[0][0]}")
    if n_generation[0][0] == 0:
        break

    # advancing the best set of population
    n1_generation = n_generation[0:advance_generation]
    # creating crossover genes
    for i in range(crossover_generation):
        board_x = n_generation[random.randint(0, advance_generation)][1]
        board_y = n_generation[random.randint(0, population_size - 1)][1]
        sv = 0
        ev = random.randint(0, 63)
        cross = board_x[sv: ev] + board_y[ev: 64]
        my_ga.get_crossover(cross)
        fitness_board = my_ga.get_fitness(cross)
        n1_generation.append((fitness_board, cross))
    # creating mutated genes
    for i in range(mutated_generation):
        x = random.randint(advance_generation, population_size - 1)
        mutated_board = n_generation[x][1]
        my_ga.get_mutated_board(mutated_board)
        fitness_board = my_ga.get_fitness(mutated_board)
        n1_generation.append((fitness_board, mutated_board))

    n_generation = copy.deepcopy(n1_generation)

print('best board is: ')
print_board(n_generation[0][1])
