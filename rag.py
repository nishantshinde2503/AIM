import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Configure the API key
genai.configure(api_key="AIzaSyAj8P8tfNWx385yVJk4y4dxvlzwWZzEIqA")
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample previous conversation data (questions and responses)
previous_conversation = [
    ("What are you good at?", "I am good at app development, especially in Flutter."),
    ("How would you use Flutter for app development?", "I have worked on cross-platform apps using Flutter for building task management and weather apps."),
    ("What is your experience with Python?", "I have experience working with Python for data science and web development."),
    # Add more historical data here
]

# Function to calculate cosine similarity between the new question and previous questions
def get_similar_questions(new_question, prev_conversations, top_k=3):
    # Extracting the questions from previous conversations
    prev_questions = [q for q, _ in prev_conversations]
    
    # Using TF-IDF Vectorizer to vectorize the questions
    vectorizer = TfidfVectorizer()
    all_questions = prev_questions + [new_question]  # Add the new question to the list for comparison
    tfidf_matrix = vectorizer.fit_transform(all_questions)
    
    # Compute the cosine similarity between the new question and previous ones
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Get the indices of the top_k similar questions
    similar_indices = np.argsort(similarity_scores[0])[::-1][:top_k]
    
    # Get the top k most similar questions and their responses
    similar_q_and_r = [prev_conversations[i] for i in similar_indices]
    
    return similar_q_and_r

# Function to summarize the context
def summarize_context(context):
    # Summarize the context using Gemini API
    context_text = " ".join([f"Q: {q} A: {a}" for q, a in context])
    summary_prompt = f"Summarize the following context:\n{context_text}"
    summary_response = model.generate_content(summary_prompt)
    return summary_response.text.strip()

# Function to simulate the interview flow with RAG approach
def interviewer_ask_with_rag(new_question, previous_conversations, top_k=3):
    # Step 1: Get the top k similar questions and responses from previous conversations
    similar_context = get_similar_questions(new_question, previous_conversations, top_k)
    
    # Step 2: Summarize the top k results to create context
    context = summarize_context(similar_context)
    
    # Print the summarized context
    print("Summarized Context:")
    print(context)

# Example usage
new_question = "Can you explain how you would use Flutter for app development?"
interviewer_ask_with_rag(new_question, previous_conversation, top_k=3)
