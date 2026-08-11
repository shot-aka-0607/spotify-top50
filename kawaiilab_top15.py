import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# 認証情報
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8000/callback")
REFRESH_TOKEN = os.environ["SPOTIPY_REFRESH_TOKEN"]

SCOPE = "playlist-modify-private playlist-read-private"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)
token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)
sp = Spotify(auth=token_info["access_token"])

source_playlist_id = "07kXPcjIqWw5DUT4Ybsdod"
target_playlist_id = "1anCYH7pLqOzgW7F53Kn0M"

# 1. 配信停止曲などで目減りすることを見越し、余裕を持って50件取得
results = sp.playlist_items(source_playlist_id, limit=50)

valid_uris = []
for item in results.get("items", []):
    # ポッドキャスト等の場合(episode)も含めてチェック
    track_data = item.get("track") or item.get("episode")
    
    # 有効なトラック（URIが存在する）のみを追加
    if track_data and track_data.get("uri"):
        valid_uris.append(track_data["uri"])
    
    # 目的の「30曲」が集まった時点で抽出を終了
    if len(valid_uris) == 30:
        break

# 2. きっちり30曲揃ったか確認して置き換え
if len(valid_uris) > 0:
    sp.playlist_replace_items(target_playlist_id, valid_uris)
    print(f"プレイリスト「KAWAII LAB. Top30」を更新しました（{len(valid_uris)}曲反映）")
    
    if len(valid_uris) < 30:
        print(f"※元プレイリスト内に有効な曲が{len(valid_uris)}曲しか存在しませんでした。")
else:
    print("有効なトラックが1曲も見つかりませんでした。")
