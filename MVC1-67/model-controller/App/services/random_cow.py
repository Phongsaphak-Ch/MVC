import random

COW_BREEDS = {
    "White": "Holstein",
    "Brown": "Guernsey",
    "Pink": "Jersey"
}
COW_COLORS = list(COW_BREEDS.keys())

def generate_random_cows(num_cows=15):
    cow_data = []

    # First, generate initial cows
    for _ in range(num_cows):
        cow_id = str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
        color = random.choice(COW_COLORS)
        breed = COW_BREEDS[color]
        age_years = random.randint(0, 10)
        age_months = random.randint(0, 11)

        cow_data.append({
            'cow_id': cow_id,
            'breed': breed,
            'color': color,
            'age_years': age_years,
            'age_months': age_months
        })

    # Ensure at least 3 cows of each color
    for color in COW_COLORS:
        color_cows = [cow for cow in cow_data if cow['color'] == color]
        while len(color_cows) < 3:
            cow_id = str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
            new_cow = {
                'cow_id': cow_id,
                'breed': COW_BREEDS[color],
                'color': color,
                'age_years': random.randint(0, 10),
                'age_months': random.randint(0, 11)
            }
            cow_data.append(new_cow)
            color_cows.append(new_cow)

    return cow_data
