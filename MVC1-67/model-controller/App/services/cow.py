import csv
import os
import random
from fastapi import HTTPException
from App.services.random_cow import generate_random_cows
from App.services.brown import *
from App.services.white import *
from App.services.pink import *

COW_DATA_FILE = 'App/output/cow_data.csv'
MILK_PRODUCTION_FILE = 'App/output/milk_production_totals.csv'

# Function to read or initialize milk production totals from CSV
def read_milk_production_totals():
    if not os.path.exists(MILK_PRODUCTION_FILE):
        # Initialize the totals if the file doesn't exist
        return {'นมจืด': 0.0, 'นมช็อกโกแลต': 0.0, 'นมสตรอว์เบอร์รี่': 0.0}
    
    milk_totals = {'นมจืด': 0.0, 'นมช็อกโกแลต': 0.0, 'นมสตรอว์เบอร์รี่': 0.0}
    with open(MILK_PRODUCTION_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            milk_totals[row['milk_type']] = float(row['milk_production'])
    return milk_totals

# Function to write updated milk production totals to CSV
def write_milk_production_totals(milk_totals):
    with open(MILK_PRODUCTION_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['milk_type', 'milk_production']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for milk_type, milk_production in milk_totals.items():
            writer.writerow({'milk_type': milk_type, 'milk_production': milk_production})

# Function to read cow data from CSV
def read_cow_data():
    cow_data = []
    try:
        with open(COW_DATA_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cow_data.append(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return cow_data

# Function to retrieve cow by ID
def get_cow_by_id(cow_id: str):
    cow_data = read_cow_data()
    for cow in cow_data:
        if cow['cow_id'] == cow_id:
            return cow
    raise HTTPException(status_code=404, detail=f'Cow ID {cow_id} not found')

# Function to calculate milk production and return milk type based on the cow's color and age
def calculate_milk_production(cow):
    age_years = int(cow['age_years'])
    age_months = int(cow['age_months'])
    total_age_months = age_years * 12 + age_months

    if cow['color'] == 'White':
        milk = calculate_milk_for_white_cow(total_age_months)
        milk_type = 'นมจืด'
    elif cow['color'] == 'Brown':
        milk = calculate_milk_for_brown_cow(age_years)
        milk_type = 'นมช็อกโกแลต' 
    elif cow['color'] == 'Pink':
        milk = calculate_milk_for_pink_cow(age_months)
        milk_type = 'นมสตรอว์เบอร์รี่'
    else:
        raise HTTPException(status_code=400, detail='Invalid cow color')

    return milk, milk_type  # Return both milk amount and milk type
