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


class SwapWeekendNeighbourhood(Neighbourhood):
    """
    Attain a new neighbors by swap a firefighter's shifts on different weekend
    """

    def __init__(self, prob):
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        total_days = self._prob._nb_weeks * 7

        for i in range(self._prob._nb_firefighters):
            for weekend_start in range(0, total_days, 7):
                # Copy the current schedule
                new_schedule = schedule[:]

                # Extract the weekend block for this firefighter
                weekend_block = new_schedule[i][weekend_start:weekend_start + 2]

                # Check if the firefighter works on the first day of the weekend
                if weekend_block[0] in ['M', 'A', 'N']:
                    # Move the weekend block to another weekend
                    new_weekend_start = random.choice([x for x in range(0, total_days, 7) if x != weekend_start])
                    new_schedule[i] = (
                            new_schedule[i][:new_weekend_start] + weekend_block + new_schedule[i][
                                                                                  new_weekend_start + 2:]
                    )

                    # Append the modified schedule to the result if feasible
                    if self._prob.is_feasible(new_schedule) is None:
                        result.append(new_schedule)

        return result


class ShiftExtensionNeighbourhood(Neighbourhood):
    """
    This neighborhood generates a neighbor by extending or shortening a consecutive work shift of a firefighter by
    one day.
    """
    def __init__(self, prob):
        self._prob = prob

    def neighbours(self, schedule):
        result = []

        for i in range(self._prob._nb_firefighters):
            # Firstly find a consecutive working shifts of a firefighter with function
            for shift in {"M", "A", "N"}:
                consecutive_shifts = firefighter.consecutive_numbers(schedule[i], len(schedule), {shift})
                for start_day, length in consecutive_shifts.items():
                    end_day = start_day + length - 1
                    # Extend the consecutive shifts, set the next day with same shift
                    if length <= 4 and end_day < 20:
                        new_schedule = schedule[:]
                        new_schedule[i] = (
                                    new_schedule[i][:end_day + 1] + new_schedule[i][end_day] + new_schedule[i][end_day + 2:])
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule[:])
                    # Shorten the consecutive shifts, replace the end day with next shift or rest
                    if length > 2 and end_day < 20:
                        next_shift = {'M': 'A', 'A': 'N', 'N': 'M'}[new_schedule[i][end_day]]
                        new_schedule = schedule[:]
                        # replace the end day with next shift
                        new_schedule[i] = (
                                new_schedule[i][:end_day] + next_shift + new_schedule[i][end_day + 1:])
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule[:])
                        new_schedule = schedule[:]
                        # replace the end day with next rest day
                        new_schedule[i] = (
                                new_schedule[i][:end_day] + 'F' + new_schedule[i][end_day + 1:])
                        if self._prob.is_feasible(new_schedule) is None:
                            result.append(new_schedule[:])
        print(f"one day change return {len(result)} neighbors!")
        return result


class SwapOneDayNeighbourhood(Neighbourhood):
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
                new_schedule = schedule[:]
                for day in range(self._prob._nb_weeks * 7):
                    temp_shift = new_schedule[i][day]
                    new_schedule[i] = new_schedule[i][:day] + new_schedule[j][day] + new_schedule[i][day + 1:]
                    new_schedule[j] = new_schedule[j][:day] + temp_shift + new_schedule[j][day + 1:]
                    if self._prob.is_feasible(new_schedule) is None:
                        result.append(new_schedule[:])

        print(f"swap one day return {len(result)} neighbors!")
        return result

class SwapOneDayNeighbourhood(Neighbourhood):
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
                new_schedule = schedule[:]
                for day in range(self._prob._nb_weeks * 7):
                    temp_shift = new_schedule[i][day]
                    new_schedule[i] = new_schedule[i][:day] + new_schedule[j][day] + new_schedule[i][day + 1:]
                    new_schedule[j] = new_schedule[j][:day] + temp_shift + new_schedule[j][day + 1:]
                    if self._prob.is_feasible(new_schedule) is None:
                        result.append(new_schedule[:])

        print(f"swap one day return {len(result)} neighbors!")
        return result