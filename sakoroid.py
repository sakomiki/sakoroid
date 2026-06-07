import os
import torch
from google import genai
from TTS.api import TTS

def main():
    print("🤖 sakoroid システム（XTTS v2）起動中...")
    
    # 1. Geminiにセリフを考えてもらう
    client = genai.Client()
    prompt = "「sakoroidの起動に成功しました」というセリフを、1文で短く、人間の女の子っぽく可愛いらしく言ってください。セリフの文字だけを出力してください（解説や挨拶は不要です）。"
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    ai_text = response.text.strip()
    print(f"🤖 Geminiの思考セリフ: {ai_text}")
    
    # 2. Coqui TTS（XTTS v2）の超リアルAIを起動
    print("⏳ AI音声モデルを読み込み中（初回はダウンロードに1分ほどかかります）...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # 3. あなたの声（またはサンプルの声）を元に、人間らしい抑揚で喋らせる！
    print("📣 自分の声（クローン）で音声データを生成中...")
    
    # ※もし自分の声の「my_voice.wav」があればそれを指定します。
    # 最初はテストとして、AIモデルに内蔵されているデフォルトの女性の声（スピーカー）を借りて喋らせます。
    tts.tts_to_file(
        text=ai_text,
        speaker_wav="my_voice.wav", # 内蔵されている人間らしい声の持ち主
        language="ja",              # 日本語を指定
        file_path="output.wav"      # 完成した音声の保存先
    )
    print("🎉 本物の人間そっくりの output.wav が作成されました！")

if __name__ == "__main__":
    main()