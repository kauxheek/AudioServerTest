import uvicorn

if __name__ == "__main__":
    uvicorn.run("audio_server.index:app",reload=True)