# 1. 【最優先】何が何でも一番最初に画面描画のバグを封じ込める
import os
os.environ['MPLBACKEND'] = 'Agg' 

# 2. 【2番目】その次にPyTorchのセキュリティブロックを解除する
import torch
try:
    import TTS.tts.configs.xtts_config
    torch.serialization.add_safe_globals([TTS.tts.configs.xtts_config.XttsConfig])
except Exception:
    pass # まだインポートできない場合はスルーして後乗せする

# 3. 【3番目】その他のライブラリを読み込む
from google import genai
from google.genai import types
from TTS.api import TTS

def main():
    print("🤖 sakoroid システム（XTTS v2）起動中...")
    
    # 1. Geminiにセリフを考えてもらう
    client = genai.Client()
    prompt = "「sakoroidの起動に成功しました」というセリフを、1文で短く、人間の女の子っぽく可愛いらしく言ってください。セリフの文字だけを出力してください。"
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
    
    # 3. 内蔵されている女性の声を使って喋らせる
    print("📣 音声データを生成中...")
    tts.tts_to_file(
        text=ai_text,
        speaker_name="Anais Betts", 
        language="ja",              
        file_path="output.wav"      
    )
    print("🎉 本物の人間そっくりの output.wav が作成されました！")

if __name__ == "__main__":
    main()