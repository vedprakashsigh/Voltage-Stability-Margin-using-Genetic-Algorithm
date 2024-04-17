import numpy as np
import csv

from network import voltage_stability_margin, network_defination


# Define parameters
population_size = 50
num_generations = 7
mutation_rate = 0.1

# Define fitness function (objective function)
def fitness_function(chromosome):
    # Simulate power system with the given chromosome (control settings)
    # Calculate voltage stability
    return voltage_stability_margin(network_defination(chromosome))

# Generate initial population
def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = np.random.rand() * 100  
        population.append(chromosome)
    return population

# Perform crossover
def crossover(parent1, parent2, alpha=0.5):
    """
    Perform blend crossover (BLX-alpha) between two float parents.
    
    Parameters:
        parent1 (float): First parent.
        parent2 (float): Second parent.
        alpha (float): Blend factor determining the range for offspring generation.
    
    Returns:
        offspring1 (float): Offspring generated from parent1 and parent2.
        offspring2 (float): Offspring generated from parent1 and parent2.
    """
    # Calculate the range for offspring generation
    min_val = min(parent1, parent2) - alpha * abs(parent1 - parent2)
    max_val = max(parent1, parent2) + alpha * abs(parent1 - parent2)
    
    # Generate offspring within the defined range
    offspring1 = np.random.uniform(min_val, max_val)
    offspring2 = np.random.uniform(min_val, max_val)
    
    return offspring1, offspring2

# Perform mutation
def mutate(chromosome):
    # Random mutation of a gene
    if np.random.rand() < mutation_rate:
        chromosome = np.random.rand() * 100
    return chromosome

# Select Parents
def select_parents(population, fitness_values, tournament_size=3):
    selected_parents_indices = []
    
    # Adjust tournament size if it's larger than the population size
    if tournament_size > len(population):
        tournament_size = len(population)
    
    # Perform tournament selection
    while len(selected_parents_indices) < len(population) // 2:
        # Randomly select individuals for the tournament
        tournament_indices = np.random.choice(range(len(population)), size=tournament_size, replace=False)
        
        # Find the index of the individual with the highest fitness in the tournament
        winner_index = tournament_indices[np.argmax([fitness_values[i] for i in tournament_indices])]
        
        # Add the index of the winner to the selected parents
        selected_parents_indices.append(winner_index)
    
    return selected_parents_indices

# Main genetic algorithm function
def genetic_algorithm():
    # Initialization
    population = initialize_population()
    solutions = [["Generation","Voltages"]]
    
    
    # Evolution loop
    for generation in range(num_generations):
        # Evaluate fitness of each individual in the population
        fitness_values = [fitness_function(chromosome) for chromosome in population]
        
        # Select parents for crossover
        selected_parents = select_parents(population, fitness_values)
        
        # Create next generation through crossover and mutation
        new_population = []
        for i in range(0, len(selected_parents)-1, 2):
            parent1 = population[selected_parents[i]]
            parent2 = population[selected_parents[i + 1]]
            offspring1, offspring2 = crossover(parent1, parent2)
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            new_population.extend([offspring1, offspring2])
        
        # Replace the old population with the new generation
        population = new_population
        
        # Update fitness values for the new population
        fitness_values = [fitness_function(chromosome) for chromosome in population]

        if fitness_values:
            idx = np.argmax(fitness_values)
            best_sol = population[idx]
            solutions.append([generation,best_sol])
        else:
            best_sol = None

        print(f"Generation {generation}: Best Solution so far is {best_sol}")

        if best_sol is None:
            # Restart 
            population = initialize_population()

    with open('sol.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(solutions)

    # Return the best solution found
    if fitness_values:
        best_solution_index = np.argmax(fitness_values)
        best_solution = population[best_solution_index]
        return best_solution
    else:
        return solutions[-1][1]  # Return None if no solutions were found


if __name__ == "__main__":
    best_control_settings = genetic_algorithm()
    print("Best control settings:", best_control_settings)
