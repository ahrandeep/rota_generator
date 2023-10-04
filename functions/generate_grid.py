from classes.grid import Grid, Column
import functions.sheets_api as sheets_api
from string import ascii_lowercase

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
            """Generate columns from header row and add rules
              (unallowed columns and max per week/fortnight/month)"""
            for col_index, value in enumerate(row):
                if value.strip() == '':
                    continue

                unallowed_cols = []
                max_per_week = 7
                max_per_fortnight = 14
                max_per_month = 31
                consecutive_days = True

                """rules_len is checked so that the index
                  is not out of range for column_rules
                column_rules[index] is then checked to see
                  if it is an empty list (returns false)
                col_index is then checked to ensure index is not out of range"""
                if (column_rules and rules_len > 0 and 
                    column_rules[0] and col_index < len(column_rules[0])):
                    
                    for letter in column_rules[0][col_index].lower().strip():
                        unallowed_cols.append(ascii_lowercase.index(letter) - 1)

                if (column_rules and rules_len > 1 and 
                    column_rules[1] and col_index < len(column_rules[1]) and 
                    column_rules[1][col_index].strip() != ''):
                    
                    max_per_week = int(column_rules[1][col_index].strip())
                
                if (column_rules and rules_len > 2 and 
                    column_rules[2] and col_index < len(column_rules[2]) and 
                    column_rules[2][col_index].strip() != ''):
                    
                    max_per_fortnight = int(column_rules[2][col_index].strip())
                
                if (column_rules and rules_len > 3 and 
                    column_rules[3] and col_index < len(column_rules[3]) and 
                    column_rules[3][col_index].strip() != ''):
                    
                    max_per_month = int(column_rules[3][col_index].strip())
                
                if (column_rules and rules_len > 3 and 
                    column_rules[4] and col_index < len(column_rules[4]) and 
                    column_rules[4][col_index].strip() != ''):
                    # Checked to not equal 'N' so that blank entries default to True
                    consecutive_days = column_rules[4][col_index].strip() != 'N'

                grid.add_column(Column(value.strip(), max_per_week, max_per_fortnight, 
                                       max_per_month, consecutive_days, unallowed_cols))
        
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
