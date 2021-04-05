from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from audio_server.database import (
    add_song,
    add_audiobook,
    add_podcast,
    delete_audio,
    retrieve_audio,
    audiofiles,
    update_audio,
)
from audio_server.models.audioModel import (
    ErrorResponseModel,
    ResponseModel,
    SongSchema,
    UpdateSongModel,
    PodcastSchema,
    UpdatePodcastModel,
    AudioBookSchema,
    UpdateAudioBookModel,
)

router = APIRouter()

@router.post("/audio/", response_description="Student data added into the database")
async def add_audio_data(song: SongSchema = None,podcast:PodcastSchema=None,
                         audiobook: AudioBookSchema= None):

    if song:
        song = jsonable_encoder(song)
        new_song = await add_song(song)
        return ResponseModel(new_song, "Song added successfully.")
    elif podcast:
        podcast = jsonable_encoder(podcast)
        new_podcast = await add_podcast(podcast)
        return ResponseModel(new_podcast, "Podcast added successfully.")
    elif audiobook:
        audiobook = jsonable_encoder(audiobook)
        new_audiobook = await add_audiobook(audiobook)
        return ResponseModel(new_audiobook, "Audiobook added successfully.")

    return ErrorResponseModel("Data Couldn't be fetched","Try Again")


@router.get("/audio", response_description="Getting audiofiles.....")
async def get_audios():
    audios = await audiofiles()
    if audios:
        return ResponseModel(audios, "audiofiles retrieved successfully")
    return ResponseModel(audios, "Empty list returned")


@router.get("/audio/{id}", response_description="Getting audio....")
async def get_audio_data(id):
    audio = await retrieve_audio(id)
    if audio:
        return ResponseModel(audio, "Audio data retrieved successfully")
    return ErrorResponseModel("An error occurred.", "Student doesn't exist.")



@router.put("/audio/{id}")
async def update_audio_data(id: str, song: UpdateSongModel = None,podcast: UpdatePodcastModel = None,
                              audiobook: UpdateAudioBookModel = None):
    if song:
        song = jsonable_encoder(song)
        updated_song = await update_audio(id, song)
        if updated_song:
            return ResponseModel(
                "Song with ID: {} name update is successful".format(id),
                "song updated successfully",
            )

    elif podcast:
        podcast = jsonable_encoder(podcast)
        updated_podcast = await update_audio(id, podcast)
        if updated_podcast:
            return ResponseModel(
                "Podcast with ID: {} name update is successful".format(id),
                "podcast updated successfully",
            )
    elif audiobook:
        audiobook = jsonable_encoder(audiobook)
        updated_audiobook = await update_audio(id, audiobook)
        if updated_audiobook:
            return ResponseModel(
                "Audiobook with ID: {} name update is successful".format(id),
                "Audiobook updated successfully",
            )




    return ErrorResponseModel(
        "An error occurred",

        "There was an error updating the  data."
    )


@router.delete("/audio/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_audio = await delete_audio(id)
    if deleted_audio:
        return ResponseModel(
            "Audio with ID: {} removed".format(id), "Audio deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", "Audio with id {0} doesn't exist".format(id)
    )