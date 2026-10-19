from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

class Rate(BaseModel):
    '''
    Pydantic BaseModel will perform all data validation for us by defining the class attributes beforehans 
    With field, we can even perform some checks (le -> lower or equal )
    '''
    date: str = Field(max_length=8) # max len for dates is 8 yyyymmdd
    rate_name: str
    value: float = Field(le=1) # max rate is 100%

rates = {
    1: {
        "date": "20261019",
        "rate_name": "US10Y",
        "value": 0.0320
    },
    2: {
        "date": "20261019",
        "rate_name": "US02Y",
        "value": 0.0285
    },
    3: {
        "date": "20261019",
        "rate_name": "US30Y",
        "value": 0.0378
    },
    4: {
        "date": "20261019",
        "rate_name": "DE10Y",
        "value": 0.0214
    },
    5: {
        "date": "20261019",
        "rate_name": "UK10Y",
        "value": 0.0412
    },
    6: {
        "date": "20261019",
        "rate_name": "JP10Y",
        "value": 0.0115
    },
    7: {
        "date": "20261019",
        "rate_name": "CH10Y",
        "value": 0.0098
    }

}


@app.get("/rate/{id}")
def get_rate(id: int) -> dict[str, Any]:
    '''
    Getter by ID.
    '''
    if id not in rates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given ID does not exist"
        )
    return rates[id]

@app.post("/rate")
def post_rate(data: Rate) -> dict[str, int]:
    '''
    Post method allows to create a new line in our database, uploading new info. 
    '''
    date = data.date
    rate_name = data.rate_name
    value = data.value
    
    new_id = max(rates.keys()) +1
    rates[new_id] = {
        "date": date,
        "rate_name": rate_name,
        "value": value
    }
    return {"new_id": new_id}

@app.put("/rate")
def update_rate(id:int, date: str, rate_name: str, value: float) -> dict[str, Any]:
    '''
    Put method allows to update a whole row from a database. 
    However, it requires all the row to be specified, not just some of the fields.  
    '''
    rates[id] = {
        "date": date, 
        "rate_name": rate_name,
        "value": value
    }
    return rates[id]

@app.patch("/rate")
def patch_rate(id: int, body: Rate) -> dict[str, Any]:
    '''
    Patch rate is similar to the put method, but allowing for just updating the fields we want. 
    The body can be set directly in the request body section in the scalar interface 
    '''
    rate_patched = rates[id] 

    rate_patched.update(body)

    rates[id] = rate_patched
    return rates[id]

@app.delete("/rate")
def delete_rate(id: int) -> dict[str, str]:
    '''
    Delete a row from our database by its id
    '''
    rates.pop(id)
    return {"detail": f"Rate with the id #{id} has been deleted."}

@app.get("/scalar", include_in_schema=False)
def get_scalar_doc():
    '''
    Scalar interface for the API. 
    '''
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Financial Data CalAPI"
    )