from functions.sheets_api.write_data import write_data
from functions.generate_grid import generate_grid
from functions.populate_grid import populate_grid
from functions.print_grid import print_grid


def main():
    month, year = 2, 2024
    grid = generate_grid(month, year)

    grid = populate_grid(grid, 7, False)

    # print_grid(grid)

    write_data(grid)


if __name__ == '__main__':
    main()
