# Steam Games API

A REST API built with Python and FastAPI that retrieves game information from the Steam Store API and provides endpoints for searching, filtering, sorting, and limiting results.

## Features

- Retrieve a list of Steam games
- Search games by name
- Sort games by price
- Sort games by release date
- Limit the number of returned games
- Retrieve a specific game using its Steam AppID
- Return appropriate HTTP errors when a game is not found
- Health-check endpoint
- Automated tests with pytest
- Mocked external API requests during testing

## Technologies

- Python
- FastAPI
- Pydantic
- Requests
- Pytest
- Steam Store API

## API Endpoints

### `GET /games`

Returns the available games.

#### Query Parameters

- `name` — filters games by name
- `sort_by` — sorts by `price` or `release_date`
- `limit` — limits the number of results

Example:

```text
GET /games?name=counter&sort_by=price&limit=5
```

### `GET /games/{appid}`

Returns a specific game using its Steam AppID.

Example:

```text
GET /games/730
```

### `GET /health`

Returns the API health status.

Example response:

```json
{
    "status": "ok"
}
```

## Running the Project

Install the required dependencies:

```bash
pip install fastapi uvicorn requests pytest
```

Start the API with:

```bash
uvicorn steam_games:app --reload
```

The API will be available at the local server address shown by Uvicorn.

FastAPI also provides interactive API documentation.

## Running Tests

Run:

```bash
python -m pytest
```

The test suite covers:

- API endpoints
- HTTP errors
- Query parameter validation
- Result limiting
- Steam API success responses
- Unsuccessful Steam responses
- Request errors
- Invalid JSON responses

External Steam API calls are mocked during tests so the tests remain fast and independent of the real Steam service.

## Project Structure

```text
steam-games-api/
├── game_model.py
├── services.py
├── steam_games.py
├── test_steam_games.py
├── README.md
└── .gitignore
```

## What I Practiced

This project was built to practice:

- Building REST APIs with FastAPI
- Pydantic models and validation
- Query parameters
- HTTP status codes and exceptions
- Separating API logic from external-service logic
- Working with external APIs
- Error handling
- Automated testing with pytest
- Mocking external dependencies