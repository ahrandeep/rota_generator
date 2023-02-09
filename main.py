########################
#        IMPORTS       #
########################
import random

########################
#   CLASS DEFINITIONS  #
########################
class User:
  """Base details for every person on the rota

  Attributes:
    code: A string containing the letter code for the user (unique)
    allowed_cols : A list containing int indexes of columns that user can be added to
    absent_rows: A list containing int indexes of rows that user cannot be added to (holidays etc.)
  """

  def __init__(self, code) -> None:
    self.code: str = code
    self.allowed_cols: list[int] = []
    self.absent_rows: list[int] = []
  
  def add_allowed_col(self, col_index) -> None:
    self.allowed_cols.append(col_index)
  
  def add_absent_row(self, row_index) -> None:
    self.absent_rows.append(row_index)


class Event:
  """Represents a specific cell in a given column and row

  An event on a specific date

  Attributes:
    col: An int indicating which column the event is in
    row: An int indicating which row the event is in, represents each date
    assigned: A User indicating which user has been assigned to this event
  """

  def __init__(self, col, row) -> None:
    self.col: int = col
    self.row: int = row
    self.assigned: User = None

  def assign(self, user) -> None:
    self.assigned = user


class Column:
  """Details of a single column with associated rules

  Attributes:
    header: A string containing name of the task
    max_per_week: An int indicating maximum number of this task a user can do in a week
    max_per_fortnight: An int indicating maximum number of this task a user can do in a fortnight
    max_per_month: An int indicating maximum number of this task a user can do in a month
    unallowed_cols: A list containing int indexes of which tasks (columns) cannot be assigned along with this one
  """

  def __init__(self, header, max_per_week, max_per_fortnight, max_per_month, unallowed_cols) -> None:
    self.header = header
    self.max_per_week = max_per_week
    self.max_per_fortnight = max_per_fortnight
    self.max_per_month = max_per_month
    self.unallowed_cols = unallowed_cols


class Grid:
  """Contains all events with corresponding columns/rows

  Attributes:
    rows: A 2D list containing Events organised in rows
    dates: A list containing the data associated with each row
    columns: A list of Columns containg data associated with each column
  """

  def __init__(self) -> None:
    self.events: list[list[Event]] = []
    self.rows: list[int] = []
    self.columns: list[Column] = []
  
  def add_row(self, row_data) -> None:
    self.events.append([])
    self.rows.append(row_data)
  
  def add_event(self, row) -> None:
    self.events[row].append(Event(len(self.events[row]), row))
  
  def add_column(self, column: Column) -> None:
    self.columns.append(column)


########################
# FUNCTION DEFINITIONS #
########################
def get_users() -> list[User]:
  """Gets details of all unique users
  
  Gets code, allowed columns and absent rows for each user

  Returns:
    A list of all unique users
  
  """

  users = []
  for i in range(1, 10):
    user = User(str(i))
    user.add_absent_row(random.randint(0, 19))
    for k in range(0, 5):
      user.add_allowed_col(k)
    user.allowed_cols.pop(random.randint(0, 4))
    users.append(user)
  return users

def get_grid() -> Grid:
  """Generates a grid with unassigned events representing each cell in thespradsheet
  
  Returns:
    A Grid object with unassigned events
  """

  grid = Grid()
  
  for k in range(0, 5):
    grid.add_column(Column(f"T{k + 1}", k + 1, (k + 1) * 2, (k + 1) * 4, [4, 0 if k%2 == 0 else 1]))

  for i in range(0, 20):
    grid.add_row(i)
    for k in range(0, 5):
      grid.add_event(i)

  return grid

def print_grid(grid: Grid) -> None:
  """Prints date and code of assigned user for each event"""
  col_string = ""
  for column in grid.columns:
    col_string += f"\t{column.header}"
  print(col_string)

  for count, row in enumerate(grid.events):
    row_string = str(grid.rows[count])
    for event in row:
      row_string += f"\t{event.assigned.code if event.assigned != None else 'None'}"
    print(row_string)

def check_event(grid: Grid, event: Event, users: list[User], row: list[Event], rand: int) -> User:
  """Finds a valid user to assign to an event
  
  Checks user against unallowed columns and max assigned events according to column rules

  Args:
    grid: The main Grid for access to columns
    event: The Event to check
    users: A list of all unique users to check
    row: A list of all other events in the row (same date)
    rand: A random seed to help randomise assignments
  
  Returns:
    A valid User who can be assigned to the event
    or None if no valid user could be found
  """

  assignee = None
  for i, user in enumerate(users):
    if event.col in user.allowed_cols:
      already_assigned = False
      
      for row_events in row:
        if row_events.assigned is user:
          if event.col in grid.columns[row_events.col].unallowed_cols:
            print(f"{event.col} cannot be done with {row_events.col}")
            already_assigned =True
      
      if already_assigned:
        continue
      
      week = 0
      fortnight = 0
      month = 0
      for row_num, rows in enumerate(grid.events):
        if rows[event.col].assigned is user:
          month += 1

          if event.row - 7 > row_num or event.row + 7 < row_num:
            week += 1

          if event.row - 14 > row_num or event.row + 14 < row_num:
            fortnight += 1
      
      if week > grid.columns[event.col].max_per_week or fortnight > grid.columns[event.col].max_per_fortnight or month > grid.columns[event.col].max_per_month:
        print(f"User {user.code} cannot be assigned more of {grid.columns[event.col].header}")
        continue

      assignee = user
      if i >= rand:
        break
  return assignee

def parse_event(grid: Grid, event: Event, users: list[User], row: list[Event], num_users: int) -> None:
  """Assigns a valid user to an event

  Uses check_event() to find a valid user and assigns it to event.
  Ignores the first event (0, 0) in grid as this is assigned according to seed in main()

  Args:
    grid: The main Grid for access to columns
    event: The Event to check
    users: A list of all unique users to check
    row: A list of all other events in the row (same date)
    num_users: An int indicating the number of unique users - 1
  """
  
  if event.row == 0 and event.col == 0:
    if event.assigned == None:
      print(f"Unable to find match for {event.col}, {event.row}")
  else:
    event.assign(check_event(grid, event, users, row, random.randint(0, num_users)))

    if event.assigned == None:
      print(f"Unable to find match for {event.col}, {event.row}")

def populate_grid(grid: Grid, users: list[User], seed: int) -> None:
  num_users = len(users) - 1
  saved_grid = grid

  # Assigned first event with seed
  grid.events[0][0].assign(check_event(grid, grid.events[0][0], users, grid.events[0], seed))
  # Loop through rows
  for row in grid.events:
    # Loop through columns
    if random.randint(0, 1) == 0:
      for event in row:
        parse_event(grid, event, users, row, num_users)
    else:
      col_num = len(row) - 1
      while col_num >= 0:
        parse_event(grid, row[col_num], users, row, num_users)
        col_num -= 1
        
  return grid


########################
#      MAIN RUNTIME    #
########################
def main():
  users = get_users()
  grid = get_grid()

  grid = populate_grid(grid, users, 5)

  print_grid(grid)
  

main()