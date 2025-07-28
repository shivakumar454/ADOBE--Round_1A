import os
import fitz  
import json
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re

INPUT_DIR = "input"
OUTPUT_DIR = "output"

regex_patterns = {
    "H1": [r"^(Chapter|CHAPTER|[1-9][0-9]*\.)", r"^第[一二三四五六七八九十0-9]+章"],
    "H2": [r"^\d+\.\d+\s+.+", r"^第[一二三四五六七八九十0-9]+節"],
    "H3": [r"^\d+\.\d+\.\d+\s+.+", r"^第[一二三四五六七八九十0-9]+項"]
}


def detect_heading_level(text, font_size=None, font_ranks={}):
    text = text.strip()
    for level, patterns in regex_patterns.items():
        for pat in patterns:
            if re.match(pat, text):
                return level
    if font_size and font_size in font_ranks:
        return font_ranks[font_size]
    return None


def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = os.path.splitext(os.path.basename(pdf_path))[0]
    outline = []

    font_sizes = set()
    all_spans = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue
                    font_size = span["size"]
                    font_sizes.add(font_size)
                    all_spans.append({
                        "text": text,
                        "size": font_size,
                        "page": page_num
                    })

    sorted_fonts = sorted(list(font_sizes), reverse=True)
    font_ranks = {}
    if len(sorted_fonts) >= 3:
        font_ranks = {
            sorted_fonts[0]: "H1",
            sorted_fonts[1]: "H2",
            sorted_fonts[2]: "H3"
        }

    for span in all_spans:
        level = detect_heading_level(span["text"], span["size"], font_ranks)
        if level:
            outline.append({
                "level": level,
                "text": span["text"],
                "page": span["page"]
            })

    if not outline:
        for page_num in range(len(doc)):
            images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
            if images:
                ocr_text = pytesseract.image_to_string(images[0], lang="eng+jpn")
                for line in ocr_text.splitlines():
                    level = detect_heading_level(line)
                    if level:
                        outline.append({
                            "level": level,
                            "text": line.strip(),
                            "page": page_num + 1
                        })

    return {"title": title, "outline": outline}


def process_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            result = extract_headings_from_pdf(pdf_path)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_all_pdfs()
