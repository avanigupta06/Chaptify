import whisper
from pathlib import Path
from datetime import timedelta

model = whisper.load_model("medium")

def transcribe_audio(mp3_path: Path):
    print(f"[INFO] Transcribing: {mp3_path.name}")
    result = model.transcribe(str(mp3_path), verbose=True)
    return result["segments"]

def save_transcript(segments, output_file: Path):
    with open(output_file, "w", encoding="utf-8") as f:
        for seg in segments:
            start = str(timedelta(seconds=int(seg['start'])))
            end = str(timedelta(seconds=int(seg['end'])))
            f.write(f"[{start} - {end}]: {seg['text'].strip()}\n")
    print(f"[INFO] Transcript saved to {output_file}")
