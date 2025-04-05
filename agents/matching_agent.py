from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(jd_text, cv_text, base_score=50, max_similarity_threshold=0.18):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([jd_text, cv_text])
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # Scale cosine similarity to [0, 100] based on max_similarity_threshold
    scaled_score = (cosine_sim / max_similarity_threshold) * 60  # Scale to remaining 60
    final_score = min(base_score + scaled_score, 100)  # Cap at 100
    return round(final_score, 2)

