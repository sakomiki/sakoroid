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

from TTS.api import TTS

def main():
    print("🤖 sakoroid システム（黒棺・スタンドアロン詠唱モード）起動中...")
    
    # 【変更点】Geminiは完全廃止！喋らせたいセリフをここに直接固定
    ai_text = "にじみだすこんだくのもんしょう。ふそんなるきょうきのうつわ。わきあがり・ひていし・しびれ・またたき・ねむりをさまたげる。はこうするてつのおうじょ。たえずじかいするどろのにんぎょう。けつごうせよ、はんぱつせよ。ちにみちおのれのむりょくをしれ‼ はどうのきゅうじゅう:くろひつぎ"
    
    print(f"📖 詠唱テキスト: {ai_text}")
    
    # 1. Coqui TTS（XTTS v2）を起動
    print("⏳ AI音声モデルを読み込み中...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # 2. 本人の声（target.wav）を分析してクローニング
    reference_wav = "/content/sakoroid/target.wav" 
    if not os.path.exists(reference_wav):
        reference_wav = "target.wav"
        
    print(f"👤 本人の声（{reference_wav}）を分析してクローニング中...")
    
    tts.tts_to_file(
        text=ai_text,
        language="ja",              
        file_path="output.wav",
        speaker_wav=reference_wav,
        
        # ↓↓↓ パラメーター調整ツマミ（お好みで数値を調整してください！） ↓↓↓
        temperature=0.75,   # 話し方の感情・ランダム性（0.1〜1.0）
        speed=1.0,          # 話す速度
    )
    print("🎉 本人の声での『黒棺』完全詠唱 output.wav が作成されました！")

if __name__ == "__main__":
    main()