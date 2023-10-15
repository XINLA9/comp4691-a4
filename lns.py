from random import randint

import firefighter
from model import ModelBuilder


def destroy_schedule(schedule, method):
    # Implement different destroy methods based on the 'method' parameter
    # For example, if method is 1, clear the schedule for a random firefighter
    if method == 1:
        random_firefighter_index = randint(0, len(schedule) - 1)
        schedule[random_firefighter_index] = "O" * len(
            schedule[random_firefighter_index])  # Clear the schedule for that firefighter
    return schedule


if __name__ == '__main__':
    # TODO: Implement Large Neighbourhood Search

    # Load the initial schedule from example.sched
    schedule = firefighter.load_schedule("example.sched")
    firefighter.save_schedule(schedule)

    # Initialize the problem and costs
    prob = firefighter.SchedulingProblem()
    costs = firefighter.read_costs(prob)
    mb = ModelBuilder(prob)
    model = mb.build_model(costs)

    # Define LNS parameters
    num_destroy_methods = 3

    # Execute the Large Neighborhood Search for each destroy method
    for method in range(1, num_destroy_methods + 1):
        current_solution = firefighter.load_last_schedule()
        current_cost = prob.cost(current_solution, costs)

        print(f"Starting LNS with destroy method {method}")

        # Set the number of iterations (you can adjust this)
        max_iterations = 100

        for iteration in range(max_iterations):
            # Destroy part of the current solution
            destroyed_solution = destroy_schedule(current_solution, method)

            # Repair the destroyed solution using your repair method (you need to implement this)
            repaired_solution = repair_schedule(destroyed_solution, prob, costs)

            # Evaluate the repaired solution
            repaired_cost = prob.cost(repaired_solution, costs)

            # If the repaired solution is better than the current solution, update it
            if repaired_cost < current_cost:
                current_solution = repaired_solution
                current_cost = repaired_cost

        feasibility = prob.is_feasible(current_solution)
        if not feasibility:
            # Save the final schedule
            firefighter.save_schedule(current_solution)
            print(f"The cost of this solution with destroy method {method} is {current_cost}")
        else:
            print(feasibility)
