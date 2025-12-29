from bertopic import BERTopic
from transformers import pipeline
import spacy
import nltk
# Asegura que el recurso 'punkt' esté disponible
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to extract main topic
def extract_main_topic(transcription_text: str) -> str:
    sentences = sent_tokenize(transcription_text)
    if len(sentences) < 2:
        return "Tema no identificado"
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(sentences)
    main_topic = topic_model.get_topic(topics[0])
    if main_topic:
        return ", ".join([word for word, _ in main_topic])
    return "Tema no identificado"

# Function to summarize text
def summarize_text(transcription_text: str) -> str:
    chunks = [transcription_text[i:i+1000] for i in range(0, len(transcription_text), 1000)]
    summaries = [summarizer(chunk, max_length=100, min_length=25, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)
