# Adobe Round 1A – PDF Parser & JSON Generator

This project parses input PDF documents and generates structured JSON output using PyMuPDF. It is containerized using Docker for consistency and portability.

---

##  Folder Structure
adobe-round1a/
├── input/ # Folder to place all input PDF files

├── output/ # Generated JSON files will appear here

├── parser.py # Main Python script for PDF parsing

├── requirements.txt # Python dependency file

├── Dockerfile # For Docker container setup

└── README.md # This file

 

****

#  How to run

# Step 1: Install Docker

Make sure Docker is installed and running on your system.  
🔗 https://docs.docker.com/get-docker/

---

#  Step 2: Add PDF Files

- Place all PDF files into the `input/` folder.

---

#  Step 3: Create `requirements.txt`

Create a `requirements.txt` file with the following line:

---

# Step 4: Build Docker Image

```bash
docker build -t adobe_pdf_parser:mypdftest123 .

---

 --- For Linux/macOS:
     docker run --platform linux/amd64 -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe_pdf_parser:mypdftest123

 ---For Windows PowerShell: 
docker run --platform linux/amd64 -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" adobe_pdf_parser:mypdftest123


Output
Parsed JSON files will be available in the output/ folder.

Each JSON corresponds to an input PDF.



Tech Stack::

    Python

    PyMuPDF (fitz)

    Docker



 **** NOTES
     If you face issues with PyMuPDF==1.22.3, install the latest with just pip install PyMuPDF and update requirements.txt accordingly.

     Make sure input/ and output/ folders exist before running.