from fastapi import FastAPI, Query, HTTPException
from game_model import Game, SortOption
from services import fetch_games
from datetime import datetime


app = FastAPI()
     
@app.get("/games", response_model=list[Game])
def get_games(name: str | None = None, sort_by: SortOption | None = None, limit: int | None = Query(default=None, gt=0)):
     games = fetch_games()
     
     #FILTER 
     if name is not None:
         filtered_games = []
         for game in games:
             if name.lower() in game['name'].lower():
                 filtered_games.append(game)
         games = filtered_games
     
     #SORT
     if sort_by == SortOption.price:
         games = sorted(games, key=lambda x: (x['price'] is not None, x['price']))
     elif sort_by == SortOption.release_date:
        games = sorted(
        games,
        key=lambda x: (
            x["release_date"] is None,
            datetime.strptime(x["release_date"], "%b %d, %Y")
            if x["release_date"] is not None
            else datetime.min
        )
    )

     #LIMIT
     if limit is not None:
         games = games[:limit]

     return games


@app.get("/games/{appid}", response_model=Game)
def get_game(appid: int):
     games = fetch_games()
     for game in games:
         if game['id'] == appid:
             return game
     raise HTTPException(status_code=404, detail="Game not found")


@app.get("/health")
def health_check():
     return {"status": "ok"}