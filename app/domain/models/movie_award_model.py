from pydantic import BaseModel


class MovieAwardModel(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int
