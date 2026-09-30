from pydantic import BaseModel
from enum import Enum

class Game(BaseModel):
    id: int
    name: str 
    price: float | None
    release_date: str | None
    
class SortOption(str, Enum):
    price = "price"
    release_date = "release_date"