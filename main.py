#!/usr/bin/env python3
"""
Example usage of the YouTube Transcript API
"""

from youtube_transcript_api import YouTubeTranscriptApi


def main():
    """
    Main function to demonstrate YouTube Transcript API usage
    """
    
    # Example: YouTube video ID
    # You can extract this from a URL like: https://www.youtube.com/watch?v=VIDEO_ID
    video_id = "dQw4w9WgXcQ"  # Replace with your video ID
    
    try:
        # Fetch transcript in default language
        print(f"Fetching transcript for video: {video_id}\n")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Display transcript
        print("=" * 60)
        print("TRANSCRIPT")
        print("=" * 60)
        for entry in transcript:
            print(f"[{entry['start']:.2f}s] {entry['text']}")
        
        # Optional: Save transcript to a file
        with open("transcript.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(f"{entry['text']} ")
        print("\n✓ Transcript saved to 'transcript.txt'")
        
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        print("Please check the video ID and try again.")


def get_available_languages(video_id):
    """
    Fetch available transcript languages for a video
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        print(f"Available languages for video {video_id}:")
        print("\nManually created transcripts:")
        for transcript in transcript_list.manually_created_transcripts:
            print(f"  - {transcript.language} ({transcript.language_code})")
        
        print("\nAuto-generated transcripts:")
        for transcript in transcript_list.automatically_generated_transcripts:
            print(f"  - {transcript.language} ({transcript.language_code})")
            
    except Exception as e:
        print(f"Error listing transcripts: {e}")


def get_transcript_by_language(video_id, language_code):
    """
    Fetch transcript in a specific language
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=[language_code]
        )
        
        print(f"Transcript in {language_code}:")
        for entry in transcript:
            print(f"[{entry['start']:.2f}s] {entry['text']}")
            
    except Exception as e:
        print(f"Error fetching transcript: {e}")


if __name__ == "__main__":
    main()
    
    # Uncomment to see available languages:
    # get_available_languages("dQw4w9WgXcQ")
    
    # Uncomment to get transcript in a specific language:
    # get_transcript_by_language("dQw4w9WgXcQ", "pt")  # Portuguese
