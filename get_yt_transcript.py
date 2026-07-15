from youtube_transcript_api import YouTubeTranscriptApi

try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch("8ULmmnz8gXA", languages=['th', 'en'])
    text = " ".join([t['text'] for t in transcript])
    print(text)
except Exception as e:
    print(f"Error: {e}")
