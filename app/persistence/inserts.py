from typing import List

from app.mlb_models import Base

from .util import insert_result


@insert_result()
def insert_rows(rows: List[Base]):
    return rows
