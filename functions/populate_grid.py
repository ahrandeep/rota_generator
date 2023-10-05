import random

from classes.grid import Grid
from functions.parse_event import parse_event
from functions.check_event import check_event


def populate_grid(grid: Grid, seed: int, verbose: bool = False) -> None:
    """Fills in grid by assigning users to events
    
    Loops through rows either forwards or backwards randomly

    Args:
        grid: The main grid to populate
        seed: An int used to determine starting assignment in the first event
        verbose: A bool indicating whether to print verbose statements 
    """

    num_users = len(grid.users) - 1

    # Assigned first event with seed
    grid.events[0][0].assign(check_event(grid, grid.events[0][0], grid.events[0], seed))
    # Loop through rows
    for row in grid.events:
      # Loop through columns
      if random.randint(0, 1) == 0:
          for event in row:
              parse_event(grid, event, row, num_users, verbose)
      else:
          col_num = len(row) - 1
          while col_num >= 0:
              parse_event(grid, row[col_num], row, num_users, verbose)
              col_num -= 1
          
    return grid