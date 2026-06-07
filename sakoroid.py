# 1. 【最優先】画面描画のバグを封じ込める
import os
os.environ['MPLBACKEND'] = 'Agg' 

# 2. 【最重要】PyTorchのセキュリティ検問を一括解除する
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

# 3. その他のライブラリを読み込む
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from TTS.api import TTS

def main():
    print("🤖 sakoroid システム（XTTS v2）起動中...")
    
    # 1. Geminiにセリフを考えてもらう（リトライ機能付き）
    client = genai.Client()
    prompt = "「sakoroidの起動に成功しました」というセリフを、1文で短く、人間の女の子っぽく可愛いらしく言ってください。セリフの文字だけを出力してください。"
    
    ai_text = "sakoroid、起動できたよ！" # 万が一のときのバックアップセリフ
    
    for attempt in range(3):
        try:
            print(f"⏳ Geminiが思考中... (試行 {attempt + 1}/3)")
            response = client.models.generate_content(
                model='gemini-2.5-flash', # 公式100%サポートの本命モデル
                contents=prompt
            )
            ai_text = response.text.strip()
            break
        except ServerError as e:
            if "503" in str(e) and attempt < 2:
                print("⚠️ Googleのサーバーが混雑しています。3秒後に自動で再接続します...")
                time.sleep(3)
                continue
            raise e

    print(f"🤖 Geminiの思考セリフ: {ai_text}")
    
    # 2. Coqui TTS（XTTS v2）の超リアルAIを起動
    print("⏳ AI音声モデルを読み込み中...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # 3. 内蔵されている女性の声を使って喋らせる
    print("📣 音声データを生成中...")
    
    # 【超安全対策】モデルが持っているスピーカー名リストから、最初の1人（確実にある声）を自動取得
    available_speakers = tts.speakers
    chosen_speaker = "Aura Rachel" if "Aura Rachel" in available_speakers else available_speakers[0]
    print(f"👤 使用するスピーカー: {chosen_speaker}")

    tts.tts_to_file(
        text=ai_text,
        speaker=chosen_speaker,  # ← 自動選択された確実に存在する声をセット！
        language="ja",              
        file_path="output.wav"      
    )
    print("🎉 本物の人間そっくりの output.wav が作成されました！")

if __name__ == "__main__":
    main()