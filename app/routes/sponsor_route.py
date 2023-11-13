from fastapi import APIRouter
from app.services.sponsor_service import create_sponsor

router = APIRouter()

@router.post("/sponsor")
def create_sponsor_endpoint():
    pass