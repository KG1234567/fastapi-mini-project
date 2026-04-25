from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StrictInt, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="The full name of the patient")]
    city: Annotated[str, Field(..., description="The city where the patient resides")]
    age: Annotated[StrictInt, Field(..., gt=0, lt=120, description="The age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms")]

    @computed_field
    @property
    def bmi(Self) -> float:
        return round(Self.weight / (Self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(Self) -> str:
        if Self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= Self.bmi < 25:
            return "Normal weight"
        elif 25 <= Self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="The full name of the patient")]
    city: Annotated[Optional[str], Field(default=None, description="The city where the patient resides")]
    age: Annotated[Optional[StrictInt], Field(default=None, gt=0, lt=120, description="The age of the patient")]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None, description="The gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="The height of the patient in meters")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="The weight of the patient in kilograms")]


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A Fully Functional API to manage our Patient Records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve"), example="P001"):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by height, weight or bmi"), order:
    str = Query('asc', description="The order to sort patients, either 'asc' or 'desc'")):
    data = load_data()
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'")
    
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    # add new patient to data
    data[patient.id] = patient.model_dump(exclude=['id'])  # convert to dict
    
    # save into json file
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully", "patient_id": patient.id}, status_code=201)


@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]

    updated_patient = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient.items():
        existing_patient[key] = value
    
    existing_patient['id'] = patient_id  
    patient_pydantic_object = Patient(**existing_patient)  
    
    existing_patient = patient_pydantic_object.model_dump(exclude=['id'])

    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(content={"message": "Patient updated successfully", "patient_id": patient_id}, status_code=200)

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(content={"message": "Patient deleted successfully", "patient_id": patient_id}, status_code=200)

