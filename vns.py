import random
import firefighter
import neighbours

if __name__ == '__main__':
    # Load the initial schedule from example.sched
    initial_schedule = firefighter.load_schedule("example.sched")

    # Initialize the problem and costs
    prob = firefighter.SchedulingProblem()
    costs = firefighter.read_costs(prob)

    # Define neighbourhoods list
    neighborhoods = [neighbours.SwapNeighbourhood(prob)]

    # Initialize current solution
    current_solution = initial_schedule
    current_cost = prob.cost(current_solution, costs)

    # Define your VNS parameters
    kmax = len(neighborhoods)  # Number of neighborhoods
    k = 1

    # Execute the Variable Neighborhood Descent
    while k <= kmax:
        # Choose the k-th neighbourhood`
        neighborhood = neighborhoods[k - 1]
        print(type(neighborhood))

        # Generate neighbors using the selected neighbourhood
        neighbors = neighborhood.neighbours(current_solution)

        # Evaluate the neighbors and find the best one
        improved_neighbor = None
        improved_neighbor_cost = current_cost

        for neighbor in neighbors:
            neighbor_cost = prob.cost(neighbor, costs)
            if neighbor_cost < improved_neighbor_cost:
                improved_neighbor = neighbor
                improved_neighbor_cost = neighbor_cost

        # If a better neighbor is found, update the current solution and reset k
        if improved_neighbor is not None and improved_neighbor_cost < current_cost:
            current_solution = improved_neighbor
            current_cost = improved_neighbor_cost
            k = 1
        # If a better neighbor is not found, move to the next neighborhood
        else:
            k += 1

    feasibility = prob.is_feasible(current_solution)
    if not feasibility:
        # Save the final schedule
        firefighter.save_schedule(current_solution)
    else:
        print(feasibility)
