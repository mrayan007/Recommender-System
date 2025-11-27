from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    isOffer: Union[bool, None] = None
