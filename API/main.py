# from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# models
# from models import Item

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get():
    return "Hello, World!"
