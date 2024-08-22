from deap import base, creator, tools, algorithms
from plotting import *
import random
import numpy as np

POPULATION_SIZE = 300  # Population size
P_CROSSOVER = 0.9  # Crossover probability
P_MUTATION = 0.2  # Mutation probability
MAX_GENERATIONS = 500  # Maximum number of generations
HALL_OF_FAME_SIZE = int(POPULATION_SIZE * 0.1)  # Hall of Fame size
TIME_STEPS = 290   # Number of time steps
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Coordinates of the starting and ending points
START_X, START_Y, START_THETA, START_PHI = 5, 5, 0, 0
GOAL_X, GOAL_Y = 5, 95

# Create classes to describe the optimization problem
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize fitness function
creator.create("Individual", list, fitness=creator.FitnessMin)  # Define an individual

toolbox = base.Toolbox()

# Function to generate random speed values for the left and right wheels
def random_u():
    return random.random(), random.random()

# Register the necessary functions in the toolbox
toolbox.register("attr_float", random_u)
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.attr_float, n=TIME_STEPS)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

MAX_PHI_RAD = np.pi / 2  # Maximum turning radius
# List of obstacles: [(x1, y1, x2, y2), ...]
WALLS = [
    (0, 99, 100, 100),
    (0, 1, 1, 99),
    (0, 0, 100, 1),
    (99, 1, 100, 99)
]

OBSTACLES = [
    (56, 1, 62, 12),
    (1, 30, 22, 36),
    (22, 30, 28, 42),
    (28, 36, 40, 42),
    (64, 38, 70, 60),
    (70, 38, 99, 44),
    (36, 58, 42, 72),
    (30, 72, 46, 78),
    (72, 76, 80, 99)
]

# Function to check collisions with obstacles
def check_collision(x, y, obstacles):
    return any(
        x_min - 2 <= x <= x_max + 2 and y_min - 2 <= y <= y_max + 2 for (x_min, y_min, x_max, y_max) in obstacles)

# Fitness function
def fitnessFunc(individual):
    trajectory = calculate_trajectory(individual, START_X, START_Y, START_THETA, START_PHI)
    total_distance = np.sum(np.sqrt(np.diff(trajectory[:, 0]) ** 2 + np.diff(trajectory[:, 1]) ** 2))
    for x, y, theta, phi in trajectory:
        if abs(phi) > MAX_PHI_RAD or check_collision(x, y, WALLS) or check_collision(x, y, OBSTACLES):
            return float("inf"),  # Return infinity for minimization
    # Calculate penalty for distance from the goal
    final_x, final_y = trajectory[-1, 0], trajectory[-1, 1]
    goal_penalty = np.sqrt((final_x - GOAL_X) ** 2 + (final_y - GOAL_Y) ** 2)
    fitness = 1000 * goal_penalty + total_distance

    return fitness,

# Mutation function with Gaussian mutation and shrinking
def mutGaussianAndShrink(individual, sigma, indpb, shrink_prob):
    if random.random() < shrink_prob and len(individual) > 1:
        individual.pop()
    else:
        for i in range(len(individual)):
            if random.random() < indpb:
                left_wheel, right_wheel = individual[i]
                left_wheel = np.clip(left_wheel + random.gauss(0, sigma), 0, 1)
                right_wheel = np.clip(right_wheel + random.gauss(0, sigma), 0, 1)
                individual[i] = (left_wheel, right_wheel)
    return individual,

# One-point crossover function with possible shrinking of offspring
def cxOnePointShrink(ind1, ind2):
    size = min(len(ind1), len(len(ind2)))
    if size > 1:
        cxpoint = random.randint(1, size - 1)
        child1 = ind1[:cxpoint] + ind2[cxpoint:size]
        child2 = ind2[:cxpoint] + ind1[cxpoint:size]
    else:
        child1, child2 = toolbox.clone(ind1), toolbox.clone(ind2)
    return creator.Individual(child1), creator.Individual(child2)

# Register genetic algorithm operations in the toolbox
toolbox.register("evaluate", fitnessFunc)
toolbox.register("mate", cxOnePointShrink)
toolbox.register("mutate", mutGaussianAndShrink, sigma=0.1, indpb=0.2, shrink_prob=0.01)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    plot_trajectories(population, "Initial Population Trajectories", START_X, START_Y, GOAL_X, GOAL_Y)
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    for gen in range(MAX_GENERATIONS):
        offspring = toolbox.select(population, len(population) - HALL_OF_FAME_SIZE)
        offspring = algorithms.varAnd(offspring, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION)
        elite_clones = list(map(toolbox.clone, tools.selBest(population, HALL_OF_FAME_SIZE)))
        offspring.extend(elite_clones)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        population[:] = offspring
        hof.update(population)
        record = stats.compile(population)
        print(f"Generation {gen}, Statistics: {record}")
        best_ind = tools.selBest(population, 1)[0]
    plot_best_trajectory(best_ind, "Best Trajectory", START_X, START_Y, START_THETA, START_PHI, GOAL_X, GOAL_Y)
    print("Best Individual:", best_ind)
    print("Best Fitness:", best_ind.fitness.values[0])

if __name__ == "__main__":
    main()