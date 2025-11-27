# from typing import Union

from fastapi import FastAPI

# models
# from models import Item

app = FastAPI()


@app.get("/get")
def get():
    return "GET Endpoint"
