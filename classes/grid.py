from datetime import datetime
from classes.user import User

class Event:
    """Represents a specific cell in a given column and row

    An event on a specific date

    Attributes:
        col: An int indicating which column the event is in
        row: An int indicating which row the event is in, represents each date
        assigned: A User indicating which user has been assigned to this event
    """

    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
        self.assigned: User = None

    def assign(self, user: User) -> None:
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

    def __init__(self, header: str, max_per_week: int, max_per_fortnight: int, max_per_month: int, consecutive_days: bool, unallowed_cols: list[int]) -> None:
        self.header = header
        self.max_per_week = max_per_week
        self.max_per_fortnight = max_per_fortnight
        self.max_per_month = max_per_month
        self.consecutive_days = consecutive_days
        self.unallowed_cols = unallowed_cols


class Grid:
    """Contains all events with corresponding columns/rows

    Attributes:
        rows: A 2D list containing Events organised in rows
        dates: A list containing the data associated with each row
        columns: A list of Columns containg data associated with each column
    """

    def __init__(self, month: int, year: int) -> None:
        self.events: list[list[Event]] = []
        self.rows: list[int] = []
        self.columns: list[Column] = []
        self.users: dict[str, User] = {}
        self.dates: list[datetime] = []
        for i in range(1,32):
            try:
                self.dates.append(datetime(year, month, i))
            except ValueError:
                break
    
    def add_row(self, row_data: str) -> None:
        self.events.append([])
        self.rows.append(row_data)
    
    def add_event(self, row: int) -> None:
        self.events[row].append(Event(len(self.events[row]), row))
    
    def add_column(self, column: Column) -> None:
        self.columns.append(column)

    def add_user(self, code: str) -> None:
        if code in self.users:
            return
        self.users[code] = User(code)