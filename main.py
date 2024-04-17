from genetic_algo import genetic_algorithm, voltage_stability_margin, network_defination


# Main function to train the model
def train_genetic_algorithm():
    best_solution = genetic_algorithm()  # Run the genetic algorithm to find the best control settings
    best_fitness = voltage_stability_margin(network_defination(best_solution))
    print("Training Complete...")
    print("Best control settings:", best_solution)
    print("Best VSM:", best_fitness, "%")



if __name__ == "__main__":
    # Run the training
    print("Training in Process....")
    train_genetic_algorithm()