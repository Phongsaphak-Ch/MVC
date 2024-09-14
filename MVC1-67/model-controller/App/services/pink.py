def calculate_milk_for_pink_cow(age_months: int) -> float:
    # If the result is less than 0, return 0.
    return max(30 - age_months, 0)