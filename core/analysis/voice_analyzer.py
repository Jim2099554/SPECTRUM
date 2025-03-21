import librosa
import numpy as np
import tensorflow as tf

class VoiceAnalyzer:
    def __init__(self):
        self.model = tf.keras.models.load_model('models/voice_stress_detector.h5')
        
    def analyze(self, audio_path: str) -> dict:
        # Extract features
        y, sr = librosa.load(audio_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        
        # Predict stress level
        prediction = self.model.predict(np.expand_dims(mfcc, axis=0))
        
        return {
            'stress_level': float(prediction[0][0]),
            'pitch_variance': float(np.var(librosa.yin(y, fmin=50, fmax=2000))),
            'speech_rate': len(librosa.effects.split(y, top_db=20)) / (len(y) / sr)
        }
