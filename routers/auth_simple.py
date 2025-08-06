print("Starting auth_new.py import")

from fastapi import APIRouter

print("FastAPI imported successfully")

router = APIRouter()

print("Router created successfully")

@router.get("/test")
async def test():
    return {"message": "test"}

print("Router configured successfully")
