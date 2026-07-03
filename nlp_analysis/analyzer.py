"""
NLP Review Analyzer
Detects scam keywords and analyzes sentiment of user reviews.
"""

SCAM_KEYWORDS = [
    'fraud', 'scam', 'fake', 'cheat', 'cheat', 'hack', 'harass',
    'harassment', 'blackmail', 'threat', 'threaten', 'bully',
    'contacts stolen', 'data leaked', 'privacy violation',
    'illegal', 'trap', 'recovery agent', 'abuse', 'abusive',
    'loot', 'looted', 'robbed', 'extort', 'extortion',
    'shame', 'humiliate', 'humiliation', 'embarrass',
    'beware', 'warning', 'avoid', 'dangerous app',
    'personal data', 'misuse', 'leaked photos',
]

POSITIVE_WORDS = [
    'good', 'great', 'excellent', 'nice', 'helpful', 'fast',
    'genuine', 'trustworthy', 'reliable', 'recommend', 'safe',
    'legitimate', 'approved', 'quick', 'easy', 'smooth',
]

NEGATIVE_WORDS = [
    'bad', 'terrible', 'awful', 'horrible', 'worst', 'poor',
    'slow', 'rejected', 'fraud', 'fake', 'scam', 'useless',
    'waste', 'dangerous', 'risky', 'problem', 'issue',
    'error', 'failed', 'denied', 'stolen', 'lost',
]


def analyze_single_review(text):
    """Analyze a single review text."""
    text_lower = text.lower()

    # Scam keyword detection
    found_keywords = [kw for kw in SCAM_KEYWORDS if kw in text_lower]

    # Sentiment via TextBlob (fallback to rule-based)
    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
    except Exception:
        # Rule-based polarity
        pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
        neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
        polarity = (pos - neg) / max(pos + neg, 1)

    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    # If scam keywords found, override sentiment
    if found_keywords:
        sentiment = 'negative'
        polarity = min(polarity, -0.3)

    return {
        'sentiment': sentiment,
        'polarity': round(polarity, 3),
        'scam_keywords_found': found_keywords,
        'is_scam_review': len(found_keywords) > 0,
    }


def analyze_reviews_bulk(review_texts, loan_app=None):
    """Analyze multiple reviews and optionally save to DB."""
    from nlp_analysis.models import Review
    results = []
    for text in review_texts:
        if not text.strip():
            continue
        result = analyze_single_review(text)
        result['text'] = text
        if loan_app:
            Review.objects.create(
                app=loan_app,
                review_text=text,
                sentiment=result['sentiment'],
                polarity=result['polarity'],
                is_scam_review=result['is_scam_review'],
                scam_keywords_found=result['scam_keywords_found'],
            )
        results.append(result)
    return results
