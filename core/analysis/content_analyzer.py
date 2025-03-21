from transformers import pipeline
from typing import Dict, Any, List
import re

class ContentAnalyzer:
    def __init__(self):
        """Initialize the content analysis system"""
        # Pre-defined risk patterns
        self.risk_patterns = {
            'drugs': [
                r'(?i)cocaine|heroin|meth|drug|pills?|weed|marijuana',
                r'(?i)dealer|supply|stash|batch|pure|quality',
                r'(?i)grams?|kilos?|ounces?|pounds?',
                r'(?i)delivery|pickup|drop.?off|meet.?up'
            ],
            'money': [
                r'(?i)\$\d+[k]?',
                r'(?i)cash|money|payment|transfer',
                r'(?i)bitcoin|crypto|wallet'
            ],
            'suspicious': [
                r'(?i)cops?|police|feds?',
                r'(?i)careful|quiet|private|secret',
                r'(?i)burner|phone|secure|encrypted'
            ]
        }
        
        # Initialize sentiment analysis
        self.sentiment = pipeline('sentiment-analysis', model='distilbert-base-uncased')
    
    def analyze_conversation(self, text: str) -> Dict[str, Any]:
        """Analyze conversation content for risks"""
        results = {
            'risk_level': 0,  # 0-100
            'risk_factors': [],
            'matches': {},
            'sentiment': None
        }
        
        # Check for risk patterns
        for category, patterns in self.risk_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.finditer(pattern, text)
                for match in found:
                    matches.append({
                        'text': match.group(),
                        'start': match.start(),
                        'end': match.end()
                    })
            if matches:
                results['matches'][category] = matches
                results['risk_factors'].append(category)
        
        # Calculate risk level
        risk_score = 0
        if 'drugs' in results['risk_factors']:
            risk_score += 40
        if 'money' in results['risk_factors']:
            risk_score += 30
        if 'suspicious' in results['risk_factors']:
            risk_score += 30
            
        # Adjust risk based on co-occurrence
        if len(results['risk_factors']) > 1:
            risk_score = min(100, risk_score * 1.5)
            
        results['risk_level'] = int(risk_score)
        
        # Add sentiment analysis
        try:
            sentiment = self.sentiment(text)[0]
            results['sentiment'] = {
                'label': sentiment['label'],
                'score': sentiment['score']
            }
        except Exception as e:
            results['sentiment'] = {'error': str(e)}
            
        return results
    
    def _generate_summary(self, doc) -> str:
        """
        Generate a brief summary of the text
        
        Args:
            doc: spaCy document
            
        Returns:
            Summary string
        """
        # Simple extractive summarization
        sentences = list(doc.sents)
        if not sentences:
            return ""
            
        # Return first sentence as summary if text is short
        if len(sentences) <= 2:
            return sentences[0].text
            
        # Otherwise return first and last sentences
        return f"{sentences[0].text} [...] {sentences[-1].text}"
