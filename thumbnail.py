from pytube import YouTube

def get_youtube_thumbnail(url):
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        return thumbnail_url
    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example YouTube video URL
thumbnail_url = get_youtube_thumbnail(video_url)
print("Thumbnail URL:", thumbnail_url)
