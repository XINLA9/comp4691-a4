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
        print(f"swap between firefighters {len(result)} neighbors!")
        return result


class OffDutyMoveNeighbourhood(Neighbourhood):
    """
    Attain a new neighbors by move a firefighter's day off tp another day
    """

    def __init__(self, prob):
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for i in range(self._prob._nb_firefighters):
            for day in range(self._prob._nb_weeks * 7):
                if schedule[i][day] == 'F':
                    s = schedule[i][:day] + schedule[i][i + 1:]
                    for k in range(len(s)):
                        new_schedule = schedule[:]
                        new_schedule[i] = s[:k] + 'F' + s[k:]
                        # Append the modified schedule to the result if feasible
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule)
        print(f"move duty off return {len(result)} neighbors!")
        return result

class TwoOffDutyMoveNeighbourhood(Neighbourhood):
    """
    Attain a new neighbors by move a firefighter's day off tp another day
    """

    def __init__(self, prob):
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for i in range(self._prob._nb_firefighters):
            for day in range(self._prob._nb_weeks * 7 - 1):
                if schedule[i][day] == 'F' and schedule[i][day + 1] == 'F':
                    s = schedule[i][:day] + schedule[i][i + 2:]
                    for k in range(len(s)):
                        new_schedule = schedule[:]
                        new_schedule[i] = s[:k] + 'FF' + s[k:]
                        # Append the modified schedule to the result if feasible
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule)
        print(f"move duty off return {len(result)} neighbors!")
        return result

class ChangOneDayNeighbourhood(Neighbourhood):
    """
    This neighborhood generates a neighbor by changing exactly one day schedule of one firefighter.
    """

    def __init__(self, prob) -> None:
        self._prob = prob

    def neighbours(self, schedule):
        result = []

        for i in range(self._prob._nb_firefighters):
            for day in range(self._prob._nb_weeks * 7):
                for k in {'M', 'N', 'A'}:
                    # Swaps one day schedule of firefighters i.
                    new_schedule = schedule[:]
                    if new_schedule[i][day] != k:
                        new_schedule[i] = new_schedule[i][:day] + k + new_schedule[i][day + 1:]
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule[:])

        print(f"change one day shift of one firefighter return {len(result)} neighbors!")
        return result


class SwapDaysNeighbourhood(Neighbourhood):
    """
    This neighborhood generates a neighbor by iteratively swapping the one-day schedules of exactly two firefighters.
    """

    def __init__(self, prob) -> None:
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for i in range(self._prob._nb_firefighters):
            for j in range(i + 1, self._prob._nb_firefighters):
                # Swaps one day schedule of firefighters i and j.
                new_schedule1 = schedule[:]
                for day in range(self._prob._nb_weeks * 7):
                    if new_schedule1[i][day] != new_schedule1[j][day]:
                        temp_shift = new_schedule1[i][day]
                        new_schedule1[i] = new_schedule1[i][:day] + new_schedule1[j][day] + new_schedule1[i][day + 1:]
                        new_schedule1[j] = new_schedule1[j][:day] + temp_shift + new_schedule1[j][day + 1:]
                        if self._prob.is_feasible(new_schedule1) is None:
                            result.append(new_schedule1[:])

        print(f"swap days shifts between firefighters return {len(result)} neighbors!")
        return result


class SwapDayNeighbourhood(Neighbourhood):
    """
    This neighborhood generates a neighbor by swapping one day schedule of exactly two firefighters.
    """

    def __init__(self, prob) -> None:
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for i in range(self._prob._nb_firefighters):
            for j in range(i + 1, self._prob._nb_firefighters):
                # Swaps one day schedule of firefighters i and j.
                for day in range(self._prob._nb_weeks * 7):
                    new_schedule1 = schedule[:]
                    if new_schedule1[i][day] != new_schedule1[j][day]:
                        temp_shift = new_schedule1[i][day]
                        new_schedule1[i] = new_schedule1[i][:day] + new_schedule1[j][day] + new_schedule1[i][day + 1:]
                        new_schedule1[j] = new_schedule1[j][:day] + temp_shift + new_schedule1[j][day + 1:]
                        if self._prob.is_feasible(new_schedule1) is None:
                            result.append(new_schedule1[:])

        print(f"swap one day between firefighters return {len(result)} neighbors!")
        return result


class ShiftRotationNeighbourhood(Neighbourhood):
    """
    This neighborhood generates a neighbor by swapping one day schedule of exactly two firefighters.
    """

    def __init__(self, prob) -> None:
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        for k in range(2):
            new_schedule = schedule[:]
            for i in range(self._prob._nb_firefighters):
                for day in range(self._prob._nb_weeks * 7):
                    next_shift = {'M': 'A', 'A': 'N', 'N': 'M', 'F': 'F'}[new_schedule[i][day]]
                    new_schedule[i] = new_schedule[i][:day] + next_shift + new_schedule[i][day + 1:]

            result.append(new_schedule[:])

        print(f"shift rotation return {len(result)} neighbors!")
        return result
