from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from audio_server.routes.api_routes import router as AudioRouter

app = FastAPI()

app.include_router(AudioRouter, tags=["Audio"], prefix="/api")
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/", tags=["Root"])
async def read_root():
    return {"Welcome to this Audio Server!!!"}
