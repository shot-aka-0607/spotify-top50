import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 認証設定
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="081a2d8bf2e04e61b79032cd94706eec",
    client_secret="2901037299cf4dc3bc5a202b8245b218",
    redirect_uri="http://127.0.0.1:8000/callback",
    scope="playlist-modify-public user-top-read"
))

user_id = sp.me()["id"]
playlist_name = "6months Top50"

# トップ50を取得
top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")
track_uris = [track["uri"] for track in top_tracks["items"]]

# 既存プレイリストを検索
playlists = sp.current_user_playlists()
playlist_id = None
for playlist in playlists["items"]:
    if playlist["name"] == playlist_name:
        playlist_id = playlist["id"]
        break

# なければ作成
if not playlist_id:
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlist["id"]

# 最新のトップ50で上書き
sp.playlist_replace_items(playlist_id, track_uris)

print("✅ 最新のトップ50でプレイリストを更新しました！")
