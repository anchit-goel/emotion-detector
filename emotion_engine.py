import json
import re

class EmotionEngine:
    def __init__(self, afinn_path='afinn.json'):
        self.afinn = {}
        try:
            with open(afinn_path, 'r') as f:
                self.afinn = json.load(f)
        except Exception as e:
            print(f"Error loading AFINN data: {e}")
            # Fallback mock data if file missing
            self.afinn = {"happy": 3, "sad": -2, "angry": -3, "excited": 3, "furious": -4}

        self.emotion_keywords = {
            "angry": ["furious", "angry", "mad", "rage", "hate", "annoyed", "irritated"],
            "fearful": ["scared", "afraid", "terrified", "fear", "panic", "anxious", "nervous"],
            "sad": ["sad", "lonely", "depressed", "unhappy", "heartbroken", "grief", "cry"]
        }

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def analyze(self, text):
        if not text or not text.strip():
            return None

        tokens = self.tokenize(text)
        score = 0
        words_matched = 0

        # 1. Calculate Sentiment Score
        for token in tokens:
            if token in self.afinn:
                score += self.afinn[token]
                words_matched += 1

        # 2. Detect specific keywords
        keyword_counts = {k: 0 for k in self.emotion_keywords}
        for token in tokens:
            for emotion, keywords in self.emotion_keywords.items():
                if token in keywords:
                    keyword_counts[emotion] += 1

        # 3. Determine Primary Emotion
        primary = 'neutral'
        confidence = 50

        if score > 0:
            primary = 'happy'
            confidence = min(50 + (score * 10), 95)
        elif score < 0:
            # Negative sentiment - distinguish between sad, angry, fearful
            max_count = 0
            best_neg = 'sad'
            
            for em in ['angry', 'fearful', 'sad']:
                if keyword_counts[em] > max_count:
                    max_count = keyword_counts[em]
                    best_neg = em
            
            if max_count == 0:
                if score < -3: best_neg = 'angry'
                else: best_neg = 'sad'

            primary = best_neg
            confidence = min(50 + (abs(score) * 10), 95)
        else:
            if words_matched == 0: confidence = 40
            else: confidence = 80

        # 4. Construct Scores
        scores = {
            "happy": 50 + score*10 if score > 0 else 5,
            "sad": 50 + abs(score)*10 if primary == 'sad' else 10,
            "angry": 50 + abs(score)*10 if primary == 'angry' else 10,
            "fearful": 50 + abs(score)*10 if primary == 'fearful' else 10,
            "neutral": 60 if score == 0 else 10
        }

        # Normalize
        total = sum(scores.values())
        for k in scores:
            scores[k] = round((scores[k] / total) * 100)

        return {
            "primary": primary,
            "confidence": round(confidence),
            "scores": scores,
            "text": text
        }
