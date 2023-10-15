from random import randint
from pulp import PULP_CBC_CMD
import firefighter
from model import ModelBuilder


def destroy1(schedule: list) -> list:
    random_firefighter_index = randint(0, len(schedule) - 1)
    schedule[random_firefighter_index] = "O" * len(
        schedule[random_firefighter_index])  # Clear the schedule for that firefighter
    return schedule


def destroy2(schedule: list) -> list:
    # Determine the number of firefighters to clear their schedule
    num_firefighters_to_clear = randint(1, len(schedule))
    # Randomly select firefighters without duplicates
    firefighters_to_clear = set()
    while len(firefighters_to_clear) < num_firefighters_to_clear:
        random_firefighter_index = randint(0, len(schedule) - 1)
        firefighters_to_clear.add(random_firefighter_index)
    for firefighter_index in firefighters_to_clear:
        schedule[firefighter_index] = "O" * len(schedule[firefighter_index])


def destroy3(schedule: list) -> list:
    random_firefighter_index = randint(0, len(schedule) - 1)
    schedule[random_firefighter_index] = "O" * len(
        schedule[random_firefighter_index])  # Clear the schedule for that firefighter
    return schedule


def destroy(schedule: list, x: int) -> list:
    # Implement different destroy methods based on the 'x' parameter
    # For example, if method is x, clear the schedule for a random firefighter
    if x == 1:
        schedule = destroy1(schedule)
    elif x == 2:
        schedule = destroy2(schedule)
    elif x == 3:
        schedule = destroy3(schedule)
    return schedule


def repair(schedule, prob, costs):
    # Implement the repair method using the Pulp model and ModelBuilder
    mb = ModelBuilder(prob)
    model = mb.build_model(costs)
    res = model.solve(PULP_CBC_CMD(msg=False))
    if res != 1:
        print('No solution found')
        return schedule  # Return the original schedule if no solution is found
    else:
        repaired_solution = mb.extract_solution()
        return repaired_solution


if __name__ == '__main__':

    # Load the initial schedule from example.sched
    schedule = firefighter.load_schedule("example.sched")
    firefighter.save_schedule(schedule)

    # Initialize the problem and costs
    prob = firefighter.SchedulingProblem()
    costs = firefighter.read_costs(prob)

    # Define LNS parameters
    num_destroy_methods = 3


    # Set the number of iterations
    max_iterations = 100

    for iteration in range(max_iterations):
        current_solution = firefighter.load_last_schedule()
        current_cost = prob.cost(current_solution, costs)
        # Destroy part of the current solution
        destroyed_solution = destroy(current_solution, x)

        # Repair the destroyed solution using your repair method (you need to implement this)
        repaired_solution = repair(destroyed_solution, prob, costs)

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
        print(f"The cost of this solution with destroy method {x} is {current_cost}")
    else:
        print(feasibility)
