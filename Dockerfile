FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1-mesa-glx \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "process_pdfs.py"]
