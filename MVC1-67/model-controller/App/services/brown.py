def calculate_milk_for_brown_cow(age_years: int) -> float:
    # If the result is less than 0, return 0.
    return max(40 - age_years, 0)