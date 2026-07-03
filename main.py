#!/usr/bin/env python3
"""
FastAPI application for YouTube Transcript API
"""

from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi as YTTranscriptApi

app = FastAPI(
    title="YouTube Transcript API",
    description="API para obter transcrições de vídeos do YouTube",
    version="1.0.0"
)


@app.get("/")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "message": "YouTube Transcript API is running",
        "version": "1.0.0"
    }


@app.get("/transcript/{video_id}")
def get_transcript(
    video_id: str,
    language: str = Query(None, description="Language code (e.g., 'en', 'pt', 'es')")
):
    """
    Fetch transcript for a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        language (str, optional): Language code for the transcript
    
    Returns:
        dict: Transcript data with metadata
    """
    try:
        yt_api = YTTranscriptApi()
        
        if language:
            # Fetch transcript in specific language
            transcript = yt_api.get_transcript(
                video_id,
                languages=[language]
            )
        else:
            # Fetch transcript in default language
            transcript = yt_api.get_transcript(video_id)
        
        # Combine text entries
        full_text = " ".join([entry["text"] for entry in transcript])
        
        return {
            "status": "success",
            "video_id": video_id,
            "language": language or "default",
            "entries_count": len(transcript),
            "transcript": transcript,
            "full_text": full_text
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching transcript: {str(e)}"
        )


@app.get("/languages/{video_id}")
def get_available_languages(video_id: str):
    """
    List available transcript languages for a video
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        dict: Available languages organized by type (manual/auto-generated)
    """
    try:
        yt_api = YTTranscriptApi()
        transcript_list = yt_api.list_transcripts(video_id)
        
        manually_created = [
            {
                "language": t.language,
                "language_code": t.language_code,
                "is_generated": t.is_generated
            }
            for t in transcript_list.manually_created_transcripts
        ]
        
        auto_generated = [
            {
                "language": t.language,
                "language_code": t.language_code,
                "is_generated": t.is_generated
            }
            for t in transcript_list.automatically_generated_transcripts
        ]
        
        return {
            "status": "success",
            "video_id": video_id,
            "manually_created_transcripts": manually_created,
            "auto_generated_transcripts": auto_generated,
            "total_languages": len(manually_created) + len(auto_generated)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error listing transcripts: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
