from typing import List, Dict
import pandas as pd
from random import choice

__all__ = [
    "delete_col",
    "replace_data"
]


def dframe_to_dict(func):
    def inner(*args, **kwargs):
        dataf = func(*args, **kwargs)
        if dataf is not None:
            return dataf.to_dict("records")

    return inner


@dframe_to_dict
def delete_col(self, *, data: List[Dict], cols: list = None):
    frame = pd.DataFrame(data)
    return frame.drop(cols, axis=1)


@dframe_to_dict
def replace_data(self, *, data: List[Dict], _new: dict[str, list | tuple] = None, rate: float = 0.5):
    frame = pd.DataFrame(data)
    f_columns = set(frame.columns)
    _new_columns = set(_new.keys())
    _mod = _new_columns - f_columns
    if _mod == set():
        for field, values in _new.items():
            ser = frame[field].copy(deep=False)
            for i in range(int(len(ser) * rate)):
                ser[i] = choice(values)
        return frame
    raise KeyError(f"{_mod!s} not exist!")
