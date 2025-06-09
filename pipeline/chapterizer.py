import re
import json
from pathlib import Path
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from keybert import KeyBERT
from .utils import parse_timestamp, seconds_to_timestamp, format_timestamp_properly

model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
kw_model = KeyBERT()

CHUNK_SIZE = 300  # seconds

def summarize_and_translate(text):
    tokenizer.src_lang = "hi_IN"
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=128, num_beams=4, early_stopping=True)
    summary_hi = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)[0]

    translated = model.generate(tokenizer(summary_hi, return_tensors="pt").input_ids, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

def get_title(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=1)
    return keywords[0][0] if keywords else "Untitled"

def chapterize(transcript_path: Path, output_json: Path):
    with open(transcript_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    chunks, current_chunk, current_duration, chunk_start = [], [], 0, None

    for line in lines:
        match = re.match(r"\[(\d+:\d+:\d+) - (\d+:\d+:\d+)\]: (.+)", line)
        if not match:
            continue

        start, end, content = match.groups()
        start_sec = parse_timestamp(start)
        end_sec = parse_timestamp(end)
        duration = end_sec - start_sec

        if chunk_start is None:
            chunk_start = start_sec

        if current_duration + duration > CHUNK_SIZE:
            chunks.append((chunk_start, current_chunk))
            current_chunk = [(start_sec, content)]
            current_duration = duration
            chunk_start = start_sec
        else:
            current_chunk.append((start_sec, content))
            current_duration += duration

    if current_chunk:
        chunks.append((chunk_start, current_chunk))

    results = []
    for chunk_start, segment in chunks:
        full_text = " ".join([text for _, text in segment])
        translated_summary = summarize_and_translate(full_text)
        title = get_title(translated_summary)
        results.append({
            "start_time": format_timestamp_properly(seconds_to_timestamp(chunk_start)),
            "title": title,
            "summary": translated_summary
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"[INFO] Chapters saved to {output_json}")
