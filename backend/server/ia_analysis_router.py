from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.core.analysis.content_analyzer import ContentAnalyzer
import spacy

router = APIRouter()

from langdetect import detect
from transformers import pipeline

# Inicializar ContentAnalyzer
content_analyzer = ContentAnalyzer()

# Modelos spaCy por idioma
SPACY_MODELS = {
    'es': 'es_core_news_sm',
    'en': 'en_core_web_sm',
    'fr': 'fr_core_news_sm',
    'de': 'de_core_news_sm',
    'it': 'it_core_news_sm',
    'ru': 'ru_core_news_sm',
    'zh': 'zh_core_web_sm',
}

# Modelos HuggingFace para sentimiento por idioma
SENTIMENT_MODELS = {
    'es': 'pysentimiento/robertuito-sentiment-analysis',
    'en': 'distilbert-base-uncased-finetuned-sst-2-english',
    'fr': 'tblard/tf-allocine',
    'de': 'oliverguhr/german-sentiment-bert',
    'it': 'MilaNLProc/feel-it-italian-sentiment',
    'ru': 'blanchefort/rubert-base-cased-sentiment',
    'zh': 'uer/roberta-base-finetuned-jd-binary-chinese',
}

# Cache de modelos spaCy y pipelines
_spacy_cache = {}
_sentiment_cache = {}

# Precarga todos los modelos soportados al iniciar
for lang, model_name in SPACY_MODELS.items():
    try:
        _spacy_cache[lang] = spacy.load(model_name)
    except Exception:
        import spacy.cli
        spacy.cli.download(model_name)
        _spacy_cache[lang] = spacy.load(model_name)

for lang, model_name in SENTIMENT_MODELS.items():
    try:
        _sentiment_cache[lang] = pipeline('sentiment-analysis', model=model_name)
    except Exception as e:
        print(f"[WARN] No se pudo cargar modelo de sentimiento para {lang}: {e}")

def get_spacy(lang):
    return _spacy_cache.get(lang)

def get_sentiment_pipeline(lang):
    return _sentiment_cache.get(lang)

# MODELOS DE ENTRADA Y SALIDA
class TranscripcionIn(BaseModel):
    id: int
    texto: str

class TranscripcionIA(BaseModel):
    id: int
    palabras_clave: List[str]
    resumen_automatico: str
    emocion: str

@router.post("/analyze/transcription")
def analyze_transcription(payload: Dict[str, List[TranscripcionIn]]):
    transcripciones = payload.get("transcripciones", [])
    resultados = []
    for tx in transcripciones:
        texto = tx.texto
        try:
            lang = detect(texto)
        except Exception:
            lang = 'es'  # fallback
        if lang not in SPACY_MODELS:
            resultado = TranscripcionIA(
                id=tx.id,
                palabras_clave=[],
                resumen_automatico="Modelo no soportado para este idioma",
                emocion="No disponible"
            )
            resultados.append(resultado.dict())
            continue
        nlp = get_spacy(lang)
        doc = nlp(texto)
        palabras_clave = [ent.text for ent in doc.ents]
        resumen_automatico = content_analyzer._generate_summary(doc)
        # Sentimiento
        sentiment_pipeline = get_sentiment_pipeline(lang)
        if sentiment_pipeline:
            try:
                sentiment = sentiment_pipeline(texto)[0]
                emocion = sentiment.get("label", "Neutral")
            except Exception:
                emocion = "Desconocido"
        else:
            emocion = "No disponible"
        resultado = TranscripcionIA(
            id=tx.id,
            palabras_clave=palabras_clave or [],
            resumen_automatico=resumen_automatico,
            emocion=emocion
        )
        resultados.append(resultado.dict())
    return {"resultados": resultados}
