# KittenCast 🎧

A lightweight, local, command-line compiler that transforms your documents (.epub, .pdf, .docx, .txt) into high-quality audiobooks using [KittenTTS](https://github.com/KittenML/KittenTTS).

KittenCast is built to run entirely offline on your CPU, featuring intelligent text chunking, automated file routing, and a beautiful progress interface.

## ✨ Features

* **Multi-Format Support:** Automatically extracts and cleans text from EPUB, PDF, DOCX, and TXT files.
* **Smart Chunking:** Uses NLTK natural language processing to split text cleanly at sentence boundaries, preventing mid-word cutoffs and TTS audio artifacts.
* **100% Local & Private:** No API keys, no cloud processing, no DRM. Everything runs on your local machine.
* **Multiple Voices & Models:** Choose between 8 distinct voices and scale the TTS model size (`nano`, `micro`, `mini`) based on your hardware capabilities.
* **Diagnostic Tools:** Includes a built-in text-dump feature to output the parsed text before synthesis, making it easy to debug document extraction.

## 🚀 Installation

Ensure you have **Python 3.9+** installed. It is highly recommended to install KittenCast inside a virtual environment.

**1. Clone the repository:**

```bash
git clone [https://github.com/yourusername/kittencast.git](https://github.com/yourusername/kittencast.git)
cd kittencast
```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install the project (Editable Mode):**

```bash
pip install -e .
```

*(This will automatically fetch all required dependencies, including NLTK, EbookLib, PyPDF, and the KittenTTS engine).*

## 📖 Usage

Once installed, the `kittencast` command is available globally in your terminal.

### Basic Command

Point the tool at any supported document format to generate an audiobook in the default `Audiobook_Output` folder:

```bash
kittencast my_book.epub
```

### Advanced Examples

**Generate a PDF audiobook using a specific voice and output folder:**

```bash
kittencast research_paper.pdf -o "Research_Audio" -v Luna
```

**Use the higher-quality `mini` model and dump the text for debugging:**

```bash
kittencast notes.docx -m KittenML/kitten-tts-mini-0.8 -d
```

### CLI Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `input_file` | | **(Required)** Path to the `.epub`, `.pdf`, `.docx`, or `.txt` file. | |
| `--out-dir` | `-o` | The folder where the `.wav` chapter files will be saved. | `Audiobook_Output` |
| `--voice` | `-v` | TTS Voice: `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo` | `Jasper` |
| `--model` | `-m` | KittenTTS Model: `nano-0.8`, `micro-0.8`, `mini-0.8` | `nano-0.8` |
| `--dump-text`| `-d` | Saves the extracted text to `extracted_text_dump.txt` before generating audio. | `False` |

## 🛠️ Text Processing Scheme

Documents are parsed into distinct "Sections," each of which correspond to a generated `.wav` file:
* **`.epub`**: Parsed by chapter (ignoring artifact pages < 150 chars).
* **`.pdf`**: Parsed page-by-page.
* **`.docx` / `.txt`**: Parsed as a single continuous document.

## 🧪 Running Tests

To run the test suite locally and verify the text-chunking logic:

```bash
pip install pytest
pytest tests/
```