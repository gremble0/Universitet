import random
from common import fitness


def genetic_algorithm(
    city_coordinates: dict[str, list[float]],
    population_size: int = 100,
    num_generations: int = 500,
) -> tuple[str, ...]:
    # generate population_size random solutions
    cities = list(city_coordinates.keys())
    population = dict(map(lambda solution: (solution, fitness(solution)),
                 [tuple(random.sample(cities, len(cities))) for _ in range(population_size)]))
    
    for _ in range(num_generations):
        new_gen = dict(population) # copy the dict for temporary changes

        for solution in population:
            new_solution = mutate(solution)
            # this could be optimized by adding weights on who to crossover with
            new_solution = crossover(new_solution, random.choice(tuple(population.keys())))

            # no reason to handle this solution if we already have it
            if new_solution in new_gen:
                continue

            new_gen[new_solution] = fitness(new_solution)

        # sort by fitness, and set the population to the fittest solutions
        # this is not particularly smart - pretty much just pure exploitation.
        population = dict(sorted(new_gen.items(), key=lambda x: x[1])[:len(population)])

    return tuple(population.keys())[0]


def mutate(
    solution: tuple[str, ...],
    mutation_rate: float = 0.1
) -> tuple[str, ...]:
    new_solution = list(solution)
    for _ in range(int(len(solution) * mutation_rate)):
        idx1, idx2 = random.sample(range(len(solution)), 2)
        new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]

    return tuple(new_solution)


def crossover(
    solution1: tuple[str, ...],
    solution2: tuple[str, ...]
) -> tuple[str, ...]:
    split_index = random.randint(0, len(solution1) - 1)
    solution_builder = list(solution1[:split_index])
    for city in solution2:
        if city not in solution_builder:
            solution_builder.append(city)

    return tuple(solution_builder)


def genetic_algorithm_with_debug(
    city_coordinates: dict[str, list[float]],
    population_size: int = 100,
    num_generations: int = 500,
) -> tuple[tuple[str, ...], list[float]]:
    """Same as genetic_algorithm, just also keeping track of some debugging
       information requested by the assignment"""
    cities = list(city_coordinates.keys())
    population = dict(map(lambda solution: (solution, fitness(solution)),
                 [tuple(random.sample(cities, len(cities))) for _ in range(population_size)]))

    best_fitnesses: list[float] = []
    
    for _ in range(num_generations):
        new_gen = dict(population)

        for solution in population:
            new_solution = mutate(solution)
            new_solution = crossover(new_solution, random.choice(tuple(population.keys())))

            if new_solution in new_gen:
                continue

            new_gen[new_solution] = fitness(new_solution)

        population = dict(sorted(new_gen.items(), key=lambda x: x[1])[:len(population)])
        best_fitnesses.append(tuple(population.values())[0])

    return tuple(population.keys())[0], best_fitnesses
