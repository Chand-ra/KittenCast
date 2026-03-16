import argparse
import sys
from kittencast.compiler import build_audiobook

def main():
    parser = argparse.ArgumentParser(
        prog="kittencast",
        description="Compile EPUB files into Audiobooks locally."
    )
    parser.add_argument("epub_file", help="Path to the .epub file")
    parser.add_argument("-o", "--out-dir", default="Audiobook_Output", help="Output directory")
    parser.add_argument("-v", "--voice", default="Jasper", 
                        choices=['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo'])
    parser.add_argument("-m", "--model", default="KittenML/kitten-tts-nano-0.8",
                        choices=["KittenML/kitten-tts-nano-0.8", "KittenML/kitten-tts-micro-0.8", "KittenML/kitten-tts-mini-0.8"])
    
    args = parser.parse_args()
    
    try:
        build_audiobook(args.epub_file, args.out_dir, args.voice, args.model)
        print("\nSuccess: Audiobook compiled.")
    except KeyboardInterrupt:
        print("\nProcess aborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()