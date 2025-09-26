# get_refresh_token.py
# ローカル（Mac）で1回だけ実行して refresh_token を出力するスクリプト

import os
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "081a2d8bf2e04e61b79032cd94706eec"
CLIENT_SECRET = "2901037299cf4dc3bc5a202b8245b218"
REDIRECT_URI = "http://127.0.0.1:8000/callback"
SCOPE = "playlist-modify-public user-top-read"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

auth_url = sp_oauth.get_authorize_url()
print("1) ブラウザで次のURLを開いて認可してください:\n")
print(auth_url)
print("\n2) 認可後にリダイレクトされたフルURLをここに貼り付けて Enter を押してください。")
redirected = input("Redirected URL: ").strip()

code = sp_oauth.parse_response_code(redirected)
token_info = sp_oauth.get_access_token(code)  # Spotipy のバージョンによっては戻りが dict の場合あり
# token_info は dict または tuple になるバージョン差があるため安全に取得
if isinstance(token_info, dict):
    refresh_token = token_info.get("refresh_token")
else:
    # 古いバージョンで tuple の場合
    refresh_token = token_info[1].get("refresh_token") if len(token_info) > 1 else None

print("\n--- 取得した refresh_token ---\n")
print(refresh_token)
print("\n--- これを GitHub のリポジトリ Secrets に保存してください ---")

