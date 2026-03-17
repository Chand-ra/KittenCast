import argparse
import sys
from kittencast.compiler import build_audiobook

def main():
    parser = argparse.ArgumentParser(
        prog="kittencast",
        description="Compile documents (.epub, .pdf, .docx, .txt) into Audiobooks locally."
    )
    parser.add_argument("input_file", help="Path to the document file")
    parser.add_argument("-o", "--out-dir", default="Audiobook_Output", help="Output directory")
    parser.add_argument("-v", "--voice", default="Jasper", 
                        choices=['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo'])
    parser.add_argument("-m", "--model", default="KittenML/kitten-tts-nano-0.8",
                        choices=["KittenML/kitten-tts-nano-0.8", "KittenML/kitten-tts-micro-0.8", "KittenML/kitten-tts-mini-0.8"])
    
    # --- Dump text argument, helps with testing ---
    parser.add_argument("-d", "--dump-text", action="store_true", 
                        help="Save the extracted text to a .txt file for debugging before synthesis")
    
    args = parser.parse_args()
    
    try:
        build_audiobook(args.input_file, args.out_dir, args.voice, args.model, args.dump_text)
        print("\nSuccess: Audiobook compiled.")
    except KeyboardInterrupt:
        print("\nProcess aborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()