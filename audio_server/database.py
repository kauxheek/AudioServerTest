import motor.motor_asyncio
from bson import ObjectId
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)


database = client.AudioFiles

song_collection = database.get_collection("songs_collection")
audiobook_collection = database.get_collection("audiobooks_collection")
podcast_collection = database.get_collection("podcasts_collection")

Audio_list = [song_collection,audiobook_collection,podcast_collection]


def song_helper(song) -> dict:
    return {
        "id": str(song["_id"]),
        "name": song["name"],
        "duration": song["duration"],
        "upload": song["upload"],
        "audio_type":"song"

    }


def audiobook_helper(audiobook) -> dict:
    return {
        "id": str(audiobook["_id"]),
        "title": audiobook["title"],
        "author": audiobook["author"],
        "duration": audiobook["duration"],
        "upload": audiobook["upload"],
        "audio_type": "audiobook"

    }


def podcast_helper(podcast) -> dict:
    return {
        "id": str(podcast["_id"]),
        "name": podcast["name"],
        "duration": podcast["duration"],
        "upload": podcast["upload"],
        "host": podcast["host"],
        "participents": podcast["participents"],
        "audio_type": "podcast"

    }
async def audiofiles():
    audios = []
    for audio_type in Audio_list:
        if audio_type == song_collection:

            async for song in audio_type.find():
                audios.append(song_helper(song))

        elif audio_type == audiobook_collection:

            async for audiobook in audio_type.find():
                audios.append(audiobook_helper(audiobook))
        else:
            async for podcast in audio_type.find():
                audios.append(podcast_helper(podcast))
    return audios


# Add a new audio into to the database
async def add_song(song_data: dict) -> dict:
    song = await song_collection.insert_one(song_data)
    new_song = await song_collection.find_one({"_id": song.inserted_id})
    return song_helper(new_song)
async def add_podcast(podcast_data: dict) -> dict:
    podcast = await podcast_collection.insert_one(podcast_data)
    new_podcast = await podcast_collection.find_one({"_id": podcast.inserted_id})
    return podcast_helper(new_podcast)
async def add_audiobook(audiobook_data: dict) -> dict:
    audiobook = await audiobook_collection.insert_one(audiobook_data)
    new_audiobook = await audiobook_collection.find_one({"_id": audiobook.inserted_id})
    return audiobook_helper(new_audiobook)


# Retrieve an audio with a matching ID
async def retrieve_audio(id: str) -> dict:
    for datas in Audio_list:
       audio = await datas.find_one({"_id": ObjectId(id)})
       if audio:
           if datas.name== "songs_collection":
               return song_helper(audio)


           elif datas.name== "podcasts_collection":
                return podcast_helper(audio)
           elif datas.name== "audiobooks_collection":
                return audiobook_helper(audio)



# Update an audio with a matching ID
async def update_audio(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    for datas in Audio_list:
        audio = await datas.find_one({"_id": ObjectId(id)})
        if audio:
            if datas.name == "songs_collection":
                updated_audio = await song_collection.update_one(
                    {"_id": ObjectId(id)}, {"$set": data}
                )
                if updated_audio:
                    return True
                return False


            elif datas.name == "podcasts_collection":
                updated_audio = await podcast_collection.update_one(
                    {"_id": ObjectId(id)}, {"$set": data}
                )
                if updated_audio:
                    return True
                return False
            elif datas.name == "audiobooks_collection":
                updated_audio = await audiobook_collection.update_one(
                    {"_id": ObjectId(id)}, {"$set": data}
                )
                if updated_audio:
                    return True
                return False





# Delete an audio from the database
async def delete_audio(id: str):

    for datas in Audio_list:
       audio = await datas.find_one({"_id": ObjectId(id)})
       if audio:
           if datas.name== "songs_collection":
               await song_collection.delete_one({"_id": ObjectId(id)})
               return True


           elif datas.name== "podcasts_collection":
               await podcast_collection.delete_one({"_id": ObjectId(id)})
               return True
           elif datas.name== "audiobooks_collection":
               await audiobook_collection.delete_one({"_id": ObjectId(id)})
               return True




