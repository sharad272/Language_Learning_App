from fastapi import APIRouter, Request,requests
from fastapi.templating import Jinja2Templates
from cachetools import TTLCache
from fastapi.responses import JSONResponse
from functools import wraps


from app.services.youtube_service import get_channel_id, get_channel_playlists

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")
cache = TTLCache(maxsize=100, ttl=60)



def cache_response(ttl: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if request.url.path in cache:
                response_data = cache[request.url.path]
                return response_data

            response = await func(request, *args, **kwargs)
            if isinstance(response, JSONResponse):
                response_data = response.json()
                cache[request.url.path] = response_data
            return response

        return wrapper

    return decorator



@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@router.get('/german')
@cache_response(ttl=300)
async def german_playlists(request: Request):
    channel_name = 'lingoniGERMAN'
    channel_id = await get_channel_id(channel_name)
    if channel_id:
        playlist_ids = [
            'PL5QyCnFPRx0GxaFjdAVkx7K9TfEklY4sg',
            'PL5QyCnFPRx0G34DRN9b5MDwsUQoxIbg6c',
            'PL5QyCnFPRx0HwdFq5hG3B47NCsaAaJN17'
        ]
        playlists = await get_channel_playlists(playlist_ids)
        return templates.TemplateResponse('playlists.html', {'request': request, 'playlists': playlists})
    else:
        return templates.TemplateResponse('error.html', {'request': request, 'error_message': 'Channel not found'})


@router.get('/french')
@cache_response(ttl=300)
async def french_playlists(request: Request):
    channel_name = 'learnfrenchwithalexa'
    channel_id = await get_channel_id(channel_name)
    if channel_id:
        playlist_ids = [
            'PLV1-QgpUU7N2TVWS6gEVMqEfAFjAl-DV6'
        ]
        playlists = await get_channel_playlists(playlist_ids)
        return templates.TemplateResponse('playlists.html', {'request': request, 'playlists': playlists})
    else:
        return templates.TemplateResponse('error.html', {'request': request, 'error_message': 'Channel not found'})
