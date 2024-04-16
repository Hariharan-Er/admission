from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://thehariharan10:kali@cluster0.6hfswur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["admission_form_db"]
collection = db["admission_form"]

# Model for admission form data
class AdmissionForm(BaseModel):
    full_name: str
    email: str
    phone: str
    course: str
    message: str = None

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/admission-form")
async def submit_form(admission_form: AdmissionForm):
    try:
        admission_data = {
            "full_name": admission_form.full_name,
            "email": admission_form.email,
            "phone": admission_form.phone,
            "course": admission_form.course,
            "message": admission_form.message
        }
        result = collection.insert_one(admission_data)
        if result.inserted_id:
            return {"message": "Form submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit form")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app)
