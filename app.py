from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langdetect import detect
from googletrans import Translator as GoogleTranslator
from transformers import pipeline
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to process YouTube URL
def process_youtube_url(youtube_url):
    # Add your processing logic here
    if "youtube.com" in youtube_url:
        # Return example image URL and string
        image_url = thumbnail(youtube_url)  # Example image URL
        summary=get_youtube_summary(youtube_url)
        return image_url, summary
    else:
        return None, "Invalid YouTube URL"
    
def thumbnail(youtube_url):
    try:
        yt = YouTube(youtube_url)
        thumbnail_url = yt.thumbnail_url
        return thumbnail_url
    except Exception as e:
        print("Error:", e)
        return None

def get_youtube_summary(VIDEO_URL):
    if '=' in VIDEO_URL:
        video_id = VIDEO_URL.split('=')[1]
    else:
        print("Invalid URL")
        return None

    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=languages = [
    'en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
    'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'eo', 'et', 'tl', 'fi',
    'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'he', 'iw', 'hi',
    'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw',
    'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt',
    'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro',
    'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su',
    'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz',
    'vi', 'cy', 'xh', 'yi', 'yo', 'zu'
]
)
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    str0 = ''
    for i in srt:
        str0 += i['text'] + " "

    l = str0.split(" ")
    strl = ""
    for i in l:
        if len(i) == 0:
            l.remove(i)
        elif (i[0] == '[' and i[-1] == ']'):
            l.remove(i)
        else:
            strl += i + " "

    language = detect(strl)

    def translate_text(text, to_lang, from_lang=None, chunk_size=500):
        translator = GoogleTranslator()
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = [translator.translate(chunk, src=from_lang, dest=to_lang).text for chunk in chunks]
        translated_text = ''.join(translated_chunks)
        return translated_text

    normal = 'en'
    if language == 'en':
        translated_text = translate_text(strl, to_lang="en", from_lang=normal)
    else:
        translated_text = translate_text(strl, to_lang="en", from_lang=language)

    # Split the translated text into chunks of 1024 tokens
    chunks = [translated_text[i:i + 1024] for i in range(0, len(translated_text), 1024)]

    summarizer = pipeline("summarization")

    # Summarize each chunk and concatenate the results
    summary = ""
    for chunk in chunks:
        summary += summarizer(chunk, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)[0]['summary_text']

    return summary

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    result_text = None
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        image_url, result_text = process_youtube_url(youtube_url)

    return render_template("index.html", image_url=image_url, result_text=result_text)

if __name__ == "__main__":
    app.run(debug=True)
