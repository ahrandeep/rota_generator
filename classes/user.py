class User:
    """Base details for every person on the rota

    Attributes:
        code: A string containing the letter code for the user (unique)
        allowed_cols : A list containing int indexes of columns 
          that user can be added to
        absent_rows: A list containing int indexes of rows 
          that user cannot be added to (holidays etc.)
    """

    def __init__(self, code: str) -> None:
        self.code = code
        self.allowed_cols: list[int] = []
        self.absent_rows: list[int] = []
    
    def add_allowed_col(self, col_index: int) -> None:
        self.allowed_cols.append(col_index)
    
    def add_absent_row(self, row_index: int) -> None:
        self.absent_rows.append(row_index)

