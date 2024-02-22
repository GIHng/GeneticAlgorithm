import numpy as np
import random

GRID_SIZE = 100
START_POINT = (0, 0)
END_POINT = (GRID_SIZE - 1, GRID_SIZE - 1)
OBSTACLES = [(5, 5), (6, 6), (7, 7)] # 임의의 장애물 위치

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)] # 상, 하, 좌, 우

POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 100

class RobotPath:
    def __init__(self, moves = None):
        if moves is None:
            self.moves = self.random_path()
        else:
            self.moves = moves

    def random_path(self):
        return [random.choice(MOVES) for _ in range(GRID_SIZE * 2)]
    
    def fitness(self):
        position = START_POINT
        score = 0

        for move in self.random_path():
            next_position = (position[0] + move[0], position[1] + move[1])

            if next_position == END_POINT:
                score += 1000
                break
            
            if next_position in OBSTACLES:
                score -= 100
            else:
                score += 1
            position = next_position
        return score

    def crossover(self, other):
        crossover_point = random.randint(0, len(self.moves) - 1) # 마지막 경로 전.
        child1_moves = self.moves[:crossover_point] + other.moves[crossover_point:]
        child2_moves = other.moves[:crossover_point] + self.moves[crossover_point:]

        return RobotPath(child1_moves), RobotPath(child2_moves)

    def mutate(self):
        mutation_point = random.randint(0, len(self.moves) - 1)
        self.moves[mutation_point] = random.choice(MOVES)

def select(population):
    selected = []

    for _ in range(POPULATION_SIZE // 2):
        individual1 = random.choice(population)
        individual2 = random.choice(population)

        selected.append(individual1 if individual1.fitness() > individual2.fitness() else individual2)
    
    return selected

def main():
    population = [RobotPath() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        fitness_values = [path.fitness() for path in population]

        selected = select(population)

        children = []

        for _ in range(len(population) // 2):
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)

            child1, child2 = parent1.crossover(parent2)

            children.extend([child1, child2])

        for child in children:
            if random.random() < MUTATION_RATE:
                child.mutate()

        population = children

        best_fitness = max(fitness_values)
        print(f"Gen {generation + 1}: Best Fitness = {best_fitness}")


if __name__ == "__main__":
    main()