import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# 認証情報を環境変数から取得
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

# 1. market="JP" を指定して日本の楽曲データを確実に取得する
results = sp.playlist_items(source_playlist_id, limit=50, market="JP")

items = results.get("items", [])
print(f"取得した生のアイテム数: {len(items)}件")

valid_uris = []
for item in items:
    if not item:
        continue

    # 新仕様の "item" キーを最優先し、旧仕様 "track" / "episode" をフォールバックにする
    track_data = item.get("item") or item.get("track") or item.get("episode")
    
    if track_data and isinstance(track_data, dict):
        uri = track_data.get("uri")
        if uri:
            valid_uris.append(uri)
    
    # 30曲集まった時点で終了
    if len(valid_uris) == 30:
        break

# 2. ターゲットプレイリストに反映
if valid_uris:
    sp.playlist_replace_items(target_playlist_id, valid_uris)
    print(f"プレイリスト「KAWAII LAB. Top30」を更新しました（{len(valid_uris)}曲反映）")
else:
    print("エラー: 有効なトラックを取得できませんでした。プレイリストIDまたは権限を確認してください。")
