import os
import numpy as np
import soundfile as sf
from tqdm import tqdm
from kittentts import KittenTTS
from kittencast.text_utils import extract_document, split_text

def build_audiobook(input_path: str, output_dir: str, voice: str, model_name: str, dump_text: bool = False):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extracting text from {input_path}...")
    chapters = extract_document(input_path)
    
    if not chapters:
        print("Error: No readable text found in the document.")
        return

    # --- NEW: Text Dumping Logic ---
    if dump_text:
        dump_path = os.path.join(output_dir, "extracted_text_dump.txt")
        print(f"Dumping processed text to {dump_path}...")
        with open(dump_path, "w", encoding="utf-8") as f:
            for i, chapter in enumerate(chapters):
                f.write(f"--- Section {i+1} ---\n\n")
                f.write(chapter)
                f.write("\n\n")

    print(f"Loading TTS Model: {model_name}...")
    engine = KittenTTS(model_name)
    sample_rate = 24000
    
    for i, chapter_text in enumerate(chapters):
        print(f"\nProcessing Section {i+1}/{len(chapters)}")
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
            out_file = os.path.join(output_dir, f"Section_{i+1:03d}.wav")
            sf.write(out_file, final_audio, sample_rate)