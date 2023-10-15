from random import randint, random

import firefighter
from firefighter import SchedulingProblem, save_schedule
from sys import argv


def create_solution(seed):
    """
    Creates a feasible solution based on the specified seed.
    Different seeds should generally lead to different solutions.

    TODO: Implement this method.
    """
    # Set the random seed for reproducibility


    # Initialize parameters and variables
    num_firefighters = 20
    days = 21
    shifts = ["M", "A", "N", "F"]
    schedule = []

    for _ in range(num_firefighters):
        # Generate a random schedule for each firefighter
        firefighter_schedule = ""
        for day in range(days):
            # Generate a random shift
            shift = shifts[randint(0, 3)]
            firefighter_schedule += shift
        schedule.append(firefighter_schedule)
    schedule = firefighter.load_schedule("example.sched")

    return schedule


if __name__ == "__main__":
    arg = 0  # default seed
    if len(argv) > 1:
        arg = int(argv[1])
    schedule = create_solution(arg)

    # Sanity check: making sure the schedule is feasible
    prob = SchedulingProblem()
    feasibility = prob.is_feasible(schedule)
    if feasibility != None:
        print(f"schedule is not feasible ({feasibility})")
        exit(0)

    save_schedule(schedule)

# eof
