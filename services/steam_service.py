import requests


def get_recently_played_games(steam_key, steam_id):
    """
    最近遊んだゲームをSteam APIから取得する。
    """
    url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    params = {
        "key": steam_key,
        "steamid": steam_id,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "games" in data["response"]:
            return [
                {
                    "name": game["name"],
                    "playtime_2weeks": game.get("playtime_2weeks", 0) // 60  # 分を時間に変換
                }
                for game in data["response"]["games"][:30]
            ]
    return []


def get_most_played_games(steam_key, steam_id):
    """
    累計プレイ時間が長いゲームをSteam APIから取得する。
    """
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": steam_key,
        "steamid": steam_id,
        "include_appinfo": True,  # ゲーム名を取得するためのオプション
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "games" in data["response"]:
            most_played_games = sorted(
                data["response"]["games"], key=lambda x: x.get("playtime_forever", 0), reverse=True
            )
            return [
                {
                    "name": game["name"],
                    "playtime_forever": game["playtime_forever"] // 60  # 分を時間に変換
                }
                for game in most_played_games[:30]
            ]
    return []
