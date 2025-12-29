import logging
logger = logging.getLogger(__name__)
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

class AdaptiveLearner:
    def __init__(self, n_clusters=10):
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.cluster_model = KMeans(n_clusters=n_clusters)
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
        # Update risk patterns with new terms, using analyst-labeled examples
        if not self.manual_labels:
            return None
        labeled_embeddings = [np.array(term['embedding']) for term in self.manual_labels]
        labeled_labels = [term['label'] for term in self.manual_labels]
        self.cluster_model.fit(labeled_embeddings)
        logger.info("Retraining complete using manually labeled data.")
