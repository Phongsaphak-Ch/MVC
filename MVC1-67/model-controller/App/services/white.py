def calculate_milk_for_white_cow(total_age_months: int) -> float:
    # If the result is less than 0, return 0.
    return max(120 - total_age_months, 0)