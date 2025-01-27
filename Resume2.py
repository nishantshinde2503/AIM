import fitz
import pandas as pd
from unidecode import unidecode
import re

def analyze_resume(filepath):
    doc = fitz.open(filepath)
    rows = []

    # Extract spans
    for page in doc:
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if block['type'] == 0:  # Text blocks
                for line in block['lines']:
                    for span in line['spans']:
                        text = unidecode(span['text']).strip()
                        if text:
                            rows.append({
                                'text': text,
                                'font_size': span['size'],
                                'font': span['font'],
                                'is_bold': "bold" in span['font'].lower(),
                                'is_upper': text.isupper(),
                                'ymin': span['bbox'][1]  # Top coordinate for ordering
                            })

    # Create a DataFrame from spans
    span_df = pd.DataFrame(rows).sort_values(by='ymin')
    
    # Group spans into headings and contents
    headings, contents = [], []
    current_heading = None
    content_lines = []

    avg_font_size = span_df['font_size'].mean()

    for _, row in span_df.iterrows():
        text = row['text']
        font_size = row['font_size']
        is_bold = row['is_bold']
        is_upper = row['is_upper']

        # Identify headings
        if font_size > avg_font_size or is_bold or is_upper:
            if current_heading:
                headings.append(current_heading)
                contents.append("\n".join(content_lines).strip())
            current_heading = text
            content_lines = []
        else:
            content_lines.append(text)

    # Add the last heading and its content
    if current_heading:
        headings.append(current_heading)
        contents.append("\n".join(content_lines).strip())

    # Create a DataFrame of headings and content
    resume_df = pd.DataFrame({'Headings': headings, 'Content': contents})

    # Categorize content into sections
    data = {"skills": [], "experience": [], "projects": [], "certifications": [], "achievements": []}

    for _, row in resume_df.iterrows():
        heading = row['Headings'].lower()
        content = row['Content']
        
        if "skills" in heading:
            # Split skills by commas or periods
            data["skills"] = re.split(r',|\.', content)
        elif "experience" in heading:
            # Add experience content as-is
            data["experience"].extend(content.split("\n"))  # Split by newlines to handle multi-line descriptions
        elif "projects" in heading:
            # Add project content as-is
            data["projects"].extend(content.split("\n"))  # Split by newlines to handle multi-line descriptions
        elif "certifications" in heading:
            # Split certifications by periods
            data["certifications"] = [cert.strip() for cert in content.split('.') if cert.strip()]
        elif "achievements" in heading or "summary" in heading:
            # Include achievements or summary-related content
            data["achievements"].extend(re.split(r',|\.', content))

    # Clean up empty or malformed entries
    for key in data:
        data[key] = [item.strip() for item in data[key] if item.strip()]

    # Print output
    for key, value in data.items():
        print(f"{key.capitalize()}: [")
        for item in value:
            print(f'    "{item}",')
        print("]")

# Call the function with the uploaded PDF
analyze_resume('C:/Users/nisha/Desktop/Review 1/Sample Resume 4.pdf')