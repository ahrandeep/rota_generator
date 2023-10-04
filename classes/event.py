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