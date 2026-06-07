# sakoroid

# 1. あなたの情報に変数を書き換えてください
GITHUB_USER = "sakomiki"
GITHUB_TOKEN = "github_pat_"
REPO_NAME = "sakoroid"

# 2. 通行証（トークン）を使って、安全にPrivate倉庫からクローンします
!git clone https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git

# 3. sakoroidのフォルダに移動して自動構築
%cd {REPO_NAME}
!pip install -r requirements.txt

print("🎉 パスワードなしでPrivate倉庫から自動構築が完了しました！")