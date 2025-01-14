from dotenv import load_dotenv
import os


def load_env():
    load_dotenv()
    steam_api_key = os.getenv("STEAM_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not steam_api_key or not openai_api_key:
        raise EnvironmentError("APIキーが設定されていません。`.env`ファイルを確認してください。")
    return steam_api_key, openai_api_key
