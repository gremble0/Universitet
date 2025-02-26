from itertools import permutations
from common import fitness


def exhaustive_search(city_coordinates: dict[str, list[float]]) -> tuple[str, ...]:
    all_permutations = list(permutations(city_coordinates.keys()))

    best_solution = ()
    best_solution_fitness = float("inf")

    for permutation in all_permutations:
        permutation_fitness = fitness(permutation)

        if permutation_fitness < best_solution_fitness:
            best_solution = permutation
            best_solution_fitness = permutation_fitness

    return best_solution
