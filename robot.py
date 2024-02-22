import numpy as np
import random

GRID_SIZE = 10
START_POINT = (0, 0)
END_POINT = (GRID_SIZE - 1, GRID_SIZE - 1)
OBSTACLES = [(5, 5)] # 임의의 장애물 위치
# OBSTACLES = [(5, 5), (6, 6), (7, 7)] # 임의의 장애물 위치

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
        # END_POINT까지 이동하기 위한 최소이동횟수 설정.
        path_length = 2 * (GRID_SIZE - 1)
        return [random.choice(MOVES) for _ in range(path_length)]
    
    def fitness(self):
        position = START_POINT
        score = 0

        for move in self.moves:
            next_position = (position[0] + move[0], position[1] + move[1])

            # GRID_SIZE를 벗어나는 이동 제한하기.
            if not (0 <= next_position[0] < GRID_SIZE and 0 <= next_position[1] < GRID_SIZE):
                score -= 50
                continue

            if next_position == END_POINT:
                score += 1000
                break
            
            if next_position in OBSTACLES:
                # print("장애물 걸림")
                score -= 100
            else:
                # 종료 지점에 가까워질수록 더 높은 점수를 부여하기.
                score += max(0, 10 - (abs(END_POINT[0] - next_position[0]) + (abs(END_POINT[1] - next_position[1]))))
            position = next_position
        return score

    def crossover(self, other):
        crossover_point = random.randint(0, len(self.moves) - 1) # 마지막 경로 전.
        child1_moves = self.moves[:crossover_point] + other.moves[crossover_point:]
        child2_moves = other.moves[:crossover_point] + self.moves[crossover_point:]

        return RobotPath(child1_moves), RobotPath(child2_moves)

    def mutate(self):
        # print("돌연변이 발생!!")
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
        # 현재 세대의 적합도 계산

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

        # 인구를 자식 세대로 갱신
        population = children

        # 갱신된 인구에 대해 적합도 다시 계산
        fitness_values = [path.fitness() for path in population]
        best_fitness = max(fitness_values)
        print(f"Gen {generation + 1}: Best Fitness = {best_fitness}")


if __name__ == "__main__":
    main()