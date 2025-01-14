import streamlit as st
from utils.env_loader import load_env
from services.steam_service import get_recently_played_games, get_most_played_games
from services.openai_service import generate_game_recommendations


def main():
    # タイトルを設定
    st.title("🎮 おすすめゲーム紹介BOT 🎮")

    # APIキーのロード
    try:
        steam_key, openai_key = load_env()
    except Exception as e:
        st.error(f"環境変数の読み込みに失敗しました: {e}")
        return

    # SteamユーザーIDの入力
    steam_id = st.text_input("SteamユーザーIDを入力してください:", "76561198293569386")

    # 初期化
    if "displayed_games" not in st.session_state:
        st.session_state["displayed_games"] = []  # すでに表示したゲームを追跡
    if "recommendation_shown" not in st.session_state:
        st.session_state["recommendation_shown"] = False  # おすすめリストが表示されたかを追跡

    # ボタンが押されたら処理を実行
    if st.button("おすすめゲームを紹介"):
        # 最近遊んだゲームを取得
        recent_games = get_recently_played_games(steam_key, steam_id) or []
        most_played_games = get_most_played_games(steam_key, steam_id) or [] 

        # OpenAIでおすすめゲームを取得
        if recent_games or most_played_games:
            st.subheader("🤖 おすすめのゲーム 🤖")
            try:
                recommendations = generate_game_recommendations(
                    openai_key,
                    recent_games,
                    most_played_games,
                    st.session_state["displayed_games"]
                )
                st.session_state["displayed_games"].extend(recommendations)
                display_recommendations(recommendations)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.info("データが不足しているため、おすすめを生成できません。")


def display_recommendations(recommendations):
    """
    ゲームのリストを表示する。
    """
    if not recommendations:
        st.info("新しいおすすめゲームはありません。")
        return

    for idx, game in enumerate(recommendations, start=1):
        st.write(f"{idx}つめ")
        st.write(f"**タイトル**: {game['title']}")
        st.write(f"**ジャンル**: {game['genre']}")
        st.markdown(f"**URL**: [ストアページはこちら]({game['url']})")
        st.divider()


if __name__ == "__main__":
    main()
