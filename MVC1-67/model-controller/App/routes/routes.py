from fastapi import APIRouter, Query, HTTPException
from App.services.cow import *
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/get_milk_production')
async def get_milk_production(cow_id: str = Query(...)):
    try:
        # Validate cow ID is numeric and 8 digits long, and doesn't start with 0
        if len(cow_id) != 8 or not cow_id.isdigit() or cow_id[0] == '0':
            raise HTTPException(status_code=400, detail='Invalid cow ID. Must be exactly 8 digits and cannot start with 0.')
        
        # Retrieve cow by ID
        cow = get_cow_by_id(cow_id)
        
        # Calculate milk production and type based on cow's attributes
        milk_production, milk_type = calculate_milk_production(cow)

        # Read current totals from CSV
        milk_totals = read_milk_production_totals()

        # Update the total for the specific milk type
        milk_totals[milk_type] += milk_production
        
        # Write updated totals back to CSV
        write_milk_production_totals(milk_totals)
        
        # Returning additional cow information with the milk production result
        return JSONResponse({
            'status': 200,
            'cow_id': cow_id,
            'breed': cow['breed'],
            'color': cow['color'],
            'age_years': cow['age_years'],
            'age_months': cow['age_months'],
            'milk_production': milk_production,
            'milk_type': milk_type
        })
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        # Fallback for general exceptions
        raise HTTPException(status_code=500, detail='An internal error occurred: ' + str(e))
    
@router.get('/get_cow_data')
async def get_cow_data():
    try:
        # Read cow data from CSV file
        cow_data = read_cow_data()
        milk_produce = read_milk_production_totals()
        return JSONResponse(content={'status': 200, 'data': cow_data, 'milk': milk_produce})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error: ' + str(e))
