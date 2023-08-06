import pandas as pd


def max_pandas_display(pd: pd, max_row: int = 100) -> None:
    """
    set pandas print format to print all
    Args:
        pd: pandas object

    Returns: None

    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", max_row)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.expand_frame_repr", False)
