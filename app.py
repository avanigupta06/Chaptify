from flask import Flask, request, render_template, jsonify
from pathlib import Path
import uuid
import os
import json

from pipeline.downloader import download_audio
from pipeline.transcriber import transcribe_audio, save_transcript
from pipeline.chapterizer import chapterize

app = Flask(__name__)

BASE_DIR = Path("workspace")
BASE_DIR.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    chapters = None
    error = None

    if request.method == "POST":
        youtube_url = request.form.get("url")
        if not youtube_url:
            error = "Please provide a YouTube URL."
        else:
            try:
                job_id = uuid.uuid4().hex
                job_dir = BASE_DIR / job_id
                job_dir.mkdir()

                audio_path = download_audio(youtube_url, job_dir)
                segments = transcribe_audio(audio_path)
                transcript_path = job_dir / "transcript.txt"
                save_transcript(segments, transcript_path)

                output_json = job_dir / "chapters.json"
                chapterize(transcript_path, output_json)

                with open(output_json, "r", encoding="utf-8") as f:
                    chapters = json.load(f)

            except Exception as e:
                error = str(e)

    return render_template("index.html", chapters=chapters, error=error)

if __name__ == "__main__":
    app.run(debug=True)
