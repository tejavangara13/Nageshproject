import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required tokenizer models
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Knowledge base of question-response pairs
KNOWLEDGE_BASE = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What can I do for you?",
    "what is your name": "I am PyBot, your Python-powered virtual assistant.",
    "how are you": "I'm functioning at full capacity! How are you doing?",
    "what can you do": "I can assist you with general queries, FAQs, and task guidance.",
    "what is python": "Python is a high-level, interpreted programming language known for readability.",
    "how to track expenses": "You can record your daily transactions in Task 3's Finance Manager!",
    "bye": "Goodbye! Have a productive day ahead."
}

corpus_questions = list(KNOWLEDGE_BASE.keys())

def preprocess(text):
    """Lowercases text and strips punctuation."""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text

def get_best_response(user_input, threshold=0.3):
    """Finds the closest matching intent using TF-IDF cosine similarity."""
    cleaned_input = preprocess(user_input)
    
    all_texts = corpus_questions + [cleaned_input]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Compute similarity between user input and all known questions
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = similarities.argmax()
    best_score = similarities[0, best_match_idx]
    
    if best_score >= threshold:
        matched_key = corpus_questions[best_match_idx]
        return KNOWLEDGE_BASE[matched_key]
    else:
        return "I'm sorry, I didn't quite understand that. Could you please rephrase?"

def start_chat():
    print("=" * 45)
    print(" PyBot is online! Type 'bye' or 'exit' to quit.")
    print("=" * 45)
    
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"PyBot: {KNOWLEDGE_BASE['bye']}")
            break
            
        reply = get_best_response(user_input)
        print(f"PyBot: {reply}")

if __name__ == "__main__":
    start_chat()