from typing import List
import firefighter


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
                # if not self._prob.is_feasible(new_schedule) == None: continue No need to test for feasibility: this
                # new schedule is guaranteed to be feasible (assuming the specified one was feasible).
                result.append(new_schedule)
        return result


# TODO: Define more neighbourhoods, and remove this comment.
class SwapWeekendNeighbourhood(Neighbourhood):
    """
    A neighbourhood that swaps the weekend schedules of a firefighter.
    """

    def __init__(self, prob):
        super().__init__(prob)

    def neighbours(self, schedule):
        result = []
        nb_weekend_days = self._prob._nb_weeks * 2  # Number of weekend days in the scheduling period

        for i in range(self._prob._nb_firefighters):
            # Create a copy of the current schedule
            new_schedule = schedule[:]

            for day in range(nb_weekend_days):
                # Get the positions of the weekend days for the firefighter i
                day_i = day

                # Swap the schedules for the weekend days
                new_schedule[i][day_i], new_schedule[i][day_i + nb_weekend_days] = new_schedule[i][
                    day_i + nb_weekend_days], new_schedule[i][day_i]

            # Check if the new schedule is feasible and add it to the result
            if self._prob.is_feasible(new_schedule) is None:
                result.append(new_schedule)

        return result

# eof
