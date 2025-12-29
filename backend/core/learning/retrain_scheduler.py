from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AdaptiveLearner:
    def __init__(self):
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.cluster_model = KMeans(n_clusters=10)
        self.new_terms = []
        self.manual_labels = []  # Analyst input

    def analyze_text(self, text: str, lang: str):
        sentences = [s.strip() for s in text.split('.') if s]
        embeddings = self.embedder.encode(sentences)

        if len(embeddings) > 10:
            self.cluster_model.fit(embeddings)
            for idx, label in enumerate(self.cluster_model.labels_):
                if self._is_novel(embeddings[idx]):
                    self.new_terms.append({
                        'text': sentences[idx],
                        'lang': lang,
                        'embedding': embeddings[idx].tolist(),
                        'distance': float(np.min(cosine_distances([embeddings[idx]], self.cluster_model.cluster_centers_)))
                    })

    def _is_novel(self, embedding: np.ndarray) -> bool:
        distances = cosine_distances([embedding], self.cluster_model.cluster_centers_)
        min_distance = np.min(distances)
        return min_distance > 0.4  # Tunable threshold

    def get_new_terms(self):
        return self.new_terms

    def label_term(self, text: str, label: str):
        for term in self.new_terms:
            if term['text'] == text:
                term['label'] = label
                self.manual_labels.append(term)
                break

    def retrain(self):
        if not self.manual_labels:
            logger.info("No labeled terms available for retraining.")
            return None
        labeled_embeddings = [np.array(term['embedding']) for term in self.manual_labels]
        labeled_labels = [term['label'] for term in self.manual_labels]
        self.cluster_model.fit(labeled_embeddings)
        logger.info("Retraining complete using manually labeled data.")


class RetrainScheduler:
    def __init__(self, learner: AdaptiveLearner):
        self.learner = learner

    async def start(self):
        while True:
            now = datetime.now()
            if now.hour == 4 and now.minute == 0:
                await self.daily_retrain()
            elif len(self.learner.manual_labels) >= 50:
                await self.emergency_retrain()
            await asyncio.sleep(60)

    async def daily_retrain(self):
        if len(self.learner.manual_labels) > 0:
            self.learner.retrain()
            logger.info(f"[{datetime.now()}] Performed daily retraining")

    async def emergency_retrain(self):
        self.learner.retrain()
        logger.info(f"[{datetime.now()}] Emergency retrain for 50+ new terms")

    async def trigger_retrain_now(self):
        self.learner.retrain()
        logger.info("Retrain manually triggered by analyst.")
