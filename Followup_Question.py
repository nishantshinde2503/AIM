import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv("API_KEY")

# If the API key is not found, raise an error
if not api_key:
    raise ValueError("API_KEY is missing! Please set the API_KEY in your .env file.")

# Configure the API with the loaded key
genai.configure(api_key=api_key)

# Initialize the model (you can choose the desired model like gemini-1.5-flash, if available)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_followup_question_and_answer(score, user_answer, question, context):
    """
    Generate a follow-up question and a correct answer based on the user's score and answer.
    """
    # Start building the prompt, adding context
    prompt = f"Context: {context}\n\n"

    if 80 <= score <= 100:
        # High confidence: Generate an advanced-level follow-up question
        prompt += (
            f"The user has demonstrated a high level of confidence. Generate a challenging follow-up question that tests their depth of knowledge.\n\n"
            f"User's answer: {user_answer}\n"
            f"Question: {question}\n"
            f"Follow-up question:"
        )
    elif 50 <= score <= 79:
        # Medium confidence: Moderate difficulty follow-up
        prompt += (
            f"The user has moderate confidence. Generate a follow-up question to encourage deeper understanding.\n\n"
            f"User's answer: {user_answer}\n"
            f"Question: {question}\n"
            f"Follow-up question:"
        )
    elif 30 <= score <= 49:
        # Low confidence: Simple, clarifying question
        prompt += (
            f"The user has low confidence, indicating nervousness. Generate a simple follow-up question to clarify their answer and help them build confidence.\n\n"
            f"User's answer: {user_answer}\n"
            f"Question: {question}\n"
            f"Follow-up question:"
        )
    elif 0 <= score <= 29:
        # Very low confidence: Basic, supportive question
        prompt += (
            f"The user is very nervous and lacks confidence. Generate a basic, encouraging follow-up question to help the user regain confidence and ease into the topic.\n\n"
            f"User's answer: {user_answer}\n"
            f"Question: {question}\n"
            f"Follow-up question:"
        )
    else:
        return "Invalid score. Score must be between 0 and 100."

    # Generate the follow-up question using the model
    response = model.generate_content(prompt)

    if response:
        return response.text.strip()  # Return the follow-up question and correct answer as the response text
    else:
        return "Failed to generate follow-up question."

# Example usage
if __name__ == "__main__":
    context = "Q: What are you good at? A: I am good at app development, especially in Flutter. Q: How would you use Flutter for app development? A: I have worked on cross-platform apps using Flutter for building task management and weather apps."
    user_score = 99  # Example low score (indicating nervousness)
    user_answer = "I do not know"
    question = "What are widgets in flutter?"

    follow_up_and_answer = generate_followup_question_and_answer(user_score, user_answer, question, context)
    print("Generated Follow-Up Question and Answer:", follow_up_and_answer)
