from typing import Optional,List
from pydantic import BaseModel, validator, Field

from datetime import datetime,date

class AudioType(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    duration: int = Field(..., gt=0)
    upload: datetime

    @validator("upload")
    def ensure_date_range(cls, v):
        if str(v.date()) != str(date.today()):
            raise ValueError("Uploadtime can't be in your past")
        return v

class UpdateAudioModel(BaseModel):

    name: Optional[str]
    duration: Optional[int]
    upload: datetime

    @validator("upload")
    def ensure_date_range(cls, v):
        if str(v.date()) != str(date.today()):
            raise ValueError("Uploadtime can't be in your past")
        return v

class SongSchema(AudioType):
    pass

class UpdateSongModel(UpdateAudioModel):
    pass

class Participent(BaseModel):
    p_name : str = Field(...,min_length=1,max_length=100)
class PodcastSchema(AudioType):
    host: str = Field(..., min_length=1, max_length=100)
    participents: List[Participent] = Field(None, max_items=10)

class UpdatePodcastModel(UpdateAudioModel):
    host: Optional[str]
    participents: Optional[List[Participent]]

class AudioBookSchema(AudioType):

     author: str = Field(..., min_length=1, max_length=100)
     narrator: str = Field(..., min_length=1, max_length=100)



class UpdateAudioBookModel(UpdateAudioModel):

    author: Optional[str]
    narrator : Optional[str]
    



def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, message ,code=500): ###
    return {"error": error, "code": code, "message": message}
