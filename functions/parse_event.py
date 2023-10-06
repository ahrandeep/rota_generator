from random import randint

from classes.grid import Grid, Event
from functions.check_event import check_event


def parse_event(grid: Grid, event: Event, row: list[Event],
                num_users: int, verbose: bool = False) -> None:
    """Assigns a valid user to an event

    Uses check_event() to find a valid user and assigns it to event.
    Ignores the first event (0, 0) in grid as
      this is assigned according to seed in main()

    Args:
        grid: The main Grid for access to columns
        event: The Event to check
        row: A list of all other events in the row (same date)
        num_users: An int indicating the number of unique users - 1
        verbose: A bool indicating whether to print verbose statements
    """
    
    event.assign(check_event(grid, event, row, randint(0, num_users)))

    if event.assigned is None and verbose:
        print(f'Unable to find match for {event.col}, {event.row}')