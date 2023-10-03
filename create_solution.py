from firefighter import SchedulingProblem, save_schedule
from sys import argv


def create_solution(seed):
    """
    Creates a feasible solution based on the specified seed.
    Different seeds should generally lead to different solutions.

    TODO: Implement this method.
    """
    pass


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
