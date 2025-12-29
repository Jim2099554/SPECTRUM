from threading import Lock
from collections import deque
import numpy as np
from scipy.spatial.distance import cosine
import whisper
import torch
import torchaudio
import time
from pathlib import Path
import os
from typing import Dict, Any, List, Optional
from utils.crypto import encrypt_file, decrypt_file, secure_tempfile

class AudioTranscriber:
    def __init__(self, model_name: str = "base"):
        """
        Initialize the transcriber with the specified Whisper model.
        Args:
            model_name: The name of the Whisper model to use (tiny, base, small, medium, large)
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_name).to(self.device)
    
    def transcribe(self, audio_path: Path) -> Dict[str, Any]:
        """
        Transcribe an audio file to text.
        Args:
            audio_path: Path to the audio file
        Returns:
            Dictionary containing transcription results and metadata
        """
        try:
            decrypted_path_tuple = secure_tempfile()
            decrypted_path = decrypted_path_tuple[0] if isinstance(decrypted_path_tuple, tuple) else decrypted_path_tuple
            decrypt_file(str(audio_path), decrypted_path)
            result = self.model.transcribe(decrypted_path)
            os.remove(decrypted_path)
            return {
                "text": result.get("text", ""),
                "segments": result.get("segments", []),
                "language": result.get("language", ""),
                "status": "success"
            }
        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_word_timestamps(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract word-level timestamps from the transcription result.
        Args:
            result: The transcription result dictionary
        Returns:
            List of words with their timestamps
        """
        words = []
        for segment in result.get("segments", []):
            for word in segment.get("words", []):
                words.append({
                    "text": word.get("text"),
                    "start": word.get("start"),
                    "end": word.get("end"),
                    "confidence": word.get("confidence")
                })
        return words

class RealTimeTranscriber:
    def __init__(self, transcriber: Optional[AudioTranscriber] = None):
        """
        Real-time transcriber for streaming audio and voiceprint matching.
        Args:
            transcriber: Optional AudioTranscriber instance for transcription.
        """
        self.buffer = deque(maxlen=10)  # 10-second buffer
        self.lock = Lock()
        self.voiceprints = {}  # Known voiceprints {id: embedding}
        self.transcriber = transcriber or AudioTranscriber()

    def process_chunk(self, audio_chunk: np.ndarray, sample_rate: int) -> Optional[Dict[str, Any]]:
        """
        Process 2-second audio chunks in real-time.
        Args:
            audio_chunk: Audio data as numpy array.
            sample_rate: Sample rate of the audio.
        Returns:
            Transcription and speaker info if buffer is full, else None.
        """
        with self.lock:
            waveform = torch.from_numpy(audio_chunk).float()
            if sample_rate != 16000:
                waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
            self.buffer.append(waveform)
            if sum(len(w) for w in self.buffer) >= 5 * 16000:
                full_waveform = torch.cat(list(self.buffer))
                results = self._process_full(full_waveform)
                self.buffer.clear()
                return results
        return None

    def _process_full(self, waveform: torch.Tensor) -> Dict[str, Any]:
        """
        Process buffered audio with voice matching.
        """
        # Save waveform to temp file for transcription
        import tempfile
        import torchaudio
        import os
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            torchaudio.save(tmp_wav.name, waveform.unsqueeze(0), 16000)
            temp_path = tmp_wav.name
        transcription_result = self.transcriber.transcribe(Path(temp_path))
        os.remove(temp_path)
        embedding = self.get_voiceprint(waveform)
        speaker_id = self.match_voiceprint(embedding)
        return {
            "text": transcription_result.get("text", ""),
            "speaker": speaker_id,
            "timestamp": time.time(),
            "embedding": embedding
        }

    def get_voiceprint(self, waveform: torch.Tensor) -> List[float]:
        """
        Dummy voiceprint extraction. Replace with actual embedding extraction.
        """
        # Placeholder: mean of waveform as embedding
        return waveform.mean(dim=-1).tolist()

    def match_voiceprint(self, embedding: List[float]) -> str:
        """
        Find closest voiceprint match using cosine similarity.
        """
        if not self.voiceprints or np.linalg.norm(embedding) == 0:
            return "unknown"
        similarities = {
            uid: 1 - cosine(embedding, known_emb)
            for uid, known_emb in self.voiceprints.items()
            if np.linalg.norm(known_emb) != 0
        }
        if not similarities:
            return "unknown"
        best_match = max(similarities, key=similarities.get)
        return best_match if similarities[best_match] > 0.85 else "unknown"

       