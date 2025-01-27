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

def get_feedback_and_rating(question: str, user_answer: str):
    """
    Given a question and user answer, this function generates feedback and a rating for the answer.
    """
    # Construct the prompt for Gemini model
    prompt = f"""
    Given the following question and answer, rate the answer on a scale of 1 to 10 and provide concise feedback. Focus on key areas where the answer can be improved, such as clarity, accuracy, and completeness. Avoid unnecessary elaboration.
    Provide a sample correct answer 
    If the answer is non-technical, provide suggestions on how to structure the answer better.

    Question: {question}
    Answer: {user_answer}

    Output should in the format: Rating : [1-10] Feedback: [concise feedback] Sample Correct Answer: [sample correct answer]
    """

    # Generate the feedback and rating using the model
    response = model.generate_content(prompt)

    if response:
        # Separate the rating and feedback based on the format returned by the model
        response_text = response.text.strip()
        lines = response_text.split("\n")
        
        rating = lines[0] if lines else "Rating not available"
        feedback = "\n".join(lines[1:]) if len(lines) > 1 else "Feedback not available"
        
        return {"rating": rating, "feedback": feedback}
    else:
        return {"error": "Failed to get response from Gemini API"}

# Example question and user answer
question = "What is the difference between SQL and NoSQL?"
user_answer = "SQL is used with structured data and nosql is used with unstructured data."

# Get the rating and feedback
result = get_feedback_and_rating(question, user_answer)

# Print the result
print(result.get("rating"))
print(result.get("feedback"))
