import os
os.environ['MPLBACKEND'] = 'Agg' 

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
        TTS.config.shared_configs.BaseDatasetConfig
    ])
except Exception:
    pass

import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from TTS.api import TTS

def main():
    print("🤖 sakoroid システム（XTTS v2 ボイスクローニング）起動中...")
    
    # 1. Geminiにセリフを考えてもらう
    client = genai.Client()
    prompt = "「sakoroidの起動に成功しました」というセリフを、1文で短く、人間の女の子っぽく可愛いらしく言ってください。セリフの文字だけを出力してください。"
    
    ai_text = "sakoroid、起動できたよ！"
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            ai_text = response.text.strip()
            break
        except ServerError:
            time.sleep(3)

    print(f"🤖 Geminiの思考セリフ: {ai_text}")
    
    # 2. Coqui TTS（XTTS v2）を起動
    print("⏳ AI音声モデルを読み込み中...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # 3. 本人の声（target.wav）を分析して、その声で喋らせる！
    # ※プログラムと同じ場所に target.wav を置いておく必要があります
    reference_wav = "/content/sakoroid/sakoroid/target.wav" 
    
    if not os.path.exists(reference_wav):
        # フォルダがずれていた場合のバックアップ確認
        reference_wav = "target.wav"
        
    print(f"👤 本人の声（{reference_wav}）を分析してクローニング中...")
    
    tts.tts_to_file(
        text=ai_text,
        language="ja",              
        file_path="output.wav",
        speaker_wav=reference_wav, # ← ここで本人の声を指定！speaker引数は不要になります
    )
    print("🎉 本人の声を完全に再現した output.wav が作成されました！")

if __name__ == "__main__":
    main()