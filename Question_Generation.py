import google.generativeai as genai
import psycopg2
import os
from Resume import data
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Configure the API key securely from an environment variable
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Database connection configuration
DB_CONFIG = {
    "dbname": "Question",  # Replace with your database name
    "user": "postgres",  # Replace with your username
    "password": os.getenv("DB_PASSWORD"),  # Retrieve password from an environment variable
    "host": "localhost",  # Replace with your server's IP if remote
    "port": "5432"  # Default PostgreSQL port (change if necessary)
}

# Function to create the table if it doesn't exist
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS interview_questions (
        id SERIAL PRIMARY KEY,
        type TEXT NOT NULL,
        subtype TEXT,  -- New column to store specific values (e.g., Python, C++, etc.)
        question TEXT NOT NULL,
        answer TEXT,
        user_answer TEXT,
        score FLOAT
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error creating table: {e}")

# Function to insert interview questions into the database
def insert_into_db(question_type, subtype, question):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(insert_query, (question_type, subtype, question, None, None, None))
                conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Database error while inserting: {e}")

# Function to generate interview questions and store them in PostgreSQL
def generate_interview_questions(input_jsons):
    """
    Generate easy-level, short interview questions based on input JSON data
    and store the results in PostgreSQL.
    """
    for input_data in input_jsons:
        for key, value in input_data.items():  # This works now since input_data is a dictionary
            if key == "skill":
                # Generate questions for each skill
                for skill in value:
                    prompt = (
                        f"Generate one short and easy-level interview question based on the skill: "
                        f"{skill}. The question should be simple and concise, suitable for beginners."
                    )
                    subtype = skill  # Assign the skill as the subtype

                    # Generate the question using the model
                    response = model.generate_content(prompt)
                    question = response.text.strip()

                    # Insert the record into PostgreSQL
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            insert_query = """
                            INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
                            cur.execute(insert_query, (key, subtype, question, None, None, None))
                            conn.commit()

            elif key == "experience":
                # Generate questions for each experience entry
                for experience in value:
                    subtype = experience.split()[0]  # Extract the first word (e.g., SDE, Intern)
                    prompt = (
                        f"Generate one short and easy-level interview question based on the following experience: "
                        f"{experience}. The question should be simple and concise, suitable for beginners."
                    )

                    # Generate the question using the model
                    response = model.generate_content(prompt)
                    question = response.text.strip()

                    # Insert the record into PostgreSQL
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            insert_query = """
                            INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
                            cur.execute(insert_query, (key, subtype, question, None, None, None))
                            conn.commit()

            elif key == "project":
                # Generate questions for each project
                for project in value:
                    subtype = project  # Assign the project as the subtype
                    prompt = (
                        f"Generate one short and easy-level interview question based on the following project: "
                        f"{project}. The question should be simple and concise, suitable for beginners."
                    )

                    # Generate the question using the model
                    response = model.generate_content(prompt)
                    question = response.text.strip()

                    # Insert the record into PostgreSQL
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            insert_query = """
                            INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
                            cur.execute(insert_query, (key, subtype, question, None, None, None))
                            conn.commit()

            elif key == "certificate":
                # Generate questions for each certificate
                for certificate in value:
                    subtype = certificate  # Assign the certificate as the subtype
                    prompt = (
                        f"Generate one short and easy-level interview question based on the following certification: "
                        f"{certificate}. The question should be simple and concise, suitable for beginners."
                    )

                    # Generate the question using the model
                    response = model.generate_content(prompt)
                    question = response.text.strip()

                    # Insert the record into PostgreSQL
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            insert_query = """
                            INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
                            cur.execute(insert_query, (key, subtype, question, None, None, None))
                            conn.commit()

            elif key == "achievements":
                # Generate questions for each achievement
                for achievement in value:
                    subtype = achievement  # Assign the achievement as the subtype
                    prompt =(
                        f"Generate one short and easy-level interview question based on the following achievement: "
                        f"{achievement}. The question should be simple and concise, suitable for beginners."
                    )

                    # Generate the question using the model
                    response = model.generate_content(prompt)
                    question = response.text.strip()

                    # Insert the record into PostgreSQL
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            insert_query = """
                            INSERT INTO interview_questions (type, subtype, question, answer, user_answer, score)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
                            cur.execute(insert_query, (key, subtype, question, None, None, None))
                            conn.commit()


# Create table and generate questions
create_table()
generate_interview_questions(data)
