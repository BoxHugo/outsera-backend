from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def healthcheck():
    """ Healthcheck """
    
    return {"message": "ok"}
