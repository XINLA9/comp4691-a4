import random
import firefighter
import neighbours

if __name__ == '__main__':
    # Load the initial schedule from example.sched
    schedule = firefighter.load_schedule("example.sched")
    firefighter.save_schedule(schedule)

    # Initialize the problem and costs
    prob = firefighter.SchedulingProblem()
    costs = firefighter.read_costs(prob)

    # Define neighbourhoods list
    neighborhoods = [
        # neighbours.SwapNeighbourhood(prob),
        neighbours.ChangOneDayNeighbourhood(prob),
        neighbours.OffDutyMoveNeighbourhood(prob),
        neighbours.SwapDaysNeighbourhood(prob),
        neighbours.TwoOffDutyMoveNeighbourhood(prob),

    ]

    # Initialize current solution


    # Define your VNS parameters
    kmax = len(neighborhoods)  # Number of neighborhoods
    k = 1

    # Execute the Variable Neighborhood Descent
    while k <= kmax:
        current_solution = firefighter.load_last_schedule()
        current_cost = prob.cost(current_solution, costs)
        # Choose the k-th neighbourhood
        neighborhood = neighborhoods[k - 1]
        # print(type(neighborhood))

        # Generate neighbors using the selected neighbourhood
        neighbors = neighborhood.neighbours(current_solution)

        # Evaluate the neighbors and find the best improved one
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
            firefighter.save_schedule(current_solution)
        # If a better neighbor is not found, move to the next neighborhood
        else:
            k += 1

    feasibility = prob.is_feasible(current_solution)
    if not feasibility:
        # Save the final schedule
        firefighter.save_schedule(current_solution)
        print(f"The cost of this solution is {current_cost}")
    else:
        print(feasibility)
