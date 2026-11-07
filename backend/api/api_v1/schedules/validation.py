from datetime import time

from fastapi import HTTPException, status


def validate_time_to_naive(t: time):
    return t.replace(tzinfo=None) if t.tzinfo else t


def validate_time_range(start_time: time, end_time: time):
    if validate_time_to_naive(start_time) >= validate_time_to_naive(end_time):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Start time must be before end time",
        )
