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


class ChangeShiftNeighbourhood(Neighbourhood):
    """
    A schedule s' is a neighbour of a schedule s
    if it can be obtained by 将一位消防员的班次循环往后推一个
    """

    def __init__(self, prob):
        self._prob = prob

    def neighbours(self, schedule):
        result = []
        new_schedule = schedule[:]
        for i in range(self._prob._nb_firefighters):
            # Create a copy of the current schedule
            schedule_list = list(new_schedule[i])
            for c in range(len(schedule_list)):
                if schedule_list[c] == 'M':
                    schedule_list[c] = 'A'
                elif schedule_list[c] == 'A':
                    schedule_list[c] = 'N'
                elif schedule_list[c] == 'N':
                    schedule_list[c] = 'M'
            new_schedule[i] = ''.join(schedule_list)
        if self._prob.is_feasible(new_schedule) is None:
            result.append(new_schedule)

        return result


class MoveWeekendNeighbourhood(Neighbourhood):
    """
    A neighbourhood that moves a firefighter's weekend shift to another weekend.
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
