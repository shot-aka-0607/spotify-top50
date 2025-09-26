# top50_4weeks.py
import os
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8000/callback")
REFRESH_TOKEN = os.environ.get("SPOTIPY_REFRESH_TOKEN")

if not CLIENT_ID or not CLIENT_SECRET:
    logger.error("SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET not set.")
    sys.exit(1)

SCOPE = "playlist-modify-public user-top-read"

if REFRESH_TOKEN:
    # 非対話: 保持している refresh_token でアクセストークンを更新
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)
    access_token = token_info["access_token"]
    sp = Spotify(auth=access_token)
else:
    # ローカルで手動認証して cache を使う場合
    sp = Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

# --- ここから既存のトップ50取得＆プレイリスト上書き処理 ---
user = sp.me()
user_id = user["id"]
playlist_name = "4weeks Top50"

# 時間範囲の例： short_term / medium_term / long_term
time_ranges = ["short_term"]  # 必要なら ["short_term","medium_term","long_term"] に拡張

# ここでは short_term を使って上書き。あなたの既存ロジックに差し替えてください。
top_tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")
track_uris = [t["uri"] for t in top_tracks["items"]]

# プレイリスト検索
playlist_id = None
for p in sp.current_user_playlists(limit=50)["items"]:
    if p["name"] == playlist_name:
        playlist_id = p["id"]
        break

if not playlist_id:
    created = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = created["id"]

sp.playlist_replace_items(playlist_id, track_uris)
logger.info("プレイリストを更新しました: %s (tracks=%d)", playlist_name, len(track_uris))
