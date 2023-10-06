from random import randint

from classes.grid import Grid
from functions.parse_event import parse_event


def populate_grid(grid: Grid, verbose: bool = False) -> None:
    """Fills in grid by assigning users to events
    
    Loops through rows either forwards or backwards randomly

    Args:
        grid: The main grid to populate
        verbose: A bool indicating whether to print verbose statements 
    """

    num_users = len(grid.users) - 1
    num_rows = len(grid.events) - 1
    populated_rows = []

    while len(populated_rows) <= num_rows:
        row_to_pop = randint(0, num_rows)

        if row_to_pop in populated_rows:
            continue

        row = grid.events[row_to_pop]

        if randint(0, 1) == 0:
          for event in row:
              parse_event(grid, event, row, num_users, verbose)
        else:
            col_num = len(row) - 1
            while col_num >= 0:
                parse_event(grid, row[col_num], row, num_users, verbose)
                col_num -= 1

        populated_rows.append(row_to_pop)

    return grid