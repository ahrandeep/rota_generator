from datetime import datetime

from classes.user import User
from classes.event import Event
from classes.column import Column

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