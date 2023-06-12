from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import youtube_routes

app = FastAPI()

# Mount the static files directory
#app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")




app.include_router(youtube_routes.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
