import whisper
import torch
from pathlib import Path
from typing import Dict, Any

class AudioTranscriber:
    def __init__(self, model_name: str = "base"):
        """
        Initialize the transcriber with the specified Whisper model
        
        Args:
            model_name: The name of the Whisper model to use (tiny, base, small, medium, large)
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_name).to(self.device)
    
    async def transcribe(self, audio_path: Path) -> Dict[str, Any]:
        """
        Transcribe an audio file to text
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results and metadata
        """
        try:
            result = self.model.transcribe(str(audio_path))
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"],
                "status": "success"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_word_timestamps(self, result: Dict[str, Any]) -> list:
        """
        Extract word-level timestamps from the transcription result
        
        Args:
            result: The transcription result dictionary
            
        Returns:
            List of words with their timestamps
        """
        words = []
        for segment in result["segments"]:
            for word in segment.get("words", []):
                words.append({
                    "text": word["text"],
                    "start": word["start"],
                    "end": word["end"],
                    "confidence": word["confidence"]
                })
        return words
