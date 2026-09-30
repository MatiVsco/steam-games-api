import requests

appids = [730, 440, 570, 543987589045678080, 304930, 578080, 252490, 238960, 292030, 252950, 271590]


def fetch_games():
    games = []
    for appid in appids:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        
        try:
            response = requests.get(url, timeout=5)  # Set a timeout for the request
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException:
            continue  # Skip this appid if there's an error with the request
        
        try:
            data = response.json()
        except ValueError:
            continue

        if data[str(appid)]['success']:
            app_data = data[str(appid)]['data']
            app_name = app_data['name']
            app_price = app_data['price_overview']['final'] / 100 if 'price_overview' in app_data else None
            release_date = app_data['release_date']['date'] if 'release_date' in app_data else None
            
            if app_name is not None:
                games.append({
                        'id': appid,
                        'name': app_name,
                        'price': app_price,
                        'release_date': release_date
                })
            else:
                continue
    return games
