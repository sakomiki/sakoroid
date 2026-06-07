import os
from google import genai

def main():
    print("🤖 sakoroid システム起動中...")
    
    # 1. Gemini CLIと同じ仕組みでGeminiを呼び出す
    # (Colab側で実行するときは自動で環境変数からキーを読み込みます)
    client = genai.Client()
    
    prompt = "「sakoroidの起動に成功しました」というセリフを、1文で短く、少し可愛いAIロボット風に言ってください。"
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    
    ai_text = response.text.strip()
    print(f"🤖 Geminiの思考: {ai_text}")
    
    # 2. テストとして、Linux（Colab）の音声合成コマンドで喋らせるファイルを作る
    print("📣 音声データの生成準備...")
    # ※あとでここにCoqui TTS（XTTS）や自分の声のモデルを組み込みます！
    os.system(f'espeak -v mb-it1 "{ai_text}" -w output.wav')
    print("🎉 output.wav が作成されました！")

if __name__ == "__main__":
    main()