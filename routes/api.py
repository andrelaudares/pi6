from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.recommendation import RecommendationEngine
from utils.input_processor import process_user_input

router = APIRouter()

class UserInput(BaseModel):
    location: str
    budget: float
    energy_needs: float
    roof_type: str
    property_type: str

@router.post("/recommend")
async def get_recommendations(user_input: UserInput):
    try:
        processed_input = process_user_input(user_input)
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(processed_input)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
