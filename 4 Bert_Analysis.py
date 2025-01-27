from bert_score import score
from textblob import TextBlob

def evaluate_answer(user_answer, correct_answer):
    """
    Evaluate the user's answer against the correct answer and generate a score out of 100.
    
    Args:
        user_answer (str): The answer provided by the user.
        correct_answer (str): The correct or reference answer.

    Returns:
        dict: A dictionary containing the overall score and a recommendation for follow-up.
    """
    # Calculate BERT score
    P, R, F1 = score([user_answer], [correct_answer], lang="en", verbose=False)

    # Perform sentiment analysis
    user_sentiment = TextBlob(user_answer).sentiment
    correct_sentiment = TextBlob(correct_answer).sentiment

    # Calculate sentiment similarity
    polarity_similarity = 1 - abs(user_sentiment.polarity - correct_sentiment.polarity)
    subjectivity_similarity = 1 - abs(user_sentiment.subjectivity - correct_sentiment.subjectivity)

    # Combine metrics into a final score
    bert_weight = 0.7
    polarity_weight = 0.2
    subjectivity_weight = 0.1

    final_score = (
        F1.item() * 100 * bert_weight +
        polarity_similarity * 100 * polarity_weight +
        subjectivity_similarity * 100 * subjectivity_weight
    )


    # Compile results
    evaluation_results = {
        "bert_score": {
            "precision": P.item(),
            "recall": R.item(),
            "f1": F1.item()
        },
        "sentiment_analysis": {
            "user_answer": {
                "polarity": user_sentiment.polarity,
                "subjectivity": user_sentiment.subjectivity
            },
            "correct_answer": {
                "polarity": correct_sentiment.polarity,
                "subjectivity": correct_sentiment.subjectivity
            }
        },
        "final_score": round(final_score, 2)
    }
    return evaluation_results

# Example usage
if __name__ == "__main__":
    "High Score"
    user_answer = "ETL is the process of extracting data, transforming it into a usable format, and then loading it into a data warehouse."
    correct_answer = "ETL involves three steps: Extract, Transform, and Load. Data is extracted from sources, transformed into a required structure, and loaded into a target system."

    """Low Score
    "user_answer = ""ETL is a random process used to transfer files to different computers. It does not involve much structure."
    "correct_answer = ""ETL involves three steps: Extract, Transform, and Load. Data is extracted from sources, transformed into a required structure, and loaded into a target system."

    "Medium Score"
    "user_answer = ""ETL is the process of extracting and transforming data into a structured format before loading it into a database.""
    "correct_answer = ""ETL involves three steps: Extract, Transform, and Load. Data is extracted from sources, transformed into a required structure, and loaded into a target system.""
"""
    results = evaluate_answer(user_answer, correct_answer)
    
    # Print Results
    print("Evaluation Results:")
    print("BERT Score - Precision:", results["bert_score"]["precision"])
    print("BERT Score - Recall:", results["bert_score"]["recall"])
    print("BERT Score - F1:", results["bert_score"]["f1"])
    print("Sentiment Analysis (User Answer):", results["sentiment_analysis"]["user_answer"])
    print("Sentiment Analysis (Correct Answer):", results["sentiment_analysis"]["correct_answer"])
    print("Final Score (Out of 100):", results["final_score"])
