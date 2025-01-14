from openai import OpenAI
import json


def generate_game_recommendations(api_key, recent_games_list, most_played_games_list, displayed_games):
    """
    openAIにプレイしたゲームを渡し、関連するゲームを返してもらう。
    """
    client = OpenAI(api_key=api_key)
    system = (
        "あなたはゲームの推薦システムです。\n"
        "出力は必ず以下のJSON形式で返してください。\n"
        "処理の中でデータをパースするので、不要な文言は一切不要です。"
    )
    prompt = (
        "最近遊んだゲームと累計プレイ時間の情報をもとに、"
        "最もジャンルや種類が関連するゲームを5個紹介してください。\n\n"
        "最近遊んだゲーム:\n" +
        "\n".join([f"{game['name']} - 過去2週間: {game['playtime_2weeks']} 時間" for game in recent_games_list]) +
        "\n\n累計プレイ時間トップゲーム:\n" +
        "\n".join([f"{game['name']} - 累計: {game['playtime_forever']} 時間" for game in most_played_games_list]) +
        "\n\nすでに紹介したゲームは以下です。このリストに含まれるゲームは除外してください:\n" +
        "\n".join([f"{game['title']}" for game in displayed_games]) +
        "\n\n出力は必ず以下のJSON形式で返してください。\n"
        "[\n"
        "  {\"title\": \"ゲームタイトル\", \"genre\": \"ジャンル\", \"url\": \"リンク\"},\n"
        "]"
    )
    try:
        # Chat APIを呼び出す
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        # レスポンスからメッセージの内容を取得
        raw_content = response.choices[0].message.content.strip()

        # JSON形式に変換して返却
        return json.loads(raw_content)

    except json.JSONDecodeError as json_error:
        raise RuntimeError(f"OpenAI APIからのレスポンスが無効なJSON形式です: {json_error}")
    except Exception as e:
        raise RuntimeError(f"OpenAI APIエラー: {e}")
