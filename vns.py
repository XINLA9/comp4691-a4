import random
import firefighter
import neighbours

if __name__ == '__main__':
    # Load the initial schedule from example.sched
    initial_schedule = firefighter.load_schedule("example.sched")

    prob = firefighter.SchedulingProblem()
    costs = firefighter.read_costs(prob)

    # Define neighbourhoods
    neighborhoods = [neighbours.SwapNeighbourhood(prob)]

    # Initialize current solution
    current_solution = initial_schedule
    current_cost = prob.cost(current_solution, costs)
    print(f"initial cost is {current_cost}")

    # Define your VNS parameters
    max_iterations_without_improvement = 100  # Maximum number of iterations without improvement
    kmax = len(neighborhoods)  # Number of neighborhoods

    # Initiate VNS parameters
    iterations_without_improvement = 0
    k = 1

    while k <= kmax:
        # Choose the k-th neighbourhood
        neighborhood = neighborhoods[k - 1]
        print(type(neighborhood))

        # Generate neighbors using the selected neighbourhood
        neighbors = neighborhood.neighbours(current_solution)

        # Evaluate the neighbors and find the best one
        best_neighbor = None
        best_neighbor_cost = current_cost

        for neighbor in neighbors:
            neighbor_cost = prob.cost(neighbor, costs)
            if neighbor_cost < best_neighbor_cost:
                best_neighbor = neighbor
                best_neighbor_cost = neighbor_cost

        # If a better neighbor is found, update the current solution and reset k
        if best_neighbor is not None and best_neighbor_cost < current_cost:
            current_solution = best_neighbor
            current_cost = best_neighbor_cost
            k = 1

        else:
            k += 1

            # Increment iterations_without_improvement if no better neighbor is found
            if best_neighbor is None or best_neighbor_cost >= current_cost:
                iterations_without_improvement += 1
    feasibility = prob.is_feasible(current_solution)
    if feasibility:
        # Save the final schedule
        firefighter.save_schedule(current_solution)
    else:
        print("solution is infeasible")