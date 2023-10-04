from classes.grid import Grid, Event, User

def check_event(grid: Grid, event: Event, row: list[Event], rand: int) -> User:
  """Finds a valid user to assign to an event
  
  Checks user against unallowed columns and max assigned events
    according to column rules

  Args:
      grid: The main Grid for access to columns
      event: The Event to check
      row: A list of all other events in the row (same date)
      rand: A random seed to help randomise assignments
  
  Returns:
      A valid User who can be assigned to the event
      or None if no valid user could be found
  """

  assignee = None
  for i, user in enumerate(grid.users.values()):
    if event.col in user.allowed_cols:
      already_assigned = False
      
      for row_events in row:
        if row_events.assigned is user:
          if event.col in grid.columns[row_events.col].unallowed_cols:
            print(f'{event.col} cannot be done with {row_events.col}')
            already_assigned =True
      
      if already_assigned:
        continue
      
      week = 0
      fortnight = 0
      month = 0
      consecutive = False

      for row_num, rows in enumerate(grid.events):
        if rows[event.col].assigned is user:
          month += 1

          if row_num > event.row - 7 and row_num < event.row + 7:
            week += 1

          if row_num > event.row - 14 and row_num < event.row + 14:
            fortnight += 1
          
          if row_num > event.row - 2 and row_num < event.row + 2:
            consecutive = True
      
      if (week >= grid.columns[event.col].max_per_week or 
        fortnight >= grid.columns[event.col].max_per_fortnight or 
        month >= grid.columns[event.col].max_per_month or 
        (consecutive and not grid.columns[event.col].consecutive_days)):
        print(f'User {user.code} cannot be assigned more of '
            f'{grid.columns[event.col].header}')
        continue

      assignee = user
      if i >= rand:
        break
  return assignee