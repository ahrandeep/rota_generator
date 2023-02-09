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
  

class Grid:
  """Contains all events with corresponding columns/rows

  Attributes:
    events: A 2D list containing Events organised in rows
    dates: A list containing the data associated with each row
  """

  def __init__(self) -> None:
    self.events: list[list[Event]] = []
    self.dates: list[int] = []
  
  def add_row(self, date) -> None:
    self.events.append([])
    self.dates.append(date)
  
  def add_event(self, row) -> None:
    self.events[row].append(Event(len(self.events[row]), row))

########################
# FUNCTION DEFINITIONS #
########################
def get_users() -> list[User]:
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
  grid = Grid()
  
  for i in range(0, 20):
    grid.add_row(i)
    for k in range(0, 5):
      grid.add_event(i)

  return grid

def print_grid(grid: Grid) -> None:
  for count, row in enumerate(grid.events):
    row_string = str(grid.dates[count])
    for event in row:
      row_string += f"\t{event.assigned.code if event.assigned != None else 'None'}"
    print(row_string)

def check_event(event: Event, users: list[User], row: list[Event], rand: int) -> User:
  assignee = None
  for i, user in enumerate(users):
    if event.col in user.allowed_cols:
      already_assigned = False
      
      for check_event in row:
        if check_event.assigned is user:
          already_assigned =True
      
      if already_assigned:
        continue

      assignee = user
      if i >= rand:
        break
  return assignee

def parse_event(event: Event, users: list[User], row: list[Event], row_num: int, num_users: int) -> None:
  if row_num == 0 and event.col == 0:
    if event.assigned == None:
      print(f"Unable to find match for {event.col}, {event.row}")
  else:
    attempts = 0
    while attempts < 5:
      event.assign(check_event(event, users, row, random.randint(0, num_users)))

      if event.assigned != None:
        break
      
      attempts += 1
    
    if event.assigned == None:
      print(f"Unable to find match for {event.col}, {event.row}")

def populate_grid(grid: Grid, users: list[User], seed: int) -> None:
  num_users = len(users) - 1
  saved_grid = grid

  # Assigned first event with seed
  grid.events[0][0].assign(check_event(grid.events[0][0], users, grid.events[0], seed))
  # Loop through rows
  for row_num, row in enumerate(grid.events):
    # Loop through columns
    if random.randint(0, 1) == 0:
      for event in row:
        parse_event(event, users, row, row_num, num_users)
    else:
      col_num = len(row) - 1
      while col_num >= 0:
        parse_event(row[col_num], users, row, row_num, num_users)
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