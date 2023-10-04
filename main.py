########################
#        IMPORTS       #
########################
import functions.sheets_api as sheets_api
from functions.generate_grid import generate_grid
from functions.populate_grid import populate_grid
from functions.print_grid import print_grid



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