from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
script_dir = os.path.dirname(__file__)
app = FastAPI()
st_abs_file_path = os.path.join(script_dir, "app/static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
print(st_abs_file_path)
