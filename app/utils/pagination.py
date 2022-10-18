from typing import Any, Dict


def pagination(end: int, page: int, response: Dict, total_count: int):
    if end >= total_count:
        response["pagination"]["next"] = None
        if page > 1:
            response["pagination"]["prev"] = page - 1
        else:
            response["pagination"]["prev"] = None
    else:
        if page > 1:
            response["pagination"]["prev"] = page - 1
        else:
            response["pagination"]["prev"] = None
        response["pagination"]["next"] = page + 1