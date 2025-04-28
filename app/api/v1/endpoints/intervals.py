from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse
from app.controllers.intervals_controller import IntervalsController
from config import config


router = APIRouter()


@router.get("")
async def intervals() -> JSONResponse:
    """ Get intervals (max and min) from Golden Raspberry Awards. """

    try:
        intervals = IntervalsController().get_award_intervals()

        return JSONResponse(content=intervals, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
