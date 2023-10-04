########################
#        IMPORTS       #
########################
import sheets_api
import random
from string import ascii_lowercase
from classes.grid import Grid, Column, Event, User

########################
#   CLASS DEFINITIONS  #
########################


    

########################
# FUNCTION DEFINITIONS #
########################
def generate_grid(month: int, year:int) -> Grid:
    """Generates a grid with unassigned events representing each cell in the spreadsheet
    
    Returns:
        A Grid object with unassigned events
    """

    grid = Grid(month, year)
    
    data = sheets_api.get_data()
    allowed_users = data[0]['values'] if 'values' in data[0] else None
    column_rules = data[1]['values'] if 'values' in data[1] else None
    rules_len = len(column_rules)

    if not allowed_users:
        print("No values found")
        return grid

    for row_index, row in enumerate(allowed_users):
        if row_index == 0:
            # Generate columns from header row and add rules (unallowed columns and max per week/fortnight/month)
            for col_index, value in enumerate(row):
                if value.strip() == '':
                    continue

                unallowed_cols = []
                max_per_week = 7
                max_per_fortnight = 14
                max_per_month = 31
                consecutive_days = True

                # rules_len is checked so that the index is not out of range for column_rules
                # column_rules[index] is then checked to see if it is an empty list (returns false)
                # col_index is then checked to ensure index is not out of range
                if column_rules and rules_len > 0 and column_rules[0] and col_index < len(column_rules[0]):
                    for letter in column_rules[0][col_index].lower().strip():
                        unallowed_cols.append(ascii_lowercase.index(letter) - 1)

                if column_rules and rules_len > 1 and column_rules[1] and col_index < len(column_rules[1]) and column_rules[1][col_index].strip() != '':
                    max_per_week = int(column_rules[1][col_index].strip())
                
                if column_rules and rules_len > 2 and column_rules[2] and col_index < len(column_rules[2]) and column_rules[2][col_index].strip() != '':
                    max_per_fortnight = int(column_rules[2][col_index].strip())
                
                if column_rules and rules_len > 3 and column_rules[3] and col_index < len(column_rules[3]) and column_rules[3][col_index].strip() != '':
                    max_per_month = int(column_rules[3][col_index].strip())
                
                if column_rules and rules_len > 3 and column_rules[4] and col_index < len(column_rules[4]) and column_rules[4][col_index].strip() != '':
                    # Checked to not equal 'N' so that blank entries default to True
                    consecutive_days = column_rules[4][col_index].strip() != 'N'

                grid.add_column(Column(value.strip(), max_per_week, max_per_fortnight, max_per_month, consecutive_days, unallowed_cols))
        
        else:
            # generate users and allowed rows
            for col_index, value in enumerate(row):
                value = value.upper().strip()
                if value == '':
                    continue
                
                if value not in grid.users:
                    grid.add_user(value)
                
                grid.users[value].allowed_cols.append(col_index)

    row_count = 0
    for date in grid.dates:
        if date.weekday() > 4:
            continue
        grid.add_row(row_count)
        for k in range(0, len(grid.columns)):
            grid.add_event(row_count)
        row_count += 1

    return grid

def print_grid(grid: Grid) -> None:
    """Prints date and code of assigned user for each event"""
    col_string = '\t'
    for column in grid.columns:
        col_string += f"\t{column.header}"
    print(col_string)

    row_count = 0
    for date in grid.dates:
        row_string = date.strftime("%m/%d/%Y")
        if date.weekday() <= 4:
            for event in grid.events[row_count]:
                row_string += f'\t{event.assigned.code if event.assigned is not None else "None"}'
            row_count += 1
        
        print(row_string)

def check_event(grid: Grid, event: Event, row: list[Event], rand: int) -> User:
    """Finds a valid user to assign to an event
    
    Checks user against unallowed columns and max assigned events according to column rules

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
            
            if week >= grid.columns[event.col].max_per_week or fortnight >= grid.columns[event.col].max_per_fortnight or month >= grid.columns[event.col].max_per_month or (consecutive and not grid.columns[event.col].consecutive_days):
                print(f'User {user.code} cannot be assigned more of {grid.columns[event.col].header}')
                continue

            assignee = user
            if i >= rand:
                break
    return assignee

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
        if event.assigned == None:
            print(f'Unable to find match for {event.col}, {event.row}')
    else:
        event.assign(check_event(grid, event, row, random.randint(0, num_users)))

        if event.assigned == None:
            print(f'Unable to find match for {event.col}, {event.row}')

def populate_grid(grid: Grid, seed: int) -> None:
    """Fills in grid by assigning users to events
    
    Loops through rows either forwards or backwards randomly

    Args:
        grid: The main grid to populate
        seed: An int used to determine starting assignment in the first event
    """

    num_users = len(grid.users) - 1

    # Assigned first event with seed
    grid.events[0][0].assign(check_event(grid, grid.events[0][0], grid.events[0], seed))
    # Loop through rows
    for row in grid.events:
        # Loop through columns
        if random.randint(0, 1) == 0:
            for event in row:
                parse_event(grid, event, row, num_users)
        else:
            col_num = len(row) - 1
            while col_num >= 0:
                parse_event(grid, row[col_num], row, num_users)
                col_num -= 1
          
    return grid


########################
#      MAIN RUNTIME    #
########################
def main():
    month, year = 10, 2023
    grid = generate_grid(month, year)

    grid = populate_grid(grid, 5)

    print_grid(grid)
    
    sheets_api.write_data(grid)

if __name__ == '__main__':
    main()