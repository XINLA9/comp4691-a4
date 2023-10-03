class Neighbourhood:
    """
    A neighbourhood is a class that computes explicitly neighbours of a schedule.
    """

    def neighbours(self, schedule):
        """
        Returns a list of feasible schedules that are neighbours of this schedule.
        """
        pass


class SwapNeighbourhood(Neighbourhood):
    """
    Example of a neighbourhood.
    A schedule s' is a neighbour of a schedule s
    if it can be obtained by swapping the schedule of exactly two firefighters.
    """

    def __init__(self, prob) -> None:
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for i in range(self._prob._nb_firefighters):
            for j in range(i + 1, self._prob._nb_firefighters):
                # Swaps the schedules of firefighters i and j.
                new_schedule = [
                    line for line in schedule
                ]  # notice that we can do that because strings are immutable (no risk of side effects)
                new_schedule[i] = schedule[j]
                new_schedule[j] = schedule[i]
                # if not self._prob.is_feasible(new_schedule) == None:
                #    continue
                # No need to test for feasibility: this new schedule is guaranteed to be feasible (assuming the specified one was feasible).
                result.append(new_schedule)
        return result


# TODO: Define more neighbourhoods, and remove this comment.

# eof
