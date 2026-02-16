from config import PRIORITIES, STATUSES


def validate_priority(priority):
    if priority not in PRIORITIES:
        raise ValueError(f"Invalid priority. Choose from {PRIORITIES}")


def validate_status(status):
    if status not in STATUSES:
        raise ValueError(f"Invalid status. Choose from {STATUSES}")
