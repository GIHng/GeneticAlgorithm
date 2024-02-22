import numpy as np
import random

GRID_SIZE = 10
START_POINT = (0, 0)
END_POINT = (GRID_SIZE - 1, GRID_SIZE - 1)
# OBSTACLES = [(5, 5)] # 임의의 장애물 위치
OBSTACLES = [(5, 5), (6, 6), (7, 7)] # 임의의 장애물 위치

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)] # 우, 상, 좌, 하

POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 1000


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
        goal_reached = False

        for move in self.moves:
            next_position = (position[0] + move[0], position[1] + move[1])

            # GRID_SIZE를 벗어나는 이동 제한하기.
            if not (0 <= next_position[0] < GRID_SIZE and 0 <= next_position[1] < GRID_SIZE):
                score -= 50
                continue

            if next_position == END_POINT:
                goal_reached = True
                score += 1000
                break
            
            if next_position in OBSTACLES:
                # print("장애물 걸림")
                score -= 100
            else:
                # 종료 지점에 가까워질수록 더 높은 점수를 부여하기.
                score += max(0, 10 - (abs(END_POINT[0] - next_position[0]) + (abs(END_POINT[1] - next_position[1]))))
            position = next_position
        return score, goal_reached

    def crossover(self, other):
        crossover_point = random.randint(0, len(self.moves) - 1) # 마지막 경로 전.
        child1_moves = self.moves[:crossover_point] + other.moves[crossover_point:]
        child2_moves = other.moves[:crossover_point] + self.moves[crossover_point:]

        return RobotPath(child1_moves), RobotPath(child2_moves)

    def mutate(self):
        # print("돌연변이 발생!!")
        mutation_point = random.randint(0, len(self.moves) - 1)
        self.moves[mutation_point] = random.choice(MOVES)

def tournament_selection(population, tournament_size = 3):
    tournament_group = random.sample(population, tournament_size)

    winner = max(tournament_group, key=lambda member: member.fitness())

    return winner

def is_goal_reached(population, goal=END_POINT):
    for path in population:
        if (path.moves[-1][0], path.moves[-1][1]) == goal:
            return True
    return False

def main():
    population = [RobotPath() for _ in range(POPULATION_SIZE)]

    STAGNATION_LIMIT = 100 # 성능 향상이 없는 세대 수 한계
    STAGNATION_COUNTER = 0 # 성능 향상이 없는 세대 수 카운터

    previous_best_fitness = None  # 이전 최고 적합도 점수
    for generation in range(GENERATIONS):
        # 현재 세대의 적합도 계산
        fitness_values = [path.fitness() for path in population]
        current_best_fitness = max(fitness_values)

        if previous_best_fitness is not None and current_best_fitness <= previous_best_fitness:
            STAGNATION_COUNTER += 1
        else:
            # 성능 향상이 있으면 리셋
            STAGNATION_COUNTER = 0
        previous_best_fitness = current_best_fitness

        # if STAGNATION_COUNTER >= STAGNATION_LIMIT:
        #     print(f"성능 향상 정체 Gen {generation+1} 종료")
        #     break

        if is_goal_reached(population):
            break

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
        fitness_values, goals_reached = zip(*[path.fitness() for path in population])
        
        best_fitness = max(fitness_values)
        print(f"Gen {generation + 1}: Best Fitness = {best_fitness}")

        if any(goals_reached):
            for path, goal_reached in zip(population, goals_reached):
                if goal_reached:
                    print("목표 지점에 도달한 경로:", path.moves)
            print(f"목표 지점 도달 Gen {generation+1} 종료")
            break


if __name__ == "__main__":
    main()