
from pathlib import Path
import json
import os
import subprocess

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="AI Smart Healthcare API")

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

# Select the executable for Windows or cloud Linux.
if os.getenv("CLOUD_DEPLOYMENT") == "1":
    C_PROGRAM = BASE_DIR / "patient_api"
else:
    C_PROGRAM = BASE_DIR / "patient_api.exe"
(
    BASE_DIR / "patient_api"
    if os.getenv("CLOUD_DEPLOYMENT") == "1"
    else BASE_DIR / "patient_api.exe"
)


class PatientInput(BaseModel):
    name: str = Field(min_length=1, max_length=49)
    age: int = Field(ge=1, le=150)
    gender: str = Field(min_length=1, max_length=9)
    disease: str = Field(min_length=1, max_length=49)

    @field_validator("name", "gender", "disease")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value or any(c in value for c in "|\r\n"):
            raise ValueError(
                "Text fields cannot be empty or contain pipes/newlines."
            )
        return value


@app.get("/")
def home():
    return {"message": "AI Smart Healthcare API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def run_c_program(*args: str):
    if not C_PROGRAM.is_file():
        raise HTTPException(
            status_code=500,
            detail="Patient C program not found."
        )

    try:
        result = subprocess.run(
            [str(C_PROGRAM), *args],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="C program timed out.")
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Could not start C program."
        )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail="C patient operation failed."
        )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="C program returned invalid JSON."
        )


@app.get("/patients/{patient_id}")
def search_patient(patient_id: int):
    if patient_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Patient ID must be positive."
        )

    patient = run_c_program("search", str(patient_id))

    if not patient.get("found"):
        raise HTTPException(status_code=404, detail="Patient not found.")

    return patient


@app.post("/patients", status_code=201)
def add_patient(patient: PatientInput):
    return run_c_program(
        "add",
        patient.name,
        str(patient.age),
        patient.gender,
        patient.disease,
    )
