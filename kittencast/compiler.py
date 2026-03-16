import os
import numpy as np
import soundfile as sf
from tqdm import tqdm
from kittentts import KittenTTS
from kittencast.text_utils import extract_chapters, split_text

def build_audiobook(epub_path: str, output_dir: str, voice: str, model_name: str):
    os.makedirs(output_dir, exist_ok=True)
    chapters = extract_chapters(epub_path)
    
    print(f"Loading TTS Model: {model_name}...")
    engine = KittenTTS(model_name)
    sample_rate = 24000
    
    for i, chapter_text in enumerate(chapters):
        print(f"\nProcessing Chapter {i+1}/{len(chapters)}")
        chunks = split_text(chapter_text)
        chapter_audio = []
        silence = np.zeros(int(sample_rate * 0.4))
        
        for chunk in tqdm(chunks, desc="Synthesizing", unit="chunk"):
            try:
                audio_chunk = engine.generate(chunk, voice=voice)
                chapter_audio.extend([audio_chunk, silence])
            except Exception as e:
                print(f"\nSkipping chunk due to error: {e}")
                
        if chapter_audio:
            final_audio = np.concatenate(chapter_audio)
            out_file = os.path.join(output_dir, f"Chapter_{i+1:02d}.wav")
            sf.write(out_file, final_audio, sample_rate)