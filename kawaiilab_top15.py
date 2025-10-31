import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# 認証情報を環境変数から取得
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8000/callback")
REFRESH_TOKEN = os.environ["SPOTIPY_REFRESH_TOKEN"]

SCOPE = "playlist-modify-private playlist-read-private"

# 非対話で refresh_token を使って認証
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI, scope=SCOPE)
token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)
sp = Spotify(auth=token_info["access_token"])

# --- 上位20曲を抽出したいプレイリスト ---
source_playlist_id = "07kXPcjIqWw5DUT4Ybsdod"  # 置き換え
target_playlist_id = "1anCYH7pLqOzgW7F53Kn0M"  # 置き換え

# 1. 上位20曲取得
results = sp.playlist_items(source_playlist_id, limit=20)
track_uris = [item["track"]["uri"] for item in results["items"]]

# 2. 別プレイリストに上書き
sp.playlist_replace_items(target_playlist_id, track_uris)

print(f"プレイリスト「KAWAII LAB. Top20」を更新しました（{len(track_uris)}曲）")

