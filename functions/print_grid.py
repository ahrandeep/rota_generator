from classes.grid import Grid

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