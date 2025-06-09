# 🔊 Chatify — YouTube Video Chaptering and Summarization Tool

**Chatify** is an AI-powered Flask web application that takes a YouTube video URL and automatically generates meaningful **chapter-wise summaries** and **titles** from spoken Hindi or Hinglish content. It uses **OpenAI's Whisper**, **mBART**, and **KeyBERT** to convert speech to text, summarize it, and generate chapter titles. The output is a clean, timestamped JSON file—ideal for content indexing, accessibility, or quick navigation.

---
## 🧰 Tech Stack

### 🖥️ Backend
- **Flask** — Lightweight Python web framework for handling routes and requests.

### 🧠 Machine Learning & NLP
- **Whisper (by OpenAI)** — For speech-to-text transcription from Hindi/Hinglish audio.
- **mBART (by Facebook AI)** — For abstractive summarization and Hindi → English translation.
- **KeyBERT** — For keyword-based title generation using BERT embeddings.

### 🎥 Audio & Video Processing
- **yt-dlp** — For downloading audio from YouTube videos.
- **ffmpeg** — For converting and processing audio formats (MP4 → MP3/WAV).

### 📁 File Handling & Utilities
- **uuid** — For generating unique job identifiers.
- **pathlib / os / json** — For safe file and directory operations.

### 🌐 Frontend
- **HTML + Jinja2** — For rendering dynamic content using Flask templates.
- **Bootstrap (optional)** — For basic responsive styling (if used in your `index.html`).

### 📝 Output
- **JSON** — Chapters with timestamps, titles, and summaries.


## 🚀 Features

- 🎥 Accepts a YouTube video URL as input  
- 🧠 Converts spoken Hindi/Hinglish content into English summaries  
- 🕐 Breaks videos into timestamped chapters (default: every 5 minutes)  
- 📝 Generates meaningful chapter titles using keyword extraction  
- 📁 Outputs a structured `.json` file containing start time, title, and summary  
- 🌐 Simple Flask UI to interact with the tool via browser  

---
## 🔧 Pipeline Explanation

### 1. 🎥 Input: YouTube Video Link
- The user provides a YouTube video URL.
- The audio stream is extracted and saved as an MP3 using `yt-dlp` and `ffmpeg`.

### 2. 🗣️ ASR (Automatic Speech Recognition) with Whisper
- Audio is transcribed using OpenAI's **Whisper** model.
- **Output**: Timestamped transcript in Hindi/Hinglish.
- **Format**: `[start_time - end_time]: text`

### 3. 🧹 Preprocessing
- The transcript is cleaned and formatted.
- Each segment includes a timestamp and its corresponding spoken content.

### 4. 🧩 Chunking into Segments
- The transcript is split into fixed-length chunks (e.g., 300 seconds = 5 minutes).
- Timestamp alignment is preserved.
- Each chunk is treated as a potential chapter.

### 5. 🧠 Summarization using mBART
- Each chunk is summarized using **mBART**, a multilingual transformer fine-tuned for Hindi-to-English summarization.
- **Output**: Concise English summary of the chunk’s content.

### 6. 🏷️ Chapter Title Generation with KeyBERT
- Using **KeyBERT**, important keywords are extracted from each summary.
- The most relevant keyword or phrase is selected as the chapter title.

### 7. 📦 Chapter Assembly
- For each chunk, the following are saved:
  - `start_time`
  - `summary`
  - `title`
- Final output is stored as a structured `.json` file.

### ✅ Example Output
```json
[
  {
    "start_time": "0:00:00",
    "title": "Social Professions",
    "summary": "The speaker discusses how certain professions like tea vendors, garbage collectors, and dancers are perceived with bias in Indian society..."
  },
  ...
]

## 📂 Project Structure

chatify/
│
├── app.py # Flask app
├── workspace/ # Temporary folder to store job-specific files
├── templates/
│ └── index.html # Web interface
│
└── pipeline/
├── downloader.py # Uses yt-dlp to extract audio from YouTube
├── transcriber.py # Whisper transcription + transcript saver
├── chapterizer.py # Chunking + summarization + title generation
└── utils.py # time conversion
├── static/
│ └── style.css # Web design
├── trail/     # demo files(project working)
│ └── try.ipynb 
  └── chapters.ipynb

