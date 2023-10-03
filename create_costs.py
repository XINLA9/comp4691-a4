import random
from firefighter import (
    SchedulingProblem,
    DAYS_PER_WEEK,
    SHIFT_AFTERNOON,
    SHIFT_MORNING,
    SHIFT_NIGHT,
)

if __name__ == "__main__":
    MY_ID = 46918691
    random.seed(MY_ID)

    with open("costs.scosts", "w") as f:
        prob = SchedulingProblem()
        for i in range(prob._nb_firefighters):
            for d in range(DAYS_PER_WEEK):
                for shift_type in [SHIFT_AFTERNOON, SHIFT_MORNING, SHIFT_NIGHT]:
                    f.write(
                        str(random.random())
                    )  # chooses a random number between 0 and 1
                    f.write(" ")

# eof
