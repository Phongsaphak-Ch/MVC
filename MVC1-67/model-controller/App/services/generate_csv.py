import csv
import os
from fastapi import HTTPException
from App.services.random_cow import generate_random_cows


COW_DATA_FILE = 'App/output/cow_data.csv'

# Function to write generated cow data to a CSV file
def write_cow_data_to_csv(cow_data):
    try:
        with open(COW_DATA_FILE, mode='w', newline='') as file:
            fieldnames = ['cow_id', 'breed', 'color', 'age_years', 'age_months']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cow_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to check if cow_data.csv exists, and create it if it doesn't
def check_and_generate_cow_data():
    if not os.path.exists(COW_DATA_FILE):
        # Generate 15 cows, with at least 3 cows for each color
        cow_data = generate_random_cows(num_cows=15)
        write_cow_data_to_csv(cow_data)
    else:
        print(f"File {COW_DATA_FILE} already exists. No need to generate new data.")