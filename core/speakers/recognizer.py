from speechbrain.pretrained import EncoderClassifier
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional

class SpeakerRecognizer:
    def __init__(self):
        """
        Initialize the speaker recognition system using SpeechBrain
        """
        self.encoder = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.known_speakers = {}
        
    def extract_embeddings(self, audio_path: Path) -> np.ndarray:
        """
        Extract speaker embeddings from an audio file
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Speaker embedding vector
        """
        signal = self.encoder.load_audio(str(audio_path))
        embeddings = self.encoder.encode_batch(signal)
        return embeddings.squeeze().cpu().numpy()
    
    def register_speaker(self, name: str, embedding: np.ndarray):
        """
        Register a new speaker in the database
        
        Args:
            name: Name or identifier for the speaker
            embedding: Speaker's voice embedding
        """
        self.known_speakers[name] = embedding
    
    def identify_speaker(self, embedding: np.ndarray, threshold: float = 0.75) -> Optional[str]:
        """
        Identify a speaker from their voice embedding
        
        Args:
            embedding: Voice embedding to identify
            threshold: Similarity threshold for identification
            
        Returns:
            Speaker name if identified, None if unknown
        """
        if not self.known_speakers:
            return None
            
        max_similarity = -1
        identified_speaker = None
        
        for name, known_embedding in self.known_speakers.items():
            similarity = self._compute_similarity(embedding, known_embedding)
            if similarity > max_similarity:
                max_similarity = similarity
                identified_speaker = name
        
        return identified_speaker if max_similarity > threshold else None
    
    def _compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        """
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
