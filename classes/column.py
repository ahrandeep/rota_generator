class Column:
    """Details of a single column with associated rules

    Attributes:
        header: A string containing name of the task
        max_per_week: An int indicating maximum number of this task 
          a user can do in a week
        max_per_fortnight: An int indicating maximum number of this task 
          a user can do in a fortnight
        max_per_month: An int indicating maximum number of this task 
          a user can do in a month
        unallowed_cols: A list containing int indexes of which tasks (columns)
          cannot be assigned with this one
    """

    def __init__(self, header: str, max_per_week: int,
                 max_per_fortnight: int, max_per_month: int,
                 consecutive_days: bool, unallowed_cols: list[int]) -> None:
        self.header = header
        self.max_per_week = max_per_week
        self.max_per_fortnight = max_per_fortnight
        self.max_per_month = max_per_month
        self.consecutive_days = consecutive_days
        self.unallowed_cols = unallowed_cols
