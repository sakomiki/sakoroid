# 1. 【最優先】画面描画のバグを封じ込める
import os
os.environ['MPLBACKEND'] = 'Agg' 

# 2. 【最重要】PyTorchのセキュリティ検問（すべてのConfigを一網打尽にする）
import torch
try:
    import TTS.tts.configs.xtts_config
    import TTS.tts.models.xtts
    import TTS.config.shared_configs
    
    torch.serialization.add_safe_globals([
        TTS.tts.configs.xtts_config.XttsConfig,
        TTS.tts.models.xtts.XttsAudioConfig,
        TTS.tts.models.xtts.XttsArgs,
        TTS.config.shared_configs.BaseAudioConfig,
        TTS.config.shared_configs.BaseDatasetConfig  # ←【これを追加！】
    ])
except Exception:
    pass

# 3. その他のライブラリを読み込む
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
    print("⏳ AI音声モデルを読み込み中...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # 3. 内蔵されている女性の声を使って喋らせる
    print("📣 音声データを生成中...")
    tts.tts_to_file(
        text=ai_text,
        speaker="Anais Betts",  # ← 【ここを speaker_name から speaker に変更！】
        language="ja",              
        file_path="output.wav"      
    )
    print("🎉 本物の人間そっくりの output.wav が作成されました！")

if __name__ == "__main__":
    main()