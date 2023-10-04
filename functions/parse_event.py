from classes.grid import Grid, Event
from functions.check_event import check_event
import random

def parse_event(grid: Grid, event: Event, row: list[Event], num_users: int) -> None:
    """Assigns a valid user to an event

    Uses check_event() to find a valid user and assigns it to event.
    Ignores the first event (0, 0) in grid as this is assigned according to seed in main()

    Args:
        grid: The main Grid for access to columns
        event: The Event to check
        row: A list of all other events in the row (same date)
        num_users: An int indicating the number of unique users - 1
    """
    
    if event.row == 0 and event.col == 0:
        if event.assigned is None:
            print(f'Unable to find match for {event.col}, {event.row}')
    else:
        event.assign(check_event(grid, event, row, random.randint(0, num_users)))

        if event.assigned is None:
            print(f'Unable to find match for {event.col}, {event.row}')